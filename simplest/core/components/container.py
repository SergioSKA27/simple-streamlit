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
        self.schema.set_body_name("__container__")

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
        return f"Container({self._base_component.__name__}): {self.schema}"

    def serialize(self):
        """
        Serializes the container object into a dictionary format.
        Returns:
            dict: A dictionary containing the serialized container object.
        """

        if self._base_component is not None:
            self.schema.set_body_name(f"__{self._base_component.__name__}__")
        return {
            "component": self._base_component.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self.fatal,
            "top_render": self._top_render,
            "schema": self.schema.serialize(),
            "column_based": self._colum_based,
            "_type": "Container",
        }
