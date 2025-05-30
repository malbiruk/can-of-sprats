"""
Tests for enhanced senders.
"""


def test_parse_ziff_duration():
    """Test parsing ziffers note durations."""
    from my_sardine_tools.senders import parse_ziff_duration

    # Basic notes
    assert parse_ziff_duration("w") == 4.0  # whole note
    assert parse_ziff_duration("h") == 2.0  # half note
    assert parse_ziff_duration("q") == 1.0  # quarter note
    assert parse_ziff_duration("e") == 0.5  # eighth note
    assert parse_ziff_duration("s") == 0.25  # sixteenth note

    # Dotted notes
    assert parse_ziff_duration("h.") == 3.0  # dotted half
    assert parse_ziff_duration("q.") == 1.5  # dotted quarter

    # Invalid notes
    assert parse_ziff_duration("x") is None
    assert parse_ziff_duration("") is None


def test_enhanced_D_with_rests(patch_sardine_imports):
    """Test enhanced D function with note patterns containing rests."""
    from my_sardine_tools.senders import D

    D("piano", n="C4 . E4 G4")

    # Should call original D with transformed pattern
    patch_sardine_imports["original_D"].assert_called_once()
    args, kwargs = patch_sardine_imports["original_D"].call_args

    # First argument should be transformed to handle silences
    assert "piano" in args[0]
    assert "^|" in args[0]  # Should contain silence pattern


def test_enhanced_D_without_rests(patch_sardine_imports):
    """Test enhanced D function with normal patterns."""
    from my_sardine_tools.senders import D

    D("piano", n="C4 E4 G4")

    # Should pass through unchanged to original_D
    patch_sardine_imports["original_D"].assert_called_once_with("piano", n="C4 E4 G4")


def test_ZD_mono_basic(patch_sardine_imports):
    """Test ZD_mono with basic pattern."""
    from my_sardine_tools.senders import ZD_mono

    ZD_mono("piano", "q e h", coef=0.5)

    patch_sardine_imports["ZD"].assert_called_once()
    args, kwargs = patch_sardine_imports["ZD"].call_args

    # Should add sustain parameter
    assert "sustain" in kwargs
    assert kwargs["sustain"] == "0.5 0.25 1.0"  # q*0.5, e*0.5, h*0.5
    assert kwargs["ziff"] == "q e h"


def test_zd_mono_with_custom_coef(patch_sardine_imports):
    """Test zd_mono with custom coefficient."""
    from my_sardine_tools.senders import zd_mono

    zd_mono("piano", "h q e", coef=0.75)

    patch_sardine_imports["zd"].assert_called_once()
    args, kwargs = patch_sardine_imports["zd"].call_args

    # Should add sustain parameter with custom coefficient
    assert "sustain" in kwargs
    assert kwargs["sustain"] == "1.5 0.75 0.375"  # h*0.75, q*0.75, e*0.75
