# my_sardine_tools

This is my personal collection of tools for making Sardine life easier. Think of it as a set of shortcuts and helpers that I've built up over time.

## What's Inside?

*   **Playback Utilities:** Functions to simplify pattern creation and playback.
    *   `create_player()`: Create simple players without using the `@swim` decorator (same as Pa, Pb, Pc... but with custom names)
    *   `loop()`: Create temporal loops with automatic timing management
    *   `start()/stop()`: Easily manage multiple Sardine functions
*   **State Management:** Organized parameter handling for complex compositions. This is nice for organization and allows to modify the parameters via the global scope.
    *   `State()`: Hierarchical state management with automatic parameter organization
    *   Dynamic attribute creation for nested parameter groups
*   **Enhanced Senders:** Improved MIDI and audio routing.
    *   `D`, `d`: Enhanced SuperDirt senders with additional features (real pauses for patterns specified in `n`/`midinote`)
    *   `ZD_mono`, `zd_mono`: Enhanced Ziffers senders with sustain depending on note lengths

## Installation

From the project root:

```bash
pip install -e ./my_sardine_tools
```

## Some features

### Creating Players

```python
from my_sardine_tools import create_player

# Create simple players without @swim decorator
a = create_player("a")
b = create_player("b")

# Use them in patterns
a("bd")
b("sn", amp=0.8)
```

### Managing Functions

```python
from my_sardine_tools import start, stop

# I don't use @swim decorator with @ syntaxis, it goes like this:
def function1(p=1, i=0):
    # some sender or other things
    again(swim(function1), p=p, i=i + 1)


# Start multiple functions at once
start(function1, function2, function3)

# Stop them later
stop(function1, function2, function3)

# Or manage groups of functions
my_funcs = [kick_pattern, bass_pattern, melody]
start(my_funcs)
stop(my_funcs)

# Pass additional arguments to swim
start(my_function, quant=0.5)
```

### Creating Loops

```python
from my_sardine_tools import loop, D

def pattern(p=1, i=0):
    # Define pattern with multiple senders
    duration = loop(
        (D, {"sound": "bd", "amp": 0.8}),
        (D, {"sound": "sn", "amp": 0.6}),
        n_steps=8,
        p=0.25  # Fixed step duration
    )
    again(swim(pattern), p=duration, i=i + 1)

def variable_timing(p=1, i=0):
    # Use pattern strings for variable timing
    duration = loop(
        (D, {"sound": "hh", "amp": 0.4}),
        n_steps=4,
        p="1 0.5 0.25 0.75"  # Variable step durations
    )
    again(variable_timing, p=duration, i=i+1)
```

### State Management

```python
from my_sardine_tools import State, D

state = State()

def kick_pattern(p=1, i=0):
    # Initialize state parameters
    state.drums.kick.init(
        n_steps=4,
        sound="bd",
        amp=0.8,
        orbit=0
    )

    # Initialize effects
    state.drums.kick.fx.init(
        lpf=800,
        shape=0.5,
        room=0.2
    )

    # Use in loop
    duration = loop(
        (D, state.drums.kick.fx | state.drums.kick.params()),
        n_steps=state.drums.kick.n_steps,
        p=state.drums.kick.p
    )
    again(kick_pattern, p=duration, i=i+1)
```

### Enhanced Senders

```python
from my_sardine_tools import D, ZD_mono

# Use enhanced SuperDirt sender -- makes . in n/midinote an actual pause
D("superpiano", n="E3 . E3 C4 . F3 . A3", amp=0.8, room=0.3, i=i)

# Monophonic ZD patterns -- makes sustain depend on note length (tweak with coef parameter)
ZD_mono("superpiano", "h 0 2 4", coef=0.75)
```

## Examples Directory

See `src/my_sardine_tools/examples/` for additional usage examples and patterns.

## Requirements

*   Python 3.10+
*   sardine-system

## License

This package is designed to work with Sardine and follows the same open-source principles.
