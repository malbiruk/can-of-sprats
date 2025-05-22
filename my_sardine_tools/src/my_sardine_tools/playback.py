from sardine_core.handlers.player import Player
from sardine_core.run import P, bowl, sleep, swim


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


class SwimGroup:
    """Group for managing multiple swimmers with support for variable references."""

    def __init__(self, name="group"):
        self.name = name
        self.runners = {}  # name: runner mapping

    def stop(self):
        """Stop all swimmers in the group."""
        for runner in self.runners.values():
            if runner:
                runner.stop()
        return self

    def start(self, var_func_map):
        """
        Start multiple swim functions and store their runners.
        This will update the variables in the calling scope.

        Args:
            var_func_map: Dictionary mapping variable names to functions
                         {"var_name": swim_function}
        """
        import inspect

        caller_globals = inspect.currentframe().f_back.f_globals

        for var_name, func in var_func_map.items():
            # Start the swimmer
            runner = swim(func)

            # Store in our group
            self.runners[var_name] = runner

            # Update the global variable in the caller's scope
            caller_globals[var_name] = runner

        return self
