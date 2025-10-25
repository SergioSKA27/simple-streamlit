from typing import Any
from abc import ABCMeta, abstractmethod
from ...base.components.canvas import Canvas



class Builder(metaclass=ABCMeta):



    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initialize the builder with the given arguments and keyword arguments.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.args = args
        self.kwargs = kwargs
    
    @abstractmethod
    def create_canvas(self, *args: Any, **kwargs: Any) -> Canvas:
        """
        Abstract method to create a canvas.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Canvas: An instance of the Canvas class.
        """
        pass

    
        