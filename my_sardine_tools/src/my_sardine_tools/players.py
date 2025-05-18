from sardine_core.handlers.player import Player
from sardine_core.run import bowl


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
