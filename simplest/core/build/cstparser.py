from typing import List, Dict, Any, Callable, NoReturn, Union, Optional

from ..components.ielement import IElement
from ..components.velement import VElement

from .base import Parser


class StreamlitComponentParser(Parser):
    def __init__(self, component: Callable[..., Any], *args, **kwargs):
        """
        Initialize the parser with the given component and its arguments.

        Args:
            component (Callable[..., Any]): The component to be parsed.
            *args: Variable length argument list for the component.
            **kwargs: Arbitrary keyword arguments for the component.
        """
        super().__init__(component, *args, **kwargs)

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
        if self.parserconfig.autoconfig:
            stateful = self.parserconfig.stateful
            fatal = self.parserconfig.fatal
            errhandler = self.parserconfig.errhandler
            strict = self.parserconfig.strict

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

    def __str__(self) -> str:
        """
        Return a string representation of the StreamlitComponentParser instance.

        The string representation includes the name of the component and its configuration.

        Returns:
            str: A string in the format "StreamlitComponentParser(<component_name>): <config>"
        """
        return (
            f"StreamlitComponentParser({self.component.__name__}): {self.parserconfig}"
        )

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
            "__base__": c,
            "__parser__": {
                "stateful": self.parserconfig.stateful,
                "fatal": self.parserconfig.fatal,
                "strict": self.parserconfig.strict,
                "autoconfig": self.parserconfig.autoconfig,
            },
            "__type__": "StreamlitComponentParser",
        }
