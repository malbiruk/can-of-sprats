"""
Tests for playback utilities.
"""

from unittest.mock import Mock, call


def test_create_player_new(patch_sardine_imports):
    """Test creating a new player."""
    from my_sardine_tools.playback import create_player

    # Mock Player class
    mock_player = Mock()
    mock_player.name = "test_player"
    patch_sardine_imports["Player"].return_value = mock_player

    result = create_player("test_player")

    patch_sardine_imports["Player"].assert_called_once_with(name="test_player")
    patch_sardine_imports["bowl"].add_handler.assert_called_once_with(mock_player)
    assert result == mock_player


def test_create_player_existing(patch_sardine_imports):
    """Test returning existing player."""
    from my_sardine_tools.playback import create_player

    # Mock existing runner and handler
    existing_runner = Mock()
    existing_runner.name = "existing_player"
    patch_sardine_imports["bowl"].scheduler.runners = [existing_runner]

    existing_handler = Mock()
    existing_handler.name = "existing_player"
    patch_sardine_imports["bowl"].handlers = [existing_handler]

    result = create_player("existing_player")

    assert result == existing_handler
    patch_sardine_imports["bowl"].add_handler.assert_not_called()


def test_loop_fixed_timing(patch_sardine_imports):
    """Test loop with fixed step duration."""
    from my_sardine_tools.playback import loop

    mock_sender = Mock(return_value=None)
    sender_configs = [(mock_sender, {"sound": "bd", "amp": 0.8})]

    duration = loop(*sender_configs, n_steps=4, p=0.25)

    # Should call sender 4 times with correct i values
    assert mock_sender.call_count == 4
    expected_calls = [
        call(sound="bd", amp=0.8, i=0),
        call(sound="bd", amp=0.8, i=1),
        call(sound="bd", amp=0.8, i=2),
        call(sound="bd", amp=0.8, i=3),
    ]
    mock_sender.assert_has_calls(expected_calls)

    # Should sleep 4 times
    assert patch_sardine_imports["sleep"].call_count == 4
    patch_sardine_imports["sleep"].assert_has_calls([call(0.25)] * 4)

    # Total duration should be 1.0
    assert duration == 1.0


def test_loop_pattern_timing(patch_sardine_imports):
    """Test loop with pattern string timing."""
    from my_sardine_tools.playback import loop

    mock_sender = Mock(return_value=None)
    sender_configs = [(mock_sender, {"sound": "hh"})]

    loop(*sender_configs, n_steps=2, p="0.5 0.25")

    # Should call P function for timing
    assert patch_sardine_imports["P"].call_count == 2
    patch_sardine_imports["P"].assert_has_calls([call("0.5 0.25", i=0), call("0.5 0.25", i=1)])


def test_start_single_function(patch_sardine_imports):
    """Test starting a single function."""
    from my_sardine_tools.playback import start

    def test_func():
        pass

    start(test_func)
    patch_sardine_imports["swim"].assert_called_once_with(test_func)


def test_start_multiple_functions(patch_sardine_imports):
    """Test starting multiple functions."""
    from my_sardine_tools.playback import start

    def func1():
        pass

    def func2():
        pass

    start(func1, func2)

    assert patch_sardine_imports["swim"].call_count == 2
    patch_sardine_imports["swim"].assert_has_calls([call(func1), call(func2)])


def test_start_with_kwargs(patch_sardine_imports):
    """Test starting with additional arguments."""
    from my_sardine_tools.playback import start

    def test_func():
        pass

    start(test_func, quant=0.5)
    patch_sardine_imports["swim"].assert_called_once_with(test_func, quant=0.5)


def test_stop_functions(patch_sardine_imports):
    """Test stopping functions."""
    from my_sardine_tools.playback import stop

    def func1():
        pass

    def func2():
        pass

    stop(func1, func2)

    assert patch_sardine_imports["die"].call_count == 2
    patch_sardine_imports["die"].assert_has_calls([call(func1), call(func2)])
