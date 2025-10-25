from typing import Any, Callable, Union
from streamlit import session_state

class SessionState:
    def __init__(self, key: str, initial_value: Any = None):
        """
        Initialize the SessionState object.
        
        Args:
            key (str): The key for the session state.
            initial_value (Any): The initial value for the session state.
        """
        self.key = key
        self.__set_new_session_state(initial_value)

    @property
    def value(self) -> Any:
        """
        Get the current session state value.
        
        Returns:
            Any: The current value of the session state.
        """
        return self.__get_session_state()
    
    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Set a new session state value.
        
        Args:
            new_value (Any): The new value to set for the session state.
        """
        self.__update_session_state(new_value)

    def get_setter(self) -> Callable:
        """
        Get a setter for the session state value.
        
        Returns:
            Callable: A callable that sets the session state value.
        """
        return self.__setter_factory()
    
    def get_tracker(self) -> Callable:
        """
        Get a tracker for the session state value.
        
        Returns:
            Callable: A callable that tracks the session state value.
        """
        return self.__tracker_factory()

    def set_value(self, value: Any) -> None:
        """
        Set a new session state value.
        
        Args:
            value (Any): The new value to set for the session state.
        """
        self.__update_session_state(value)

    def __set_new_session_state(self, value: Any) -> None:
        """
        Set a new session state value.
        
        Args:
            value (Any): The new value to set for the session state.
        """
        if self.key not in session_state:
            session_state[self.key] = value
    
    def __get_session_state(self) -> Any:
        """
        Get the current session state value.
        
        Returns:
            Any: The current value of the session state.
        """
        return session_state[self.key]

    def __update_session_state(self, value: Any) -> None:
        """
        Update the session state value.
        
        Args:
            value (Any): The new value to set for the session state.
        """
        session_state[self.key] = value

    def __setter_factory(self):
        """
        Create a setter for the session state value.
        
        Returns:
            Callable: A callable that sets the session state value.
        """
        def setter(value: Any) -> Any:
            session_state[self.key] = value
            return session_state[self.key]
        return setter
    
    def __tracker_factory(self) -> Callable:
        """
        Create a tracker for the session state value.
        
        Returns:
            Callable: A callable that tracks the session state value.
        """
        def tracker() -> Any:
            return session_state[self.key]
        return tracker
    
    def __repr__(self) -> str:
        """
        Get a string representation of the SessionState object.
        
        Returns:
            str: A string representation of the SessionState object.
        """
        return f"SessionState(key={self.key}, value={self.value})"

    @classmethod
    def get(cls, key: str) -> Any:
        """
        Get the session state value for a given key.
        
        Args:
            key (str): The key for the session state.
            
        Returns:
            Any: The current value of the session state.
        """
        if key not in session_state:
            raise KeyError(f"Session state key '{key}' not found")
        return session_state[key]
