import random
from pathlib import Path
from typing import Callable

import soundfile as sf
from sardine_core.run import D, P, bowl, sleep

_SAMPLE_LENGTHS = {}


def set_lengths(lengths):
    global _SAMPLE_LENGTHS
    _SAMPLE_LENGTHS = lengths


def get_length(sample):
    if sample not in _SAMPLE_LENGTHS:
        raise KeyError(
            f"Sample '{sample}' not found. Did you forget to call `calculate_sample_lengths()`?"
        )
    return _SAMPLE_LENGTHS[sample]


def calculate_sample_lengths(samples_dir=None, sample_families=None) -> dict[str, float]:
    """
    Calculate the lengths of audio samples and store them in a dictionary.

    Args:
        samples_dir: The directory or list of directories containing the sample folders
                    (default: uses SuperDirt's default location)
        sample_families: List of sample families to include (e.g., ["bd", "sfx"]). If None, include all.

    Returns:
        Dictionary mapping sample names (e.g., "sfx:0") to their lengths in seconds
    """
    # Handle samples_dir input
    if samples_dir is None:
        # Try common SuperDirt sample locations
        potential_paths = [
            Path.home()
            / ".local"
            / "share"
            / "SuperCollider"
            / "downloaded-quarks"
            / "Dirt-Samples",
            Path.home()
            / "Library"
            / "Application Support"
            / "SuperCollider"
            / "downloaded-quarks"
            / "Dirt-Samples",
        ]

        samples_dirs = []
        for path in potential_paths:
            if path.exists():
                samples_dirs = [path]
                break

        if not samples_dirs:
            raise FileNotFoundError("Could not find SuperDirt samples directory")
    else:
        # Convert to list if single directory provided
        if isinstance(samples_dir, (str, Path)):
            samples_dirs = [Path(samples_dir)]
        else:
            # Assume it's a list/iterable of directories
            samples_dirs = [Path(d) for d in samples_dir]

    sample_lengths = {}

    # Process each samples directory
    for samples_dir_path in samples_dirs:
        # Get list of sample families if not provided (from first directory)
        if sample_families is None and not sample_lengths:  # Only do this once
            sample_families = [d.name for d in samples_dir_path.iterdir() if d.is_dir()]

        for family in sample_families:
            family_dir = samples_dir_path / family
            if not family_dir.exists():
                print(f"Warning: Sample family '{family}' not found in {samples_dir_path}")
                continue

            # List all audio files in the directory
            audio_files = [
                f
                for f in family_dir.iterdir()
                if f.suffix.lower() in [".wav", ".aif", ".aiff", ".flac", ".mp3"]
            ]

            # Sort audio files to ensure consistent numbering
            audio_files.sort()

            # Start numbering from where we left off for this family
            start_index = len([k for k in sample_lengths.keys() if k.startswith(f"{family}:")])

            for i, file_path in enumerate(audio_files):
                try:
                    info = sf.info(str(file_path))
                    duration = info.duration

                    # Store in dictionary with SuperDirt-style naming (e.g., "bd:0")
                    sample_name = f"{family}:{start_index + i}"
                    sample_lengths[sample_name] = duration

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    set_lengths(sample_lengths)
    return sample_lengths


def _is_pattern(value: str | None | float) -> bool:
    """
    Check if the value is a pattern string.
    A pattern is any string that cannot be interpreted as a float.
    """
    if not isinstance(value, str):
        return False
    try:
        float(value)
        return False
    except ValueError:
        return True

