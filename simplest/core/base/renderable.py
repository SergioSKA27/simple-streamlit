from typing import List, Dict, Any, Callable, NoReturn, Union
from abc import ABCMeta, abstractmethod

from ...err.nonrender import NonRenderError


class Renderable(metaclass=ABCMeta):
    """
    Base class for all renderable components.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the renderable object with given arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            kwargs (dict): The keyword arguments passed to the base component.
            args (tuple): The arguments passed to the base component.
            _base_component (Callable[..., Any]): The base component to be rendered.
            fatal (bool): Indicates if the error is fatal.
            _errhandler (Callable[[Exception], None]): The error handler function.
            _top_render (bool): Indicates if this is the top-level render.
        """
        # the arguments passed directly to the base component
        self.kwargs = kwargs
        self.args = args
        self._base_component = None  # type: Callable[..., Any]
        self.fatal = True  # type: bool
        self._errhandler = None  # type: Callable[[Exception], None]
        self._top_render = False  # type: bool
        self._effects = []  # type: List[Callable[..., Any]]

    @abstractmethod
    def render(self, *args, **kwargs):
        """
        Render the content.

        This method must be implemented by subclasses to define how the content
        should be rendered.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("The render method must be implemented")

    def set_top_render(self, top_render: bool):
        """
        Sets the top render flag for the renderable object.

        Args:
            top_render (bool): A boolean indicating whether this object should be rendered on top.

        Returns:
            self: The instance of the renderable object.
        """
        self._top_render = top_render
        return self

    def set_fatal(self, fatal: bool):
        """
        Sets the fatal attribute of the object.

        Parameters:
        fatal (bool): A boolean value to set the fatal attribute.

        Returns:
        self: Returns the instance of the object to allow method chaining.
        """
        self.fatal = fatal
        return self

    def set_errhandler(self, handler: Callable[[Exception], Union[NoReturn, bool]]):
        """
        Sets the error handler for the renderable object.

        Args:
            handler (Callable[[Exception], Union[NoReturn, bool]]): A callable that takes an Exception as an argument
            and returns either NoReturn or a boolean value.

        Returns:
            self: The instance of the renderable object with the error handler set.
        """
        self._errhandler = handler
        return self

    def add_effect(self, effect: Callable[..., Any]):
        """
        Adds a effect to the renderable object.
        An effect is a callable that takes the result of the render method as an argument.


        Args:
            effect (Callable[..., Any]): A callable that takes the result of the render method as an argument.

        Returns:
            self: The instance of the renderable object with the effect added.
        """
        self._effects.append(effect)
        return self

    def add_effects(self, effects: List[Callable[..., Any]]):
        """
        Adds multiple effects to the renderable object.

        Args:
            effects (List[Callable[..., Any]]): A list of callables that take the result of the render method as an argument.

        Returns:
            self: The instance of the renderable object with the effects added.
        """
        self._effects.extend(effects)
        return self

    def is_top_render(self):
        """
        Check if this instance is the top render.
        Top render is the render that is  called at the top level.

        Returns:
            bool: True if this instance is the top render, False otherwise.
        """
        return self._top_render

    def _set_base_component(self, base_component: Callable[..., Any]):
        """
        Sets the base component for the renderable object.

        Args:
            base_component (Callable[..., Any]): The base component to be set.

        Returns:
            self: The instance of the renderable object.
        """
        self._base_component = base_component
        return self

    def _get_base_component(self):
        """
        Retrieve the base component.

        Returns:
            The base component of the current instance.
        """
        return self._base_component

    def _safe_render(self, *args, **kwargs) -> Union[NoReturn, Any]:
        """
        Safely renders the component by calling the `render` method and handling any exceptions that occur.
        Args:
            *args: Variable length argument list to be passed to the `render` method.
            **kwargs: Arbitrary keyword arguments to be passed to the `render` method.
        Returns:
            Union[NoReturn, Any]: The result of the `render` method if successful, or a `NonRenderError` if an exception occurs and is not handled.
        Raises:
            Exception: Any exception raised by the `render` method if it is not handled by the error handler.
        Notes:
            - If an exception occurs, the method will check if an error handler (`_errhandler`) is defined.
            - The error handler should return `True` if the error was handled, otherwise `False`.
            - If the error handler does not handle the exception, a `NonRenderError` is returned.
        """
        try:
            if res := self.render(*args, **kwargs):
                for eff in self._effects:
                    eff(res)
                return res
        except Exception as e:
            status = False
            if self._errhandler:
                # the error handler should return True if the error was handled
                # it also could be a NoReturn function(e.g. swithcpage,stop,rerun)
                status = self._errhandler(e)

            if not status:
                return NonRenderError(e, self.fatal, self)

    def __call__(self, *args, **kwargs):
        """
        Call the renderable object with the provided arguments.
        This method allows the object to be called as a function. It will render
        the base component with the given arguments if provided, otherwise it will
        use the default arguments stored in the object.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            The result of the _safe_render method.
        Raises:
            Exception: If the base component is not set.
        """
        if not self._base_component:
            raise Exception("The base component is not set")

        if not args and not kwargs:
            return self._safe_render(*self.args, **self.kwargs)

        return self._safe_render(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the Renderable object.

        If the 'key' is present in the kwargs, it includes the key in the string representation.

        Returns:
            str: A string in the format "Renderable(<base_component_name>) with key: <key_value>".
        """
        k = None
        if "key" in self.kwargs:
            k = self.kwargs["key"]
        return f"Renderable({self._base_component.__name__}) with key: {k}"

    def __repr__(self):
        """
        Return a string representation of the object for debugging.

        This method is intended to provide a "formal" string representation of the object that can be used for debugging and logging purposes. It calls the __str__() method to generate the string representation.

        Returns:
            str: A string representation of the object.
        """
        return self.__str__()

    def serialize(self):
        """
        Serialize the object to a dictionary.

        Returns:
            dict: A dictionary containing the serialized object data.
        """
        return {
            "base_component": self._base_component.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self.fatal,
            "top_render": self._top_render,
        }

    def __enter__(self):
        """
        Enter the context manager.

        Returns:
            Any: The result of the render method.
        """
        return self.render()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.

        Args:
            exc_type: The type of the exception.
            exc_value: The exception value.
            traceback: The traceback of the exception.
        """

        if exc_type:
            raise exc_type(exc_value).with_traceback(traceback)

    @classmethod
    def deserialize(
        cls,
        data: Dict[str, Any],
        components: Dict[str, Callable[..., Any]],
        effects: Dict[str, Callable[..., Any]],
    ):
        """
        Deserialize the object from a dictionary.

        Args:
            data (dict): A dictionary containing the serialized object data.

        Returns:
            Renderable: A new instance of the Renderable object with the deserialized data.
        """
        obj = cls()
        obj.args = data["args"]
        obj.kwargs = data["kwargs"]
        obj.fatal = data["fatal"]
        obj._top_render = data["top_render"]
        obj._base_component = components[data["base_component"]]
        return obj
