from typing import Any, Callable
from ..base.renderable import Renderable
from ..base.composable import Composable


class Container(Renderable, Composable):
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
        Composable.__init__(self)
        self._base_component: Callable[..., Any] = None
        self._top_render: bool = False
        self.schema.set_body_name("__container__")

    def render(self, *args, **kwargs) -> Any:
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
            self.schema.set_body_name("__children__")
        return {
            "__component__": self._base_component.__name__,
            "__args__": {
                "args": self.args,
                "kwargs": self.kwargs,
            },
            "__type__": "Container",
        }
