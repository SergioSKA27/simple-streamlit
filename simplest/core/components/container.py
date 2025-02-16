from typing import List, Dict, Any, Callable, NoReturn, Union, Literal
from ..base.renderable import Renderable
from ..base.layoutable import Layoutable

class Container(Renderable, Layoutable):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the container component.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            _base_component (Callable[..., Any]): The base component of the container.
            _top_render (bool): Flag indicating if this is the top render.
        """
        Renderable.__init__(self, *args, **kwargs)
        Layoutable.__init__(self)
        self._base_component = None  # type: Callable[..., Any]
        self._top_render = False  # type: bool

    def render(self, *args, **kwargs):
        """
        Renders the base component with the provided arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.lrender(self._base_component, *args, **kwargs)

    # override the __str__ method
    def __str__(self):
        """
        Return a string representation of the Container object.

        The string representation includes the name of the base component and the layers of the container.

        Returns:
            str: A string in the format "Container(<base_component_name>): <layers>".
        """
        return f"Container({self._base_component.__name__}): {self.layers}"
    
    def serialize(self):
        """
        Serializes the container object into a dictionary format.
        Returns:
            dict: A dictionary containing the serialized data of the container object, including:
                - component (str): The name of the base component.
                - args (list): The positional arguments of the container.
                - kwargs (dict): The keyword arguments of the container.
                - fatal (bool): Indicates if the container is fatal.
                - top_render (bool): Indicates if the container is the top render.
                - layers (dict): A dictionary where each key is a layer and the value is a list of serialized components.
                - column_based (bool): Indicates if the container is column-based.
                - order (Any): The order of the container.
        """
        d = {}

        for layer in self.layers:
            d[layer] = []
            for component in self.layers[layer]:
                d[layer].append(component.serialize())
        
        return {
            "component": self._base_component.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self.fatal,
            "top_render": self._top_render,
            "layers": d,
            "column_based": self._colum_based,
            "order": self.oderf,
            
        }

    
    

    