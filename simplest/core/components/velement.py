from ..base.renderable import Renderable


class VElement(Renderable):
    """
    Base class for all stateless visual elements.
    e.g. Text, Image, HTML, etc.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the class.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        """
        Renders the base component with the provided arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the base component rendered with the provided arguments and keyword arguments.
        """
        return self._base_component(*self.args, **self.kwargs)

    def serialize(self):
        """
        Serializes the component instance into a dictionary.

        Returns:
            dict: A dictionary containing the component's class name,
                  positional arguments, keyword arguments, and fatal flag.
        """
        return {
            "component": self._base_component.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self.fatal,
            "_type": "VElement",
        }
