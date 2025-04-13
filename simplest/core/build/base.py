from typing import List, Dict, Any, Callable, Union, Optional, TypeVar, cast
from abc import ABC, abstractmethod

from .models.base import ParserConfig


T = TypeVar("T", bound="Parser")  # Type variable for method chaining


class Parser(ABC):
    """
    Abstract base class for parsers.
    """

    def __init__(
        self, component: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> None:
        # Validate inputs using the Pydantic model
        config = ParserConfig(
            component=component,
            args=list(args),
            kwargs=kwargs,
        )
        self.component = config.component
        self.args = config.args
        self.kwargs = config.kwargs
        self._stateful = config.stateful
        self._fatal = config.fatal
        self._strict = config.strict
        self.autoconfig = config.autoconfig
        self._effects: List[Callable[..., Any]] = []
        self._errhandler: Optional[Callable[..., Any]] = None

    @property
    def parserconfig(self) -> ParserConfig:
        """
        Returns the configuration of the parser as a Pydantic model.
        """
        return ParserConfig(
            component=self.component,
            args=self.args,
            kwargs=self.kwargs,
            stateful=self._stateful,
            fatal=self._fatal,
            strict=self._strict,
            autoconfig=self.autoconfig,
            errhandler=self._errhandler,
            effects=self._effects,
        )

    @abstractmethod
    def parse(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        Abstract method to parse the component.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def set_stateful(self, stateful: bool) -> T:
        """
        Set the stateful property of the parser.

        Args:
            stateful (bool): Whether the parser should maintain state.

        Returns:
            Parser: Self for method chaining.

        Raises:
            ValueError: If stateful is not a boolean.
        """
        if not isinstance(stateful, bool):
            raise ValueError("The 'stateful' parameter must be a boolean.")
        self._stateful = stateful
        return cast(T, self)

    def set_fatal(self, fatal: bool) -> T:
        """
        Sets the fatal flag for the current instance.

        Args:
            fatal (bool): A boolean value indicating whether the fatal flag should be set.

        Returns:
            T: The current instance, cast to the generic type T.

        Raises:
            ValueError: If the provided 'fatal' parameter is not a boolean.
        """
        if not isinstance(fatal, bool):
            raise ValueError("The 'fatal' parameter must be a boolean.")
        self._fatal = fatal
        return cast(T, self)

    def set_strict(self, strict: bool) -> T:
        """
        Sets the strict mode for the current instance.

        Args:
            strict (bool): A boolean value indicating whether strict mode
                           should be enabled or disabled.

        Returns:
            T: The current instance with the updated strict mode setting.

        Raises:
            ValueError: If the provided 'strict' parameter is not a boolean.
        """
        if not isinstance(strict, bool):
            raise ValueError("The 'strict' parameter must be a boolean.")
        self._strict = strict
        return cast(T, self)

    def set_autoconfig(self, autoconfig: bool) -> T:
        """
        Sets the autoconfig attribute for the current instance.

        Args:
            autoconfig (bool): A boolean value indicating whether to enable or disable autoconfiguration.

        Returns:
            T: The current instance, cast to the appropriate type.

        Raises:
            ValueError: If the provided 'autoconfig' parameter is not a boolean.
        """
        if not isinstance(autoconfig, bool):
            raise ValueError("The 'autoconfig' parameter must be a boolean.")
        self.autoconfig = autoconfig
        return cast(T, self)

    def set_errhandler(self, errhandler: Callable[..., Any]) -> T:
        """
        Sets the error handler for the instance.

        Args:
            errhandler (Callable[..., Any]): A callable object to handle errors.
                It must be a callable function or object.

        Returns:
            T: The instance of the class, allowing method chaining.

        Raises:
            ValueError: If the provided 'errhandler' is not callable.
        """
        if not callable(errhandler):
            raise ValueError("The 'errhandler' must be callable.")
        self._errhandler = errhandler
        return cast(T, self)

    def add_effect(self, effect: Callable[..., Any]) -> T:
        """
        Adds a callable effect to the list of effects.

        Args:
            effect (Callable[..., Any]): A callable object representing the effect to be added.

        Returns:
            T: The instance of the current object, allowing for method chaining.

        Raises:
            ValueError: If the provided effect is not callable.
        """
        if not callable(effect):
            raise ValueError("The 'effect' must be callable.")
        self._effects.append(effect)
        return cast(T, self)

    def add_effects(self, effects: List[Callable[..., Any]]) -> T:
        """
        Adds a list of callable effects to the current instance.

        Args:
            effects (List[Callable[..., Any]]): A list of callable objects to be added as effects.
                Each item in the list must be a callable.

        Returns:
            T: The current instance with the added effects.

        Raises:
            ValueError: If 'effects' is not a list or if any item in the list is not callable.
        """
        if not isinstance(effects, list) or not all(
            callable(effect) for effect in effects
        ):
            raise ValueError("All 'effects' must be callable.")
        self._effects.extend(effects)
        return cast(T, self)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Enables the instance of the class to be called as a function.
        If no arguments are provided, it parses and processes the default configuration.
        If arguments or keyword arguments are provided, it parses and processes them.
        Returns:
            Any: The result of the parsed and processed computation.
        """

        comp = self.parse() if not args and not kwargs else self.parse(*args, **kwargs)
        return comp()
