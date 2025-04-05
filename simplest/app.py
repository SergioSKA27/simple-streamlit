from typing import List, Dict, Any, Callable, NoReturn, Union, Literal, Optional
from pydantic import BaseModel, Field, field_validator
from simplest.core.components.container import Container
from simplest.core.build.lstparser import StreamlitLayoutParser
from simplest.core.build.cstparser import StreamlitComponentParser
from simplest.core.handlers.layer import Layer
from simplest.core.handlers.schema import Schema

class AppPageConfig(BaseModel):
    """
    Configuration model for AppPage initialization parameters.
    
    Attributes:
        failsafe (bool): Whether to continue execution when errors occur. Default is False.
        failhandler (Optional[Callable[[Exception], Union[NoReturn, bool]]]): 
            A callable that handles exceptions. Default is None.
        strict (bool): Whether to enforce strict type checking. Default is True.
    """
    failsafe: bool = False
    failhandler: Optional[Callable[[Exception], Union[NoReturn, bool]]] = None
    strict: bool = True
    
    @field_validator("failhandler")
    def validate_failhandler(cls, value):
        """Validate that failhandler is callable if provided."""
        if value is not None and not callable(value):
            raise ValueError("failhandler must be callable")
        return value

class AppPage:
    """
    Represents a page in the application with component management capabilities.
    
    This class provides methods to add components and containers to the page,
    manage the page schema, and start the page rendering.
    
    Attributes:
        failsafe (bool): Whether to continue execution when errors occur.
        failhandler (Callable): A callable that handles exceptions.
        strict (bool): Whether to enforce strict type checking.
        _body (Schema): The schema containing the page components.
    """
    _schema = {}  # type: Dict[Union[int, str], List[Callable[..., Any]]]

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
        config = AppPageConfig(
            failsafe=failsafe,
            failhandler=failhandler,
            strict=strict
        )
        
        self.failsafe = config.failsafe
        self.failhandler = config.failhandler
        self.strict = config.strict
        self._body = Schema("__page__")

    def add_component(
        self,
        component: Union[Callable[..., Any], StreamlitComponentParser],
        *args: Any,
        **kwargs: Any,
    ) -> StreamlitComponentParser:
        """
        Add a component to the page.
        
        Components can be either callable functions or pre-configured StreamlitComponentParser instances.
        
        Args:
            component (Union[Callable[..., Any], StreamlitComponentParser]): 
                The component to add, either as a callable or a parser.
            *args: Variable length argument list to pass to the component.
            **kwargs: Arbitrary keyword arguments to pass to the component.
            
        Returns:
            StreamlitComponentParser: The parser for the added component.
            
        Raises:
            TypeError: If the component is not callable.
        """
        if isinstance(component, StreamlitComponentParser):
            component = component.component
            args = component.args
            kwargs = component.kwargs

        if not isinstance(component, Callable):
            raise TypeError(f"Expected a callable, got {type(component)}")
        return self._body.add_component(
            StreamlitComponentParser(component, *args, **kwargs)
        )

    def add_container(
        self,
        container: Union[Callable[..., Any], StreamlitLayoutParser],
        *args: Any,
        **kwargs: Any,
    ) -> StreamlitLayoutParser:
        """
        Add a container to the page.
        
        Containers can be either callable functions or pre-configured StreamlitLayoutParser instances.
        
        Args:
            container (Union[Callable[..., Any], StreamlitLayoutParser]): 
                The container to add, either as a callable or a parser.
            *args: Variable length argument list to pass to the container.
            **kwargs: Arbitrary keyword arguments to pass to the container.
            
        Returns:
            StreamlitLayoutParser: The parser for the added container.
            
        Raises:
            TypeError: If the container is not callable.
        """
        if isinstance(container, StreamlitLayoutParser):
            container = container.container
            args = container.args
            kwargs = container.kwargs

        if not isinstance(container, Callable):
            raise TypeError(f"Expected a callable, got {type(container)}")

        return self._body.add_component(
            StreamlitLayoutParser(container, *args, **kwargs)
        )

    @property
    def main_body(self) -> Layer:
        """
        Get the main body of the app page.
        
        Returns:
            Layer: The main body layer of the page.
        """
        return self._body.main_body
    
    @property
    def schema(self) -> Dict[Union[int, str], List[Callable[..., Any]]]:
        """
        Get the schema of the app page.
        
        Returns:
            Dict[Union[int, str], List[Callable[..., Any]]]: The schema dictionary.
        """
        return self._schema

    def __getitem__(self, key: Union[int, str]):
        """
        Get an item from the schema by key.
        
        Args:
            key (Union[int, str]): The key to lookup in the schema.
            
        Returns:
            Any: The value associated with the key.
            
        Raises:
            KeyError: If the key is not found in the schema.
        """
        return self._schema[key]

    def __str__(self) -> str:
        """
        Get a string representation of the app page.
        
        Returns:
            str: A string representation of the schema.
        """
        return str(self._schema)

    def __repr__(self) -> str:
        """
        Get a string representation of the app page for debugging.
        
        Returns:
            str: A string representation of the AppPage instance.
        """
        return f"AppPage({self._schema})"

    def start(self):
        """
        Start the app page by rendering all components in the main body schema.
        
        Returns:
            self: The AppPage instance for method chaining.
        """
        self._body()
        return self

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the app page to a dictionary.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the app page.
        """
        return {
            "body": self._body.serialize(),
            "failsafe": self.failsafe,
            "strict": self.strict
        }
