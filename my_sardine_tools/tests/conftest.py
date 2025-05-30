"""
Pytest configuration for my_sardine_tools tests.
Since sardine is a live coding REPL environment, we mock sardine imports
to test our helper logic without initializing the full sardine system.
"""

import sys
from unittest.mock import MagicMock, Mock

import pytest


# Mock sardine modules IMMEDIATELY before any imports can happen
class MockSardineModule(MagicMock):
    def __getattr__(self, name):
        return MagicMock()


# Create specific mocks for functions we need to track
mock_original_D = Mock()
mock_original_d = Mock()
mock_ZD = Mock()
mock_zd = Mock()
mock_P = Mock(side_effect=lambda pattern, i=0: float(pattern.split()[i % len(pattern.split())]))
mock_Player = Mock()
mock_bowl = Mock()
mock_bowl.scheduler = Mock()
mock_bowl.scheduler.runners = []
mock_bowl.handlers = []
mock_bowl.clock = Mock()
mock_bowl.clock.beat_duration = 0.5
mock_bowl.add_handler = Mock()

# Create a mock sardine_core.run module with our specific mocks
mock_run_module = MockSardineModule()
mock_run_module.D = mock_original_D  # This will be imported as original_D
mock_run_module.d = mock_original_d  # This will be imported as original_d
mock_run_module.ZD = mock_ZD
mock_run_module.zd = mock_zd
mock_run_module.P = mock_P
mock_run_module.bowl = mock_bowl
mock_run_module.swim = Mock()
mock_run_module.die = Mock()
mock_run_module.sleep = Mock()

# Create a mock sardine_core.handlers.player module
mock_player_module = MockSardineModule()
mock_player_module.Player = mock_Player

# Pre-populate sys.modules with mocked sardine modules
SARDINE_MODULES = {
    "sardine_core": MockSardineModule(),
    "sardine_core.run": mock_run_module,
    "sardine_core.handlers": MockSardineModule(),
    "sardine_core.handlers.player": mock_player_module,
    "sardine_core.handlers.osc": MockSardineModule(),
    "sardine_core.scheduler": MockSardineModule(),
    "sardine_core.scheduler.scheduler": MockSardineModule(),
    "sardine_core.scheduler.async_runner": MockSardineModule(),
}

for module_name, mock_module in SARDINE_MODULES.items():
    if module_name not in sys.modules:
        sys.modules[module_name] = mock_module


@pytest.fixture(autouse=True)
def mock_sardine_modules():
    """Mock sardine modules to prevent initialization."""
    # Modules are already mocked above, just yield them
    yield SARDINE_MODULES


@pytest.fixture
def mock_sardine_functions():
    """Mock common sardine functions used in tests."""
    return {
        "Player": mock_Player,
        "bowl": mock_bowl,
        "swim": mock_run_module.swim,
        "die": mock_run_module.die,
        "sleep": mock_run_module.sleep,
        "P": mock_P,
        "original_D": mock_original_D,
        "original_d": mock_original_d,
        "D": mock_original_D,  # For compatibility
        "d": mock_original_d,  # For compatibility
        "ZD": mock_ZD,
        "zd": mock_zd,
    }


@pytest.fixture
def temp_audio_files():
    """Create temporary audio files for testing."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as temp_dir:
        samples_dir = Path(temp_dir) / "samples"

        # Create sample family directories
        bd_dir = samples_dir / "bd"
        sfx_dir = samples_dir / "sfx"
        bd_dir.mkdir(parents=True)
        sfx_dir.mkdir(parents=True)

        # Create dummy audio files
        for i in range(3):
            (bd_dir / f"bd{i:02d}.wav").touch()
            (sfx_dir / f"sfx{i:02d}.wav").touch()

        yield samples_dir


@pytest.fixture
def patch_sardine_imports(mock_sardine_functions):
    """Patch sardine imports for all modules including senders."""
    # Reset the mocks before each test
    for mock_obj in mock_sardine_functions.values():
        if hasattr(mock_obj, "reset_mock"):
            mock_obj.reset_mock()

    return mock_sardine_functions


@pytest.fixture
def patch_senders(mock_sardine_functions):
    """Specific fixture for testing senders module."""
    # Reset the mocks before each test
    for mock_obj in mock_sardine_functions.values():
        if hasattr(mock_obj, "reset_mock"):
            mock_obj.reset_mock()

    return mock_sardine_functions
