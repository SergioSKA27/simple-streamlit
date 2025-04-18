from typing import List, Dict, Any, Callable, NoReturn, Union, Literal, Optional

from datetime import timedelta
from functools import partial

from simplest.core.build.lstparser import StreamlitLayoutParser
from simplest.core.build.cstparser import StreamlitComponentParser


from ..components.dialog import Dialog





class AppDialog(Dialog):
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

    def __init__(
        self,
        title: str = None,
        width: Literal["large", "small"] = "small",
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
        super().__init__(
            title=title,
            width=width,
            failsafe=failsafe,
            failhandler=failhandler,
            strict=strict,
        )

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

    def add_function(
        self,
        function: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Add a function to the page.
        
        Functions can be either callable functions or pre-configured StreamlitComponentParser instances.
        
        Args:
            function (Callable[..., Any]): The function to add, either as a callable or a parser.
            *args: Variable length argument list to pass to the function.
            **kwargs: Arbitrary keyword arguments to pass to the function.
            
        Returns:
            StreamlitComponentParser: The parser for the added function.
            
        Raises:
            TypeError: If the function is not callable.
        """
        return self._body.add_component(partial(function, *args, **kwargs))

    def __repr__(self) -> str:
        """
        Get a string representation of the app page for debugging.
        
        Returns:
            str: A string representation of the AppPage instance.
        """
        return f"Dialog({self.__str__()})"


    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the app page to a dictionary.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the app page.
        """
        return {
            "__dialog__": self._body.serialize(),
            "__config__": {
                "strict": self.strict,
                "failsafe": self.failsafe
            }
        }

    def __name__(self) -> str:
        """
        Get the name of the app page.
        
        Returns:
            str: The name of the app page.
        """
        return self._name if self._name else self.__class__.__name__