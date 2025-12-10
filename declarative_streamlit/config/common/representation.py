from typing import Any, Callable, Union, Dict, List

from ...core.build.cstparser import StreamlitComponentParser
from ..base.representation import BaseRepresentation


class CommonRepresentation(BaseRepresentation):
    """
    A class that represents a common representation in the system.
    It is a subclass of BaseRepresentation and provides additional functionality.
    """

    def __init__(
        self,
        default_args: List[Any] = None,
        default_kwargs: Dict[str, Any] = None,
        stateful: bool = False,
        fatal: bool = False,
        strict: bool = True,
        column_based: bool = False,
        **kwargs: Dict[str, Any]
    ) -> None:
        """
        Initialize the CommonRepresentation with default arguments and keyword arguments.

        Args:
            default_args (List[Any]): List of default arguments.
            default_kwargs (Dict[str, Any]): Dictionary of default keyword arguments.
            stateful (bool): Whether the representation is stateful. Defaults to False.
            fatal (bool): Whether the representation is fatal. Defaults to False.
            strict (bool): Whether to enforce strict behavior. Defaults to True.
            column_based (bool): Whether the representation is column based. Defaults to False.
        """
        super().__init__(
            default_args or [],
            default_kwargs or {},
            stateful,
            fatal,
            strict,
            column_based,
            **kwargs,
        )

    def generic_factory(self) -> Callable[..., Any]:
        """
        Create a generic representation of the type.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Callable[..., Any]: A callable that represents the generic factory.
        """
        p = (
            StreamlitComponentParser(
                self._type,
                *self.default_args,
                **self.default_kwargs,
            )
            .set_stateful(self.stateful)
            .set_fatal(self.fatal)
            .set_strict(self.strict)
        )
    
        return p
    
    def deserialize(self) -> Callable[..., Any]:
        return self._type

    def __str__(self) -> str:
        return f"{self._type.__name__}: {self.default_args}, {self.default_kwargs}, {self.get_parser_defaults()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._type.__name__})"

    def serialize(self) -> Dict[str, Union[str, List[Any], Dict[str, Any]]]:
        """
        Serialize the representation into a dictionary.

        Returns:
            Dict[str, Union[str, List[Any], Dict[str, Any]]]: Serialized representation.
        """
        return {
            "type": self._type.__name__,
            "args": self.default_args,
            "kwargs": self.default_kwargs,
            "stateful": self.stateful,
            "fatal": self.fatal,
            "strict": self.strict,
            "column_based": self.column_based,
        }