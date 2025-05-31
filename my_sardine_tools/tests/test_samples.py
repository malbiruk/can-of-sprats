"""
Tests for sample utilities.
Note: These test the logic without actual audio files.
"""

from unittest.mock import Mock, patch

import pytest


def test_sample_length_storage():
    """Test storing and retrieving sample lengths."""
    from my_sardine_tools.samples import get_length, set_lengths

    test_lengths = {"test:0": 1.5, "test:1": 2.0}
    set_lengths(test_lengths)

    assert get_length("test:0") == 1.5
    assert get_length("test:1") == 2.0


def test_get_length_missing_sample():
    """Test getting length for missing sample raises error."""
    from my_sardine_tools.samples import get_length, set_lengths

    set_lengths({})

    with pytest.raises(KeyError, match="Sample 'missing:0' not found"):
        get_length("missing:0")


@patch("my_sardine_tools.samples.sf")
def test_calculate_sample_lengths(mock_sf, temp_audio_files):
    """Test calculating sample lengths from directory."""
    from my_sardine_tools.samples import calculate_sample_lengths

    # Mock soundfile info
    mock_info = Mock()
    mock_info.duration = 2.0
    mock_sf.info.return_value = mock_info

    lengths = calculate_sample_lengths(temp_audio_files)

    # Should find samples in both families
    expected_keys = ["bd:0", "bd:1", "bd:2", "sfx:0", "sfx:1", "sfx:2"]
    assert all(key in lengths for key in expected_keys)

    # All should have the mocked duration
    assert all(lengths[key] == 2.0 for key in expected_keys)


def test_cut_logic_with_explicit_n_steps(patch_sardine_imports):
    """Test the cut function logic with explicit n_steps."""
    from my_sardine_tools.samples import cut, set_lengths

    # Set up sample length
    set_lengths({"test:0": 4.0})
    patch_sardine_imports["bowl"].clock.beat_duration = 0.5
    patch_sardine_imports["P"].side_effect = [0, 1, 2, 3]  # Slice indices

    # Provide explicit n_steps to avoid parser logic
    duration = cut("test:0", n_slices=4, sequence="0 1 2 3", p=0.25, n_steps=4)

    # Should call D for each slice
    assert patch_sardine_imports["D"].call_count == 4

    # Should sleep between slices
    assert patch_sardine_imports["sleep"].call_count == 4

    assert duration == 1.0


def test_cut_logic_with_pattern_parsing(patch_sardine_imports):
    """Test the cut function logic with pattern parsing."""
    from my_sardine_tools.samples import cut, set_lengths

    # Set up sample length
    set_lengths({"test:0": 4.0})
    patch_sardine_imports["bowl"].clock.beat_duration = 0.5

    # Create a P mock that handles different calls appropriately
    def mock_p_function(pattern, i=0, j=None):
        if pattern == "0 1 2 3":  # sequence pattern
            return [0, 1, 2, 3][i if j is None else j]
        elif pattern == "0.25 0.25 0.25 0.25":  # timing pattern
            return 0.25
        else:
            return 0

    patch_sardine_imports["P"].side_effect = mock_p_function

    # Mock the parser to return a list with known length
    mock_parser = Mock()
    mock_parser.parse.return_value = [0, 1, 2, 3]  # Return a list with 4 elements
    patch_sardine_imports["bowl"].parser = mock_parser

    # Don't provide n_steps so it uses pattern parsing
    duration = cut("test:0", n_slices=4, sequence="0 1 2 3", p="0.25 0.25 0.25 0.25")

    # Should call D for each slice
    assert patch_sardine_imports["D"].call_count == 4

    # Should sleep between slices
    assert patch_sardine_imports["sleep"].call_count == 4

    assert duration == 1.0


def test_cut_with_stretch(patch_sardine_imports):
    """Test the cut function with stretch parameter."""
    from my_sardine_tools.samples import cut, set_lengths

    # Set up sample length
    set_lengths({"test:0": 4.0})
    patch_sardine_imports["bowl"].clock.beat_duration = 0.5
    patch_sardine_imports["P"].side_effect = [0, 1]  # Two slices

    cut("test:0", n_slices=2, sequence="0 1", stretch=2.0, n_steps=2)

    # Should call D for each slice
    assert patch_sardine_imports["D"].call_count == 2

    # Check that speed was calculated based on stretch
    calls = patch_sardine_imports["D"].call_args_list
    # When stretch=2.0, target_duration = 2.0 * 0.5 = 1.0
    # base_speed = sample_length / target_duration = 4.0 / 1.0 = 4.0
    assert calls[0][1]["speed"] == 4.0
    assert calls[1][1]["speed"] == 4.0


def test_granulate_basic(patch_sardine_imports):
    """Test basic granulate function."""
    from my_sardine_tools.samples import granulate

    # Mock random to be predictable
    with patch("my_sardine_tools.samples.random") as mock_random:
        # Use return_value instead of side_effect for consistent behavior
        mock_random.random.return_value = 0.5
        mock_random.uniform.return_value = 0.0

        duration = granulate(
            "test:0", density=2, duration=1.0, grain_size=0.1, sender=patch_sardine_imports["D"]
        )

        # Should call D twice (density=2, duration=1.0)
        assert patch_sardine_imports["D"].call_count == 2

        # Should sleep twice
        assert patch_sardine_imports["sleep"].call_count == 2

        assert duration == 1.0


def test_granulate_with_parameters(patch_sardine_imports):
    """Test granulate with various parameters."""
    from my_sardine_tools.samples import granulate

    with patch("my_sardine_tools.samples.random") as mock_random:
        mock_random.random.return_value = 0.5
        mock_random.uniform.return_value = 0.1

        duration = granulate(
            "test:0",
            density=4,
            duration=0.5,
            grain_size=0.05,
            position_jitter=0.1,
            speed_range=(-1.0, 1.0),
            amp_jitter=0.05,
            pan_range=(0.2, 0.8),
            base_speed=2.0,
            base_amp=0.6,
            base_pan=0.3,
            sender=patch_sardine_imports["D"],
        )

        # Should call D four times (density=4, duration=0.5)
        assert patch_sardine_imports["D"].call_count == 2  # 4 * 0.5 = 2 grains

        # Check that parameters are being passed correctly
        calls = patch_sardine_imports["D"].call_args_list
        assert len(calls) == 2

        # Check that basic parameters are in the calls
        for call in calls:
            args, kwargs = call
            assert "begin" in kwargs
            assert "end" in kwargs
            assert "speed" in kwargs
            assert "amp" in kwargs
            assert "pan" in kwargs

        assert duration == 0.5
