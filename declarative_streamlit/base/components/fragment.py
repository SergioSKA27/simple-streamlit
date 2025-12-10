from typing import Callable, Union, NoReturn
from abc import ABCMeta
from datetime import timedelta
from streamlit import fragment
from .canvas import Canvas


class Fragment(Canvas,metaclass=ABCMeta):
    """
    Fragment class that extends the Canvas class.
    
    This class is used to create a fragment of a canvas, allowing for more granular control over the layout and components.
    """
    def __init__(
        self,
        failsafe: bool = False,
        failhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
        run_every: Union[int, float,timedelta,str,None] = None,
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
        self.run_every = run_every

    def __render_on_fragment(self):
        """
        Render the fragment on the canvas.
        
        This method is responsible for rendering the fragment on the canvas.
        It should be called when the fragment is ready to be displayed.
        """
        
        @fragment(run_every=self.run_every)
        def render():
            self._body()
        
        return render()
    
        
    
    def start(self):
        """
        Start the fragment rendering process.
        
        This method is responsible for starting the rendering process of the fragment.
        It should be called when the fragment is ready to be displayed.
        """
        self.__render_on_fragment()

        
        