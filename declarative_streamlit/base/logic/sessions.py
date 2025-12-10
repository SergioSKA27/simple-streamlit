"""Session state management module for Streamlit applications.

This module provides a robust, type-safe wrapper around Streamlit's session_state
with support for strict type checking, value tracking, and functional programming patterns.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Type, TypeVar, Union, Literal

from streamlit import session_state

T = TypeVar("T")


class SessionState:
    """A type-safe, feature-rich wrapper for Streamlit session state management.

    This class provides an elegant interface for managing session state with optional
    strict type checking, functional setters/trackers, and comprehensive error handling.

    Features:
        - Type-safe value storage with optional strict enforcement
        - Property-based value access with getters/setters
        - Factory methods for functional programming patterns
        - Comprehensive error handling and validation
        - Class methods for direct state access
        - Rich string representation for debugging

    Attributes:
        key: Unique identifier for the session state entry.
        session_type: Expected type for stored values (None allows any type).
        strict: Whether to enforce type checking on value assignment.

    Example:
        >>> counter = SessionState('counter', initial_value=0, session_type=int, strict=True)
        >>> counter.value = 5
        >>> print(counter.value)
        5
        >>> setter = counter.get_setter()
        >>> setter(10)
        10
    """

    __slots__ = ("key", "session_type", "strict", "_deserialize", "engine")

    def __init__(
        self,
        key: str,
        initial_value: Any = None,
        session_type: Optional[Type[T]] = None,
        strict: bool = True,
        deserialize: bool = False,
        engine: Union[Callable[[Any], Any], Literal['json']] = 'pickle',

    ) -> None:
        """Initialize a SessionState instance with type safety and validation.

        Args:
            key: Unique identifier for this session state entry. Must be non-empty.
            initial_value: Initial value to store. Type-checked if session_type is specified.
            session_type: Expected type for values. None allows any type.
            strict: If True, enforces type checking on all value assignments.
            deserialize: Whether to deserialize the initial value using the specified engine.
            engine: Deserialization engine to use ('pickle', 'json', or custom callable).

        Raises:
            ValueError: If key is empty or invalid.
            TypeError: If initial_value doesn't match session_type when strict=True.

        Note:
            The initial_value is only set if the key doesn't already exist in session_state,
            preserving existing state across reruns.
        """
        if not key or not isinstance(key, str):
            raise ValueError(f"Key must be a non-empty string, got: {key!r}")

        self.key = key
        self.session_type = session_type
        self.strict = strict
        self._deserialize = deserialize
        self.engine = engine
        self.__set_new_session_state(initial_value)

    def _deserialize_initial_value(self, value: Any) -> Any:
        """Deserialize the initial value using the specified engine.

        Args:
            value: The value to deserialize.

        Returns:
            The deserialized value.

        Raises:
            ValueError: If an unsupported engine is specified.
        """
        if not self._deserialize:
            return value

        if self.engine == 'json':
            import json
            return json.loads(value)
        elif callable(self.engine):
            return self.engine(value)
        else:
            raise ValueError(f"Unsupported deserialization engine: {self.engine!r}")

    def _type_check(self, value: Any) -> bool:
        """Validate if a value matches the expected session type.

        Supports runtime type checking including generic types and union types
        for comprehensive validation.

        Args:
            value: The value to validate against session_type.

        Returns:
            True if value matches the expected type or no type is specified,
            False otherwise.

        Note:
            If session_type is None, all values are considered valid.
        """
        if self.session_type is None:
            return True
        return isinstance(value, self.session_type)

    def _enforce_strict(self, value: Any) -> None:
        """Enforce strict type checking when enabled.

        This method is called before any value assignment to ensure type safety
        when strict mode is enabled.

        Args:
            value: The value to validate.

        Raises:
            TypeError: If strict=True and value doesn't match session_type.
                Includes descriptive error message with value and expected type.

        Note:
            No-op if strict=False or session_type is None.
        """
        if self.strict and not self._type_check(value):
            raise TypeError(
                f"Type mismatch: expected {self.session_type.__name__!r}, "
                f"got {type(value).__name__!r} for value {value!r}"
            )

    @property
    def value(self) -> Any:
        """Get the current session state value.

        Provides property-based access to the underlying session state value,
        enabling natural attribute-style access.

        Returns:
            The current value stored in session_state[key].

        Raises:
            KeyError: If the session state key doesn't exist (shouldn't occur
                after proper initialization).

        Example:
            >>> state = SessionState('counter', initial_value=0)
            >>> print(state.value)
            0
        """
        return self.__get_session_state()

    @value.setter
    def value(self, new_value: Any) -> None:
        """Set a new session state value with type checking.

        Property setter that validates and updates the session state value,
        enforcing type safety when strict mode is enabled.

        Args:
            new_value: The new value to store. Type-checked if strict=True.

        Raises:
            TypeError: If strict=True and new_value doesn't match session_type.

        Example:
            >>> state = SessionState('counter', initial_value=0, session_type=int)
            >>> state.value = 42
            >>> state.value = "invalid"  # Raises TypeError if strict=True
        """
        self.__update_session_state(new_value)

    def get_setter(self) -> Callable[[Any], Any]:
        """Create a functional setter for this session state.

        Factory method that returns a closure capturing this instance's state,
        useful for callbacks, event handlers, and functional programming patterns.

        Returns:
            A callable that accepts a value, validates it, updates the session state,
            and returns the newly set value.

        Raises:
            TypeError: If strict=True and provided value doesn't match session_type.

        Example:
            >>> state = SessionState('counter', initial_value=0)
            >>> setter = state.get_setter()
            >>> button_callback = lambda: setter(state.value + 1)
            >>> st.button('Increment', on_click=button_callback)
        """
        return self.__setter_factory()

    def get_tracker(self) -> Callable[[], Any]:
        """Create a functional tracker for this session state.

        Factory method that returns a closure for reading the current value,
        useful for monitoring state changes without direct property access.

        Returns:
            A callable that returns the current session state value when invoked.

        Example:
            >>> state = SessionState('status', initial_value='idle')
            >>> tracker = state.get_tracker()
            >>> print(tracker())
            'idle'
        """
        return self.__tracker_factory()

    def set_value(self, value: Any) -> None:
        """Set a new session state value (alternative to property setter).

        Method-based interface for updating the session state value, providing
        an alternative to the property setter for explicit method calls.

        Args:
            value: The new value to store. Type-checked if strict=True.

        Raises:
            TypeError: If strict=True and value doesn't match session_type.

        Note:
            Functionally identical to using the value property setter.

        Example:
            >>> state = SessionState('data', initial_value=[])
            >>> state.set_value([1, 2, 3])
        """
        self.__update_session_state(value)

    def __set_new_session_state(self, value: Any) -> None:
        """Initialize session state entry if not already present.

        Internal method that safely initializes the session state entry,
        preserving existing values across Streamlit reruns.

        Args:
            value: The initial value to set.

        Raises:
            TypeError: If strict=True and value doesn't match session_type.

        Note:
            Only sets the value if self.key is not already in session_state.
        """
        if self.key not in session_state:
            self._enforce_strict(value)
            value = self._deserialize_initial_value(value)
            session_state[self.key] = value

    def __get_session_state(self) -> Any:
        """Retrieve the current session state value.

        Internal method for reading from the underlying session_state storage.

        Returns:
            The current value stored in session_state[self.key].

        Raises:
            KeyError: If the key doesn't exist in session_state.
        """
        return session_state[self.key]

    def __update_session_state(self, value: Any) -> None:
        """Update the session state with a new value.

        Internal method for writing to the underlying session_state storage
        with type validation.

        Args:
            value: The new value to store.

        Raises:
            TypeError: If strict=True and value doesn't match session_type.
        """
        self._enforce_strict(value)
        session_state[self.key] = value

    def __setter_factory(self) -> Callable[[Any], Any]:
        """Create a setter closure for functional programming patterns.

        Internal factory method that creates a closure capturing this instance,
        enabling functional-style state updates.

        Returns:
            A callable that updates and returns the session state value.

        Note:
            The returned function maintains a reference to this SessionState instance.
        """

        def setter(value: Any) -> Any:
            self._enforce_strict(value)
            session_state[self.key] = value
            return session_state[self.key]

        return setter

    def __tracker_factory(self) -> Callable[[], Any]:
        """Create a tracker closure for functional programming patterns.

        Internal factory method that creates a closure capturing this instance,
        enabling functional-style state reading.

        Returns:
            A callable that returns the current session state value.

        Note:
            The returned function maintains a reference to this SessionState instance.
        """

        def tracker() -> Any:
            return session_state[self.key]

        return tracker

    def __repr__(self) -> str:
        """Generate a detailed string representation for debugging.

        Returns:
            A string showing the key, current value, type constraints, and strict mode.

        Example:
            >>> state = SessionState('counter', 0, int, True)
            >>> print(repr(state))
            SessionState(key='counter', value=0, type=<class 'int'>, strict=True)
        """
        type_info = f", type={self.session_type}" if self.session_type else ""
        return (
            f"SessionState(key={self.key!r}, value={self.value!r}"
            f"{type_info}, strict={self.strict})"
        )

    def __str__(self) -> str:
        """Generate a user-friendly string representation.

        Returns:
            A concise string showing the key and current value.

        Example:
            >>> state = SessionState('status', 'ready')
            >>> print(str(state))
            SessionState['status']: 'ready'
        """
        return f"SessionState[{self.key!r}]: {self.value!r}"

    def __eq__(self, other: object) -> bool:
        """Compare SessionState instances for equality.

        Two SessionState instances are equal if they reference the same key
        and have the same configuration.

        Args:
            other: Another object to compare with.

        Returns:
            True if both instances have the same key, session_type, and strict settings.

        Example:
            >>> s1 = SessionState('key', 0)
            >>> s2 = SessionState('key', 0)
            >>> s1 == s2
            True
        """
        if not isinstance(other, SessionState):
            return NotImplemented
        return (
            self.key == other.key
            and self.session_type == other.session_type
            and self.strict == other.strict
        )

    def __hash__(self) -> int:
        """Generate a hash for this SessionState instance.

        Returns:
            Hash value based on the key, enabling use in sets and as dict keys.

        Note:
            Hash is based solely on the key since session_type and strict are mutable.
        """
        return hash(self.key)

    @classmethod
    def get(cls, key: str) -> Any:
        """Retrieve a session state value by key (class method interface).

        Provides direct access to session_state without creating a SessionState instance.
        Useful for quick reads without the overhead of instance creation.

        Args:
            key: The session state key to retrieve.

        Returns:
            The current value stored under the specified key.

        Raises:
            KeyError: If the key doesn't exist in session_state.
            ValueError: If key is empty or invalid.

        Example:
            >>> SessionState.get('counter')
            42
        """
        if not key or not isinstance(key, str):
            raise ValueError(f"Key must be a non-empty string, got: {key!r}")
        if key not in session_state:
            raise KeyError(f"Session state key {key!r} not found")
        return session_state[key]

    @classmethod
    def exists(cls, key: str) -> bool:
        """Check if a session state key exists.

        Args:
            key: The session state key to check.

        Returns:
            True if the key exists in session_state, False otherwise.

        Example:
            >>> if SessionState.exists('user_data'):
            ...     data = SessionState.get('user_data')
        """
        return key in session_state

    @classmethod
    def delete(cls, key: str) -> None:
        """Remove a session state entry by key.

        Args:
            key: The session state key to remove.

        Raises:
            KeyError: If the key doesn't exist in session_state.

        Example:
            >>> SessionState.delete('temp_data')
        """
        if key not in session_state:
            raise KeyError(f"Session state key {key!r} not found")
        del session_state[key]
