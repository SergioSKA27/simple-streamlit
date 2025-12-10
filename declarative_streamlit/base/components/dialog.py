from typing import Callable, Union, NoReturn, Literal
from abc import ABCMeta
from streamlit import dialog
from .canvas import Canvas


class Dialog(Canvas,metaclass=ABCMeta):
    """
    Fragment class that extends the Canvas class.
    
    This class is used to create a fragment of a canvas, allowing for more granular control over the layout and components.
    """
    def __init__(
        self,
        title: str,
        width: Literal["large", "small"] = "small",
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ):
        """
        Initialize a new Fragment instance.
        
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
        self._title = title
        self._width = width

    def __render_on_dialog(self):
        """
        Render the fragment on the canvas.
        
        This method is responsible for rendering the fragment on the canvas.
        It should be called when the fragment is ready to be displayed.
        """
        
        @dialog(title=self._title, width=self._width)
        def render():
            self._body()
        
        return render()
    
    def __call__(self,*args, **kwargs):
        """
        Call the dialog with the provided arguments.
        """
        return self.start()
        
    
    def start(self,*args, **kwargs):
        """
        Start the dialog rendering process.
        """
        self.__render_on_dialog()
        

        
        