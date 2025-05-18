from functools import wraps

from sardine_core.handlers.player import Player
from sardine_core.run import D as original_D
from sardine_core.run import bowl
from sardine_core.run import d as original_d


def create_player(name: str) -> Player:
    """
    Custom function to create simple players like Pa, Pb, Pc, etc.
    without @swim decorator
    """
    # don't create a new player if it's already being used
    if name in [i.name for i in bowl.scheduler.runners]:
        return next(
            (obj for obj in bowl.handlers if hasattr(obj, "name") and obj.name == name),
            None,
        )
    p = Player(name=name)
    bowl.add_handler(p)
    return p


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
        # If first arg is a string (the most common case)
        if args:
            instrument = args[0]
            args = (f"{instrument} ^| [{instrument} ^| [{note_pattern}]]",) + args[1:]

    # Pass through to original d
    return original_D(*args, **kwargs)


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
