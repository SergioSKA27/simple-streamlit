from typing import List, Dict, Any, Callable, NoReturn, Union
from abc import ABC, abstractmethod

class Stateful(ABC):

    def __init__(self, *_, **kwargs):
        """
        Initializes the stateful object with optional keyword arguments.
        Args:
            *_: Variable length argument list (not used).
            **kwargs: Arbitrary keyword arguments. Supported keys:
                - key: An optional key to identify the object.
        Attributes:
            key (str or None): An optional key to identify the object.
            editable (bool): Indicates if the object is editable. Default is False.
            strict (bool): Indicates if the object is in strict mode. Default is True.
        """
        self.key = None
        self.editable = False
        self.strict = True
       
        if "key" in kwargs:
            self.key = kwargs["key"]

    @abstractmethod
    def track_state(self):
        """
        Tracks the state of the object.

        This method should be implemented by subclasses to define how the state
        of the object is tracked and managed.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("The track_state method must be implemented")
    
    @abstractmethod
    def set_state(self, state: Any):
        """
        Set the state of the object.

        This method must be implemented by subclasses to define how the state
        should be set.

        Parameters:
        state (Any): The new state to be set.

        Raises:
        NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("The set_state method must be implemented")
      

    def set_key(self, key: str):
        """
        Sets the key for the current instance.

        Args:
            key (str): The key to be set.

        Returns:
            self: The current instance with the updated key.
        """
        self.key = key
        return self
    
    def set_editable(self, editable: bool):
        """
        Set the editable state of the object.

        Args:
            editable (bool): A boolean value indicating whether the object should be editable.

        Returns:
            self: Returns the instance of the object to allow for method chaining.
        """
        self.editable = editable
        return self
    
    def set_strict(self, strict: bool):
        """
        Set the strict mode for the object.

        Parameters:
        strict (bool): If True, the object will operate in strict mode.

        Returns:
        self: Returns the instance of the object to allow for method chaining.
        """
        self.strict = strict
        return self
    
    def set_state(self, state: Any):
        """
        Sets the state of the object.
        Args:
            state (Any): The new state to be set.
        Raises:
            Exception: If the state is not editable.
        """
        if not self.editable:
            raise Exception("The state is not editable")
        
        return self.set_state(state)
    
    def get_key(self):
        """
        Retrieve the key associated with this instance.

        Returns:
            The key associated with this instance.
        """
        return self.key
    
    def get_state(self):
        """
        Retrieve the current state by invoking the track_state method.

        Returns:
            The current state as tracked by the track_state method.
        """
        return self.track_state()
    
    def get_state_tracker(self) -> Callable[[], Any]:
        """
        Returns a callable that tracks the state.

        Returns:
            Callable[[], Any]: A function that, when called, tracks the state.
        """
        return self.track_state
    
        



    

        






