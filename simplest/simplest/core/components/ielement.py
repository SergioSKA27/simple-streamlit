from typing import Dict, Any, Callable, TypeVar, cast
from streamlit import session_state

from ..base.renderable import Renderable
from ..base.stateful import Stateful
from .models.ielement import IElementConfig, BaseComponentConfig, StateKeyConfig

T = TypeVar("T", bound="IElement")  # Type variable for method chaining

class IElement(Renderable, Stateful):
    """
    Base class for all interactive elements.
    e.g. Button, Checkbox, etc.
    
    Attributes:
        key (str): Unique identifier for this component in the session state
        strict (bool): Whether to enforce strict validation
        _base_component (Callable): The underlying Streamlit component
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the IElement instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
            
        Note:
            If 'key' is not provided in kwargs, a unique key will be generated.
            
        Raises:
            ValueError: If validation fails for any parameters.
        """
        # Validate inputs using Pydantic model
        config = IElementConfig(args=args, kwargs=kwargs)
        
        Renderable.__init__(self, *config.args, **config.kwargs)
        Stateful.__init__(self, *config.args, **config.kwargs)

    def _set_base_component(self, base_component: Callable[..., Any]) -> T:
        """
        Sets the base component for this element.

        Args:
            base_component (Callable[..., Any]): The callable component to set.
            
        Returns:
            self: Returns the instance for method chaining.
            
        Raises:
            ValueError: If base_component is not callable.
        """
        # Validate base component using Pydantic model
        config = BaseComponentConfig(component=base_component)
        return super()._set_base_component(config.component)

    def render(self, *args, **kwargs) -> Any:
        """
        Renders the base component with the provided arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the base component's render method.
            
        Raises:
            ValueError: If base_component is not set.
        """
        if not self._base_component:
            raise ValueError("Base component must be set before rendering")
            
        args = args or self.args
        kwargs = kwargs or self.kwargs

        if "key" in kwargs:
            self.set_key(kwargs["key"])
        else:
            if self.is_strict():
                raise ValueError("Key must be provided in strict mode")
            
        return self._base_component(*args, **kwargs)

    def track_state(self) -> Any:
        """
        Tracks the state of the current element using its key.
        
        Returns:
            Any: The state associated with the element's key if it exists in the session state,
                 otherwise None.
                 
        Raises:
            ValueError: If key is invalid or not set.
        """
        # Validate key using Pydantic model
        try:
            config = StateKeyConfig(key=self.key)
        except ValueError:
            raise ValueError("Invalid key: must be a non-empty string")
            
        if config.key not in session_state:
            return None

        return session_state[config.key]

    def set_key(self, key: str) -> T:
        """
        Sets the key for this element.
        
        Args:
            key (str): The key to set.
            
        Returns:
            self: Returns the instance for method chaining.
            
        Raises:
            ValueError: If key is invalid.
        """
        # Validate key using Pydantic model
        config = StateKeyConfig(key=key)
        return super().set_key(config.key)

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the component instance into a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing the serialized component data with the following keys:
                - __component__ (str): The name of the base component class.
                - __args__ (dict): The positional and keyword arguments.
                - __type__ (str): The type of element ('IElement').
        """
        if not self._base_component:
            raise ValueError("Base component must be set before serializing")
            
        return {
            "__component__": self._base_component.__name__,
            "__args__": {
                "args": self.args,
                "kwargs": self.kwargs,
            },
            "__type__": "IElement",
        }
        
    @classmethod
    def deserialize(cls, data: Dict[str, Any], component_map: Dict[str, Callable[..., Any]]) -> 'IElement':
        """
        Deserializes the given data into an IElement instance.
        
        Args:
            data (Dict[str, Any]): The serialized data.
            component_map (Dict[str, Callable[..., Any]]): A mapping of component names to callable objects.
            
        Returns:
            IElement: A new instance populated with the deserialized data.
            
        Raises:
            ValueError: If required fields are missing or invalid.
            KeyError: If component is not found in component_map.
        """
        # Validate required fields
        required_fields = ["__component__", "__args__", "__type__"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field '{field}' in serialized data")
                
        if data["__type__"] != "IElement":
            raise ValueError(f"Expected type 'IElement', got '{data['__type__']}'")
            
        if data["__component__"] not in component_map:
            raise KeyError(f"Component '{data['__component__']}' not found in component map")
        
        # Create instance
        args = data["__args__"].get("args", [])
        kwargs = data["__args__"].get("kwargs", {})
        
        instance = cls(*args, **kwargs)
        instance._set_base_component(component_map[data["__component__"]])
        
        return instance
