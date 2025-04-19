from typing import List, Dict, Any, Callable, NoReturn, Union, TypeVar,cast
from abc import ABCMeta, abstractmethod
from ...core.build.lstparser import StreamlitLayoutParser
from ...core.build.cstparser import StreamlitComponentParser
from ...core.handlers.layer import Layer
from ...core.handlers.schema import Schema
from .models.canvas import CanvasConfig


T = TypeVar("T", bound="Canvas")

class Canvas(metaclass=ABCMeta):
    """
    Represents a canvas in the application with component management capabilities.
    """

    def __init__(
        self,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ):
        """
        Initialize a new AppPage instance.
        
        Args:
            failsafe (bool): Whether to continue execution when errors occur. Default is False.
            failhandler (Callable[[Exception], Union[NoReturn, bool]], optional): 
                A callable that handles exceptions. Default is None.
            strict (bool): Whether to enforce strict type checking. Default is True.
        
        Raises:
            ValueError: If failhandler is provided but is not callable.
        """
        # Validate inputs using the Pydantic model
        config = CanvasConfig(
            failsafe=failsafe,
            failhandler=failhandler,
            strict=strict
        )
        
        self.failsafe = config.failsafe
        self.failhandler = config.failhandler
        self.strict = config.strict
        self._body = Schema("__body__")

    @abstractmethod
    def add_component(
        self,
        component: Union[Callable[..., Any], StreamlitComponentParser],
        *args: Any,
        **kwargs: Any,
    ) -> StreamlitComponentParser:
        """
        Add a component to the page.
        
        Components can be either callable functions or pre-configured StreamlitComponentParser instances.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("add_component method must be implemented")

    @abstractmethod
    def add_container(
        self,
        container: Union[Callable[..., Any], StreamlitLayoutParser],
        *args: Any,
        **kwargs: Any,
    ) -> StreamlitLayoutParser:
        """
        Add a container to the page.
        
        Containers can be either callable functions or pre-configured StreamlitLayoutParser instances.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("add_container method must be implemented")
        

    @property
    def main_body(self) -> Layer:
        """
        Get the main body of the app page.
        
        Returns:
            Layer: The main body layer of the page.
        """
        return self._body.main_body
    
    def set_failsafe(self, failsafe: bool) -> T:
        """
        Set the failsafe mode for the canvas.
        
        Args:
            failsafe (bool): Whether to enable failsafe mode.
            
        Returns:
            T: The current instance of the canvas.
        """
        self.failsafe = failsafe
        return cast(T, self)

    def set_failhandler(
        self, failhandler: Callable[[Exception], Union[NoReturn, bool]]
    ) -> T:
        """
        Set the failhandler for the canvas.

        args:
            failhandler (Callable[[Exception], Union[NoReturn, bool]]): A callable to handle exceptions.
        
        Returns:
            T: The current instance of the canvas.
        """
        if not callable(failhandler):
            raise ValueError("failhandler must be callable")
        self.failhandler = failhandler
        return cast(T, self)
    
    def set_strict(self, strict: bool) -> T:
        """
        Set the strict mode for the canvas.
        
        Args:
            strict (bool): Whether to enable strict mode.
            
        Returns:
            T: The current instance of the canvas.
        """
        self.strict = strict
        return cast(T, self)
    

    def __getitem__(self, key: Union[int, str]) -> Union[StreamlitComponentParser, StreamlitLayoutParser]:
        """
        Get an item from the schema by key.
        
        Args:
            key (Union[int, str]): The key to lookup in the schema.
            
        Returns:
            Any: The value associated with the key.
            
        Raises:
            KeyError: If the key is not found in the schema.
        """
        try:
            return self.main_body[key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found in canvas schema")

    def __str__(self) -> str:
        """
        Get a string representation of the app page.
        
        Returns:
            str: A string representation of the schema.
        """
        return str(self.main_body)

    def __repr__(self) -> str:
        """
        Get a string representation of the app page for debugging.
        
        Returns:
            str: A string representation of the AppPage instance.
        """
        return f"AppPage({self.main_body})"

    def __call__(self):
        """
        Call the start method to execute the main body of the app page.
        """
        return self.start()

    @abstractmethod
    def start(self) -> T:
        """
        Call all the components in the main body of the app page.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("start method must be implemented")        
        
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the app page to a dictionary.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the app page.
        """
        pass





