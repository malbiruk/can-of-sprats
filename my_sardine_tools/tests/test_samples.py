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


def test_cut_logic(patch_sardine_imports):
    """Test the cut function logic without actual audio processing."""
    from my_sardine_tools.samples import cut, set_lengths

    # Set up sample length
    set_lengths({"test:0": 4.0})
    patch_sardine_imports["bowl"].clock.beat_duration = 0.5
    patch_sardine_imports["P"].side_effect = [0, 1, 2, 3]  # Slice indices

    duration = cut("test:0", n_slices=4, sequence="0 1 2 3", p=0.25)

    # Should call D for each slice
    assert patch_sardine_imports["D"].call_count == 4

    # Should sleep between slices
    assert patch_sardine_imports["sleep"].call_count == 4

    assert duration == 1.0
