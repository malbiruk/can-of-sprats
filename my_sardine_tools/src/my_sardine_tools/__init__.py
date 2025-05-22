from .playback import SwimGroup, create_player, loop
from .senders import D, ZD_mono, d, zd_mono


class State(dict):
    """
    Dictionary that allows dot notation access to its keys and nested dictionaries.

    Example:
        state = State()
        state.melody.cutoff = 5000
        print(state.melody.cutoff)  # 5000

        # You can also use it like a regular dict
        state['drums'] = {'kick': 0.8}
        print(state.drums.kick)  # 0.8

        # Display structure as a tree
        state.show()
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-convert any existing nested dicts
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, State):
                self[key] = State(value)

    def __getattr__(self, key):
        if key.startswith("_"):
            # For special methods like __copy__, __deepcopy__, etc.
            return super().__getattribute__(key)
        if key not in self:
            # Create nested State on demand
            self[key] = State()
        return self.get(key)

    def __setattr__(self, key, value):
        # Convert nested dicts to State automatically
        if isinstance(value, dict) and not isinstance(value, State):
            value = State(value)
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]

    # For better IDE support
    def __dir__(self):
        return list(self.keys()) + dir(dict)

    def tree(self, depth=None, _prefix="", _last=True, _depth_current=0):
        """
        Display the state structure as a tree.

        Args:
            depth: Maximum depth to display (None for full tree)
            _prefix: Used internally for tree formatting
            _last: Used internally for tree formatting
            _depth_current: Used internally for depth tracking

        Returns:
            String representation of the tree

        Example:
            # Show full tree
            print(state.tree())

            # Show only top-level keys
            print(state.tree(depth=1))

            # Show a subtree
            print(state.drums.tree())
        """
        # Reach maximum depth
        if depth is not None and _depth_current > depth:
            return ""

        result = []
        count = len(self)

        # Handle empty state
        if count == 0:
            if _depth_current == 0:
                return "└── (empty)"
            return ""

        # Generate tree
        for i, (key, value) in enumerate(self.items()):
            is_last = i == count - 1

            # Create branch symbol
            branch = "└── " if is_last else "├── "

            # For terminal values (leaf nodes)
            if not isinstance(value, State) or (depth is not None and _depth_current >= depth):
                result.append(f"{_prefix}{branch}{key}: {value}")
            else:
                # For nested dictionaries (branch nodes)
                result.append(f"{_prefix}{branch}{key}")

                # Set up prefix for children
                if is_last:
                    next_prefix = _prefix + "    "
                else:
                    next_prefix = _prefix + "│   "

                # Recursively format children
                if depth is None or _depth_current < depth:
                    subtree = value.tree(
                        depth=depth,
                        _prefix=next_prefix,
                        _last=is_last,
                        _depth_current=_depth_current + 1,
                    )
                    if subtree:
                        result.append(subtree)

        # Return formatted tree
        return "\n".join(result)

    def show(self, depth=None):
        """
        Print the state structure as a tree.

        Args:
            depth: Maximum depth to display (None for full tree)

        Example:
            state.show()           # Print full tree
            state.drums.show()     # Print drums subtree
            state.show(depth=1)    # Print only top-level keys
        """
        print("\n" + self.tree(depth=depth))

    def __str__(self):
        """String representation shows keys at the current level."""
        keys_list = list(self.keys())
        return f"State({keys_list})"

    def __repr__(self):
        """Repr shows the actual dictionary content."""
        return f"State({super().__repr__()})"
