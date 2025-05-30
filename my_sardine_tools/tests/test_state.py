"""
Tests for the State management system.
State is independent of sardine so we can test it directly.
"""

from my_sardine_tools.state import State


class TestStateBasics:
    def test_create_empty_state(self):
        """Test creating an empty state."""
        state = State()
        assert len(state) == 0
        assert isinstance(state, dict)

    def test_dot_notation_access(self):
        """Test accessing nested attributes with dot notation."""
        state = State()

        # Setting values
        state.melody.cutoff = 5000
        state.drums.kick.amp = 0.8

        # Getting values
        assert state.melody.cutoff == 5000
        assert state.drums.kick.amp == 0.8

        # Should auto-create nested State objects
        assert isinstance(state.melody, State)
        assert isinstance(state.drums, State)
        assert isinstance(state.drums.kick, State)

    def test_mixed_access(self):
        """Test mixing dot notation and dict access."""
        state = State()

        state.melody["cutoff"] = 5000
        state["drums"].kick = 0.8

        assert state["melody"]["cutoff"] == 5000
        assert state.drums["kick"] == 0.8


class TestStateOperations:
    def test_set_method(self):
        """Test the set method for adding multiple parameters."""
        state = State()

        result = state.melody.set(cutoff=5000, amp=0.8, sustain=0.25)

        # Should add to state
        assert state.melody.cutoff == 5000
        assert state.melody.amp == 0.8
        assert state.melody.sustain == 0.25

        # Should return dict with references
        assert result["cutoff"] == 5000
        assert result["amp"] == 0.8
        assert result["sustain"] == 0.25

    def test_init_method(self):
        """Test the init method for setting defaults."""
        state = State()

        # Set initial values
        state.melody.cutoff = 3000

        # Init should not override existing values
        result = state.melody.init(cutoff=5000, amp=0.8)

        assert state.melody.cutoff == 3000  # Unchanged
        assert state.melody.amp == 0.8  # New value

        # Return dict should have current values
        assert result["cutoff"] == 3000
        assert result["amp"] == 0.8

    def test_params_method(self):
        """Test the params method for getting sound parameters."""
        state = State()
        state.reverb.set(
            room=0.5,
            size=0.8,
            amp=0.6,
            n_steps=4,
            p=0.25,
            i=0,  # Timing parameters
        )

        result = state.reverb.params()

        # Should exclude timing parameters
        assert result == {"room": 0.5, "size": 0.8, "amp": 0.6}
        assert "n_steps" not in result
        assert "p" not in result
        assert "i" not in result

    def test_tree_display(self):
        """Test tree display functionality."""
        state = State()
        state.melody.cutoff = 5000
        state.melody.amp = 0.8
        state.drums.kick = 0.5

        tree = state.tree()

        # Should contain all nested structure
        assert "melody" in tree
        assert "cutoff: 5000" in tree
        assert "amp: 0.8" in tree
        assert "drums" in tree
        assert "kick: 0.5" in tree


class TestStateAdvanced:
    def test_nested_dict_conversion(self):
        """Test automatic conversion of nested dicts to State."""
        state = State()

        # Assign a plain dict
        state.config = {"audio": {"sample_rate": 44100, "buffer_size": 512}}

        # Should be converted to State
        assert isinstance(state.config, State)
        assert isinstance(state.config.audio, State)
        assert state.config.audio.sample_rate == 44100

    def test_complex_nesting(self):
        """Test deeply nested state structures."""
        state = State()

        # Create complex nested structure
        state.instruments.synth.oscillator.wave = "saw"
        state.instruments.synth.filter.cutoff = 5000
        state.fx.reverb.room = 0.5

        # Test access
        assert state.instruments.synth.oscillator.wave == "saw"
        assert state.instruments.synth.filter.cutoff == 5000
        assert state.fx.reverb.room == 0.5
