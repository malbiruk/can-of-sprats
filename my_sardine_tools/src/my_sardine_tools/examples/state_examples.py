"""
Examples demonstrating the power of the State system in my_sardine_tools.

This module contains practical examples that show how to use the State class
for live coding, parameter control, and creating dynamic effects.
"""


def simple_parameter_changes():
    """Example: Simple parameter changes"""
    # Create a state (normally you'd use an existing one)
    from my_sardine_tools import State

    state = State()

    # Immediate parameter changes
    state.melody.saw.cutoff = 2000
    state.melody.fx.shape = 0.8
    state.reverb.room = 0.9

    # Modify parameters for groups of instruments
    for drum in ["hh", "sn1"]:
        state.drums[drum].fx.hpf = 3000

    return state  # For interactive exploration


def create_lfo():
    """Example: Creating LFOs for parameter modulation"""
    import math

    from sardine_core.run import again, swim

    from my_sardine_tools import State

    state = State()

    # Cutoff LFO - sweeps filter cutoff over time
    def cutoff_lfo(p=0.01, i=0):
        cycle = (i * p) % 8 / 8  # 8-beat cycle
        value = 1000 + 7000 * (0.5 + 0.5 * math.sin(cycle * 2 * math.pi))
        state.melody.saw.cutoff = value
        again(cutoff_lfo_runner, p=p, i=i + 1)

    cutoff_lfo_runner = swim(cutoff_lfo)

    # To stop: cutoff_lfo_runner.stop()
    return state, cutoff_lfo_runner


def create_transitions():
    """Example: Creating transitions between parameter values"""
    from sardine_core.run import again, swim

    from my_sardine_tools import State

    state = State()

    # Fade in melody
    def fade_in(duration=8):
        def fade(p=0.1, i=0):
            if i < 16:
                progress = i / 16
                state.melody.amp = progress * 0.05
                again(fade_runner, p=duration / 16, i=i + 1)

        fade_runner = swim(fade)
        return fade_runner

    # Use it: fade_runner = fade_in(4)  # 4-beat fade in
    return state, fade_in


def global_intensity_control():
    """Example: Control multiple parameters together"""
    from my_sardine_tools import State

    state = State()

    def set_intensity(level=0.5):  # 0.0 to 1.0
        # Melody intensity
        state.melody.fx.shape = 0.3 + 0.6 * level
        state.melody.saw.cutoff = 1000 + 7000 * level

        # Drums intensity
        for drum in ["hh", "sn1"]:
            if hasattr(state.drums, drum):
                state.drums[drum].amp = 0.3 + 0.5 * level

        # Bass intensity
        state.bass.fx.lpf = 100 + 400 * level
        state.bass.amp = 0.1 + 0.3 * level

        # Reverb space
        state.reverb.room = 0.3 + 0.6 * level
        state.reverb.size = 0.5 + 0.4 * level

    # Use it: set_intensity(0.8)  # Bright, energetic sound
    return state, set_intensity


if __name__ == "__main__":
    # This section runs if you execute this file directly
    print("State Examples")
    print("=============")
    print("This module contains examples for using the State class.")
    print("Import and use the functions to see them in action.")
    print("\nAvailable examples:")
    print("  - simple_parameter_changes()")
    print("  - create_lfo()")
    print("  - create_transitions()")
    print("  - global_intensity_control()")
