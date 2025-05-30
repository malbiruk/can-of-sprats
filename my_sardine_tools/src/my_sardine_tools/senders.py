from functools import wraps

from sardine_core.run import ZD, zd
from sardine_core.run import D as original_D
from sardine_core.run import d as original_d


@wraps(original_d)
def d(*args, **kwargs):
    """Drop-in replacement for d() that handles note and frequency patterns with proper silences"""

    # Check if there's a note pattern with rests
    note_pattern = kwargs.get("n") or kwargs.get("midinote") or kwargs.get("freq")

    if note_pattern and isinstance(note_pattern, str) and "." in note_pattern:
        # If first arg is a string (the most common case)
        if args:
            instrument = args[0]
            args = (f"{instrument} ^| [{instrument} ^| [{note_pattern}]]",) + args[1:]

    # Pass through to original d
    return original_d(*args, **kwargs)


@wraps(original_D)
def D(*args, **kwargs):
    """Drop-in replacement for D() that handles note and frequency patterns with proper silences"""

    # Check if there's a note pattern with rests
    note_pattern = kwargs.get("n") or kwargs.get("midinote") or kwargs.get("freq")

    if note_pattern and isinstance(note_pattern, str) and "." in note_pattern:
        if args:
            # First arg is the instrument (the most common case)
            instrument = args[0]
            args = (f"{instrument} ^| [{instrument} ^| [{note_pattern}]]",) + args[1:]
        elif "sound" in kwargs:
            # Instrument is provided as 'sound' keyword argument
            instrument = kwargs["sound"]
            kwargs["sound"] = f"{instrument} ^| [{instrument} ^| [{note_pattern}]]"

    # Pass through to original D
    return original_D(*args, **kwargs)


def parse_ziff_duration(note: str) -> float | None:
    if not note:
        return None

    # Basic duration mappings (in beats)
    durations = {
        "w": 4.0,  # whole note
        "h": 2.0,  # half note
        "q": 1.0,  # quarter note
        "e": 0.5,  # eighth note
        "s": 0.25,  # sixteenth note
    }

    if note[0] in durations:
        duration = durations[note[0]]
        if len(note) > 1 and note[1] == ".":
            duration *= 1.5  # dotted note
        return duration
    return None


@wraps(zd)
def zd_mono(name, ziff, coef=0.5, **kwargs):
    """generates sustains based on ziff pattern"""
    notes = ziff.split()
    durations = " ".join([str(dur * coef) for note in notes if (dur := parse_ziff_duration(note))])
    kwargs["sustain"] = durations
    return zd(name, ziff=ziff, **kwargs)


@wraps(ZD)
def ZD_mono(name, ziff, coef=0.5, **kwargs):
    """generates sustains based on ziff pattern"""
    notes = ziff.split()
    durations = " ".join([str(dur * coef) for note in notes if (dur := parse_ziff_duration(note))])
    kwargs["sustain"] = durations
    return ZD(name, ziff=ziff, **kwargs)


# TODO: Vortex to MIDI:
# d1 * s("0 60")

# hush(d1)
# silence()

# @swim
# def gui_loop(p=1, i=0):
#     blip = d1.stream.get("0", 0)
#     bloop = d1.stream.get("60", 1)
#     print(blip)
#     print(bloop)
#     again(gui_loop, p=1, i=i + 1)
