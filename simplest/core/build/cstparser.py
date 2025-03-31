from typing import List, Dict, Any, Callable, NoReturn, Union, Optional

from ..components.ielement import IElement
from ..components.velement import VElement

class StreamlitComponentParser:
    def __init__(self, component: Callable[..., Any], *args, **kwargs):
        """
        Initialize the parser with the given component and its arguments.

        Args:
            component (Callable[..., Any]): The component to be parsed.
            *args: Variable length argument list for the component.
            **kwargs: Arbitrary keyword arguments for the component.
        """
        self.component = component
        self.args = args
        self.kwargs = kwargs
        self._stateful: bool = False
        self._fatal: bool = True
        self._errhandler: Optional[Callable[[Exception], Union[NoReturn, bool]]] = None
        self._strict: bool = True
        self._autoconfig: bool = True
        self._effects: List[Callable[..., Any]] = []

    @property
    def config(self) -> Dict[str, Any]:
        """
        Returns the configuration settings of the parser.

        Returns:
            dict: A dictionary containing the following configuration settings:
                - stateful (bool): Indicates if the parser is stateful.
                - fatal (bool): Indicates if the parser should raise fatal errors.
                - errhandler (callable): The error handler function.
                - strict (bool): Indicates if the parser should enforce strict mode.
        """
        return {
            "stateful": self._stateful,
            "fatal": self._fatal,
            "errhandler": self._errhandler,
            "strict": self._strict,
        }

    def set_config(self, **kwargs) -> Dict[str, Any]:
        """
        Set or retrieve the configuration settings.
        If no keyword arguments are provided, the current configuration is returned.
        Otherwise, the provided keyword arguments are used to update the configuration.
        Keyword Args:
            stateful (bool): Optional. Set the stateful configuration.
            fatal (bool): Optional. Set the fatal configuration.
            errhandler (callable): Optional. Set the error handler.
            strict (bool): Optional. Set the strict configuration.
        Returns:
            dict: The current configuration settings.
        """
        if not kwargs:
            return self.config

        if "stateful" in kwargs:
            self.set_stateful(kwargs["stateful"])
        if "fatal" in kwargs:
            self.set_fatal(kwargs["fatal"])
        if "errhandler" in kwargs:
            self.set_errhandler(kwargs["errhandler"])
        if "strict" in kwargs:
            self.set_strict(kwargs["strict"])
        return self.config

    def set_stateful(self, stateful: bool) -> "StreamlitComponentParser":
        """
        Set the stateful property of the StreamlitComponentParser.

        Args:
            stateful (bool): A boolean indicating whether the component should be stateful.

        Returns:
            StreamlitComponentParser: The instance of the parser with the updated stateful property.
        """
        if not isinstance(stateful, bool):
            raise ValueError("stateful must be a boolean")
        self._stateful = stateful
        return self

    def set_fatal(self, fatal: bool) -> "StreamlitComponentParser":
        """
        Sets the fatal flag for the StreamlitComponentParser.

        Args:
            fatal (bool): A boolean indicating whether to set the fatal flag.

        Returns:
            StreamlitComponentParser: The instance of the parser with the updated fatal flag.
        """
        if not isinstance(fatal, bool):
            raise ValueError("fatal must be a boolean")
        self._fatal = fatal
        return self

    def set_errhandler(
        self, errhandler: Callable[[Exception], Union[NoReturn, bool]]
    ) -> "StreamlitComponentParser":
        """
        Set the error handler for the StreamlitComponentParser.

        Args:
            errhandler (Callable[[Exception], Union[NoReturn, bool]]): 
                A callable that takes an Exception as an argument and returns either 
                NoReturn or a boolean value indicating whether the error was handled.

        Returns:
            StreamlitComponentParser: The instance of the parser with the error handler set.
        """
        if not callable(errhandler):
            raise ValueError("errhandler must be callable")
        self._errhandler = errhandler
        return self

    def add_effect(self, effect: Callable[..., Any]) -> "StreamlitComponentParser":
        """
        Add an effect to the StreamlitComponentParser.

        Args:
            cause (Callable[..., Any]): A callable that takes the result of the render method as an argument.

        Returns:
            StreamlitComponentParser: The instance of the parser with the cause added.
        """
        if not callable(effect):
            raise ValueError("cause must be callable")
        self._effects.append(effect)
        return self
    
    def add_effects(self, effects: List[Callable[..., Any]]) -> "StreamlitComponentParser":
        """
        Add multiple effects to the StreamlitComponentParser.

        Args:
            causes (List[Callable[..., Any]]): A list of callables that take the result of the render method as an argument.

        Returns:
            StreamlitComponentParser: The instance of the parser with the causes added.
        """
        self._effects.extend(effects)
        return self

    def set_strict(self, strict: bool) -> "StreamlitComponentParser":
        """
        Set the strict mode for the StreamlitComponentParser.

        Parameters:
        strict (bool): If True, the parser will operate in strict mode.

        Returns:
        StreamlitComponentParser: The instance of the parser with updated strict mode.
        """
        if not isinstance(strict, bool):
            raise ValueError("strict must be a boolean")
        self._strict = strict
        return self

    def set_autoconfig(self, autoconfig: bool) -> "StreamlitComponentParser":
        """
        Sets the autoconfig flag for the StreamlitComponentParser.

        Args:
            autoconfig (bool): A boolean value to enable or disable autoconfig.

        Returns:
            StreamlitComponentParser: The instance of the parser with the updated autoconfig setting.
        """
        if not isinstance(autoconfig, bool):
            raise ValueError("autoconfig must be a boolean")
        self._autoconfig = autoconfig
        return self

    def is_autoconfig(self) -> bool:
        """
        Check if the autoconfig feature is enabled.

        Returns:
            bool: True if autoconfig is enabled, False otherwise.
        """
        return self._autoconfig

    def parse(
        self,
        stateful: bool = False,
        fatal: bool = True,
        errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ) -> Union[IElement, VElement]:
        """
        Parses the component configuration and returns an element based on the provided parameters.
        Args:
            stateful (bool): Determines if the element should be stateful. Defaults to False.
            fatal (bool): Determines if errors should be fatal. Defaults to True.
            errhandler (Callable[[Exception], Union[NoReturn, bool]]): A callable to handle errors. Defaults to None.
            strict (bool): Determines if strict mode should be enabled. Defaults to True.
        Returns:
            Union[IElement, VElement]: An instance of IElement if stateful is True, otherwise an instance of VElement.
        """
        if self.is_autoconfig():
            stateful = self.config["stateful"]
            fatal = self.config["fatal"]
            errhandler = self.config["errhandler"]
            strict = self.config["strict"]

        if stateful:
            comp = IElement(*self.args, **self.kwargs)
            comp._set_base_component(self.component).set_errhandler(
                errhandler
            ).set_fatal(fatal).set_strict(strict)
        else:
            comp = VElement(*self.args, **self.kwargs)
            comp._set_base_component(self.component).set_errhandler(
                errhandler
            ).set_fatal(fatal)
        
        comp.add_effects(self._effects)

        return comp

    def __call__(self, *args, **kwargs):
        """
        Call the parser with optional arguments.
        If no arguments are provided, it calls the `parse` method without arguments.
        Otherwise, it calls the `parse` method with the provided arguments.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            The result of the `com` function.
        """
        if not args and not kwargs:
            com = self.parse()
        else:
            com = self.parse(*args, **kwargs)

        return com()

    def __str__(self) -> str:
        """
        Return a string representation of the StreamlitComponentParser instance.

        The string representation includes the name of the component and its configuration.

        Returns:
            str: A string in the format "StreamlitComponentParser(<component_name>): <config>"
        """
        return f"StreamlitComponentParser({self.component.__name__}): {self.config}"

    def __repr__(self) -> str:
        """
        Return the string representation of the object.

        This method is called by the `repr()` built-in function and is used to provide a string representation of the object that is useful for debugging.

        Returns:
            str: The string representation of the object.
        """
        return self.__str__()

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the parsed data into a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the parsed data.
        """
        c = self.parse().serialize()
        return {
            "component": c,
            "stateful": self._stateful,
            "fatal": self._fatal,
            "strict": self._strict,
            "effects": [e.__name__ for e in self._effects],
            "_type": "StreamlitComponentParser",         
        }

