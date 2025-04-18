from typing import List, Dict, Any, Callable, NoReturn, Union, Literal, Optional

from functools import partial
from streamlit import set_page_config
from pydantic import BaseModel, Field

from ...core.build.lstparser import StreamlitLayoutParser
from ...core.build.cstparser import StreamlitComponentParser

from ..components.canvas import Canvas
from ..components.fragment import Fragment


class StreamlitPageConfig(BaseModel):
    """
    Configuration model for Streamlit page settings.
    
    Attributes:
        title (str): The title of the Streamlit app. Default is "Streamlit App".
        layout (Literal["centered", "wide"]): The layout of the Streamlit app. Default is "centered".
        initial_sidebar_state (Literal["auto", "expanded", "collapsed"]): 
            The initial state of the sidebar. Default is "auto".
    """
    title: str = Field(default="Streamlit App")
    layout: Literal["centered", "wide"] = Field(default="centered")
    initial_sidebar_state: Literal["auto", "expanded", "collapsed"] = Field(default="auto")
    page_icon: Optional[str] = Field(default=None)



class AppPage(Canvas):
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
            failsafe=failsafe,
            failhandler=failhandler,
            strict=strict
        )
    
    def add_fragment(
        self,
        fragment: Union[Callable[..., Any], Fragment],
    ) -> Fragment:
        """
        Add a fragment to the page.
        
        Fragments can be either callable functions or pre-configured Fragment instances.
        
        Args:
            fragment (Union[Callable[..., Any], Fragment]): 
                The fragment to add, either as a callable or a Fragment instance.
            
        Returns:
            Fragment: The added fragment instance.
            
        Raises:
            TypeError: If the fragment is not callable.
        """
        return self._body.add_component(
            fragment
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

    
    def start(self):
        """
        Start the app page by rendering all components in the main body schema.
        
        Returns:
            self: The AppPage instance for method chaining.
        """
        self._body()
        return self


    def __repr__(self) -> str:
        """
        Get a string representation of the app page for debugging.
        
        Returns:
            str: A string representation of the AppPage instance.
        """
        return f"AppPage({self.__str__()})"


    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the app page to a dictionary.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the app page.
        """
        return {
            "__page__": self._body.serialize(),
            "__config__": {
                "strict": self.strict,
                "failsafe": self.failsafe
            }
        }


    @staticmethod
    def set_page_config(
        title: str = "Streamlit App",
        layout: Literal["centered", "wide"] = "centered",
        initial_sidebar_state: Literal["auto", "expanded", "collapsed"] = "auto",
        page_icon: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Set the configuration for the Streamlit page.
        
        Args:
            title (str): The title of the Streamlit app. Default is "Streamlit App".
            layout (Literal["centered", "wide"]): The layout of the Streamlit app. Default is "centered".
            initial_sidebar_state (Literal["auto", "expanded", "collapsed"]): 
                The initial state of the sidebar. Default is "auto".
            page_icon (Optional[str]): The icon for the page. Default is None.
        """
        # Validate inputs using the Pydantic model
        config = StreamlitPageConfig(
            title=title,
            layout=layout,
            initial_sidebar_state=initial_sidebar_state,
            page_icon=page_icon
        )
        set_page_config(
            page_title=config.title,
            layout=config.layout,
            initial_sidebar_state=config.initial_sidebar_state,
            page_icon=config.page_icon,
            **kwargs
        )