from sardine_core.handlers.player import Player
from sardine_core.run import P, bowl, sleep


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


def loop(*sender_configs: tuple, n_steps: int, p: None | float | str = None) -> float:
    """
    This function creates a temporal loop that plays through multiple steps of a pattern,
    handling the timing/sleep between steps automatically.

    Args:
        *sender_configs: Tuples of (sender_name, kwargs_dict)
        n_steps: Number of steps to play in this cycle
        p: Step duration:
           - None: Use return value from first sender (for variable timing)
           - float: Fixed step duration
           - str: Pattern string to evaluate with P() for variable timing

    Returns:
        Total duration of the loop (for use with again())
    """
    total_duration = 0

    for j in range(n_steps):
        for sender, kwargs in sender_configs:
            call_kwargs = kwargs.copy()
            call_kwargs["i"] = j

            result = sender(**call_kwargs)

            if p is None and result is not None:
                step_duration = result

        if isinstance(p, str):
            step_duration = P(p, i=j)
        elif p is not None:
            step_duration = p

        sleep(step_duration)
        total_duration += step_duration

    return total_duration