def cut(
    sample: str,
    n_slices: int = 8,
    sequence: str | None = None,
    n_steps: int | None = None,
    p: str | None = None,
    stretch: float | None = None,
    base_start: float | None = None,
    base_end: float | None = None,
    speed: float | str | None = None,
    **kwargs,
) -> float:
    """
    Play slices of a sample based on specified patterns.

    Args:
        sample: Sample name (e.g., "sfx:0")
        n_slices: Number of equal slices to divide the sample into
        sequence: Pattern of slice indices to play (0 to n_slices-1)
        n_steps: Length of the loop
        p: Period or duration for each slice
        stretch: Stretch full sample to n_beats
        base_start: Start position of the sample (0.0 to 1.0)
        base_end: End position of the sample (0.0 to 1.0)
        speed: Playback speed (can be a pattern string)
        **kwargs: Additional arguments to pass to the sender (D)

    Returns:
        Total duration of all slices played
    """
    sample_length = get_length(sample)

    if n_steps is None:
        if sequence is None and not _is_pattern(p):
            n_steps = n_slices
        else:
            potential_patterns = (
                p,
                sequence,
                speed,
                kwargs.get("note"),
                kwargs.get("pan"),
                kwargs.get("amp"),
                kwargs.get("gain"),
                kwargs.get("shape"),
            )
            patterns = [pattern for pattern in potential_patterns if _is_pattern(pattern)]
            n_steps = max(
                len(bowl.parser.parse(str(pattern).replace("None", "."))) for pattern in patterns
            )

    if base_start is None:
        base_start = 0.0

    if base_end is None:
        base_end = 1.0

    if stretch is not None:
        target_duration = stretch * bowl.clock.beat_duration
        base_speed = sample_length / target_duration
    else:
        base_speed = 1

    if sequence is None:
        sequence = " ".join(str(num) for num in range(n_slices))

    total_duration = 0

    for j in range(n_steps):
        current_slice = P(sequence, j)
        actual_speed = base_speed * (P(speed, i=j) if isinstance(speed, str) else speed or 1.0)
        if abs(actual_speed) == 0:
            actual_speed = 1.0

        if current_slice is not None:
            params = (
                dict(
                    sound=sample,
                    begin=base_start + (base_end - base_start) / n_slices * current_slice,
                    end=(base_end - base_start) / n_slices * (current_slice + 1),
                    speed=actual_speed,
                    cut=1,
                    i=j,
                )
                | kwargs
            )
            D(**params)

        if isinstance(p, str):
            step_duration = P(p, i=j)
        elif p is not None:
            step_duration = p
        else:  # Auto-calculate based on speed
            if stretch is None:
                base_slice_duration = (sample_length / n_slices) / bowl.clock.beat_duration
                step_duration = base_slice_duration / abs(actual_speed)
            else:
                base_slice_duration = stretch / n_slices
                step_duration = base_slice_duration / abs(actual_speed)

        sleep(step_duration)
        total_duration += step_duration

    return total_duration


def granulate(
    sample: str,
    density: int = 8,
    duration: float = 1.0,
    grain_size: float = 0.1,
    position_jitter: float = 0.2,
    speed_range: tuple[float, float] = (-2.0, 1.0),
    amp_jitter: float = 0.1,
    pan_range: tuple[float, float] = (0.0, 1.0),  # Added pan range
    base_speed: float = 1.0,
    base_amp: float = 0.8,
    base_pan: float = 0.5,  # Added base pan (center)
    sender: Callable = D,
    **kwargs,
) -> float:
    """
    Create a granular synthesis effect by playing many small grains of a sample.

    Args:
        sample: Sample name (e.g., "sfx:0")
        density: Number of grains per beat
        duration: Total duration in beats
        grain_size: Size of each grain in sample position units (0-1)
        position_jitter: Amount of random variation in grain position (0-1)
        speed_range: Range of speeds as (min, max) - negative values play backwards
        amp_jitter: Amount of random variation in grain amplitude
        pan_range: Range of pan values as (min, max) from 0 (left) to 1 (right)
        base_speed: Base playback speed (can be negative for backwards)
        base_amp: Base amplitude
        base_pan: Base pan position (0.5 = center, 0 = left, 1 = right)
        sender: Function to send sample (default: D)
        **kwargs: Additional arguments to pass to the sender

    Returns:
        Total duration
    """
    total_grains = int(density * duration)
    grain_duration = duration / total_grains

    for i in range(total_grains):
        # Calculate random position with jitter
        position = random.random() * (1.0 - grain_size)
        position_offset = (random.random() * 2 - 1) * position_jitter
        position = max(0, min(1 - grain_size, position + position_offset))

        # Calculate grain parameters with ranges
        min_speed, max_speed = speed_range
        speed = base_speed + random.uniform(min_speed, max_speed)

        amp = base_amp + (random.random() * 2 - 1) * amp_jitter

        # Calculate pan with range
        min_pan, max_pan = pan_range
        pan = base_pan + random.uniform(min_pan - base_pan, max_pan - base_pan)
        pan = max(0.0, min(1.0, pan))  # Clamp between 0 and 1

        # Prepare arguments
        call_kwargs = kwargs.copy()
        call_kwargs.update(
            {
                "begin": position,
                "end": position + grain_size,
                "speed": speed,
                "amp": amp,
                "pan": pan,
            }
        )

        # Play the grain
        sender(sample, **call_kwargs)

        # Sleep for grain duration
        sleep(grain_duration)

    return duration
