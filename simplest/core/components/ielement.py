from typing import List, Dict, Any, Callable, NoReturn, Union
from streamlit import session_state

from ..base.renderable import Renderable
from ..base.stateful import Stateful


class IElement(Renderable, Stateful):
    """
    Base class for all interactive elements.
    e.g. Button, Checkbox, etc.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the IElement instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        Renderable.__init__(self, *args, **kwargs)
        Stateful.__init__(self, *args, **kwargs)

    def render(self, *args, **kwargs) -> Any:
        """
        Renders the base component with the provided arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the base component's render method.
        """
        return self._base_component(*self.args, **self.kwargs)

    def track_state(self) -> Any:
        """
        Tracks the state of the current element using its key.
        Returns:
            Any: The state associated with the element's key if it exists in the session state,
                 otherwise None.
        """
        if self.key not in session_state:
            return None

        return session_state[self.key]

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the component instance into a dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing the serialized component data with the following keys:
                - component (str): The name of the base component class.
                - args (list): The positional arguments passed to the component.
                - kwargs (dict): The keyword arguments passed to the component.
                - fatal (bool): Indicates if the component is fatal.
                - key (str): The unique key for the component.
                - editable (bool): Indicates if the component is editable.
                - strict (bool): Indicates if the component is strict.
        """
        return {
            "component": self._base_component.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self.fatal,
            "key": self.key,
            "editable": self.editable,
            "strict": self.strict,
            "_type": "IElement",
        }
