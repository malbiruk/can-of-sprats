import re


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
                # Format value based on type
                if isinstance(value, str):
                    formatted_value = f'"{value}"'  # Add quotes for strings
                else:
                    formatted_value = str(value)

                result.append(f"{_prefix}{branch}{key}: {formatted_value}")
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

    def set(self, **kwargs):
        """
        Add multiple key-value pairs to the state and return a dictionary
        with references to these state variables.

        Args:
            **kwargs: Key-value pairs to add to the state

        Example:
            common_args = state.melody.add(midinote=n, sustain=0.25)

        Returns:
            Dictionary with references to state variables
        """
        # Add each key-value pair to the state
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Create a dictionary with references to state variables
        result = {}
        for key in kwargs.keys():
            # Use getattr to get the reference to the state value
            result[key] = getattr(self, key)

        return result

    def delete(self, *keys):
        """
        Delete one or more keys from the state.

        Args:
            *keys: One or more keys to delete from this state object

        Example:
            # Delete a single key
            state.melody.delete('cutoff')

            # Delete multiple keys
            state.melody.delete('amp', 'sustain', 'orbit')

            # Delete an entire branch
            state.delete('melody')

        Returns:
            Self for method chaining
        """
        for key in keys:
            if key in self:
                del self[key]
        return self

    def to_dict(self):
        """
        Convert this state object to a plain dictionary, excluding internal
        attributes and nested State objects.

        Returns:
            Dict containing all regular key-value pairs

        Example:
            params = state.melody.to_dict()  # Get all melody parameters as a dict
        """
        result = {}
        for key, value in self.items():
            if not key.startswith("_") and not isinstance(value, State):
                result[key] = value
        return result

    def init(self, **kwargs):
        """
        Initialize state values only if they don't already exist.

        This is useful for setting default values that won't overwrite
        existing values if they've already been changed.

        Args:
            **kwargs: Key-value pairs to initialize in the state

        Returns:
            Dictionary with references to these state variables

        Example:
            # Set default values that won't override existing ones:
            params = state.melody.init(cutoff=5000, amp=0.05)
        """
        result = {}

        for key, value in kwargs.items():
            # Only set if the key doesn't exist yet
            if key not in self:
                setattr(self, key, value)

            # Always add to result dictionary
            result[key] = getattr(self, key)

        return result

    def skip(self, *keys_to_skip, pattern=None):
        """
        Return a dictionary of values in this state, excluding specified keys
        or keys matching a pattern.

        Args:
            *keys_to_skip: Specific keys to exclude
            pattern: Optional regex pattern to match keys to exclude

        Returns:
            Dictionary with filtered key-value pairs

        Example:
            # Skip specific keys:
            params = state.reverb.skip("n_steps", "p")

            # Skip all keys starting with "_":
            params = state.reverb.skip(pattern="^_")

            # Skip both specific keys and pattern matches:
            params = state.reverb.skip("amp", pattern="^_")
        """
        result = {}
        skip_set = set(keys_to_skip)
        regex = re.compile(pattern) if pattern else None

        for key, value in self.items():
            # Skip internal attributes and State objects
            if key.startswith("_") or isinstance(value, State):
                continue

            # Skip explicitly listed keys
            if key in skip_set:
                continue

            # Skip pattern matches if pattern provided
            if regex and regex.match(key):
                continue

            # Include this key-value pair
            result[key] = value

        return result

    def params(self, *skip_keys, pattern=None):
        """
        Return a dictionary of parameters, excluding common timing parameters
        and any additional specified keys.

        Args:
            *skip_keys: Additional keys to exclude
            pattern: Regex pattern to match keys to skip

        Returns:
            Dictionary with filtered parameters

        Example:
            # Get sound parameters:
            (D, state.reverb.params())

            # Exclude additional parameters:
            (D, state.reverb.params("orbit", "amp"))
        """
        # Common timing/control parameters to exclude
        timing_params = {"n_steps", "p", "i"}
        all_skip_params = set(timing_params) | set(skip_keys)
        return self.skip(*all_skip_params, pattern=pattern)
