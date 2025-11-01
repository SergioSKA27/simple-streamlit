from typing import Any, Callable, Union, Dict, List, Optional, Tuple, TypeVar,Literal
from abc import ABCMeta, abstractmethod

T = TypeVar("T", bound="BaseRepresentation")  # Type variable for method chaining

class BaseRepresentation(metaclass=ABCMeta):
    """
    Base class for all representations.

    A representation is a class that can be used to represent the default
    representation of a given type, including the  default arguments to create
    a generic representation of that type. and also can be used to enforce an
    specific behavior through the use of the different parsers.
    """

    TYPE = None  # type: Optional[TypeVar]

    # Use the singleton pattern to ensure that only one instance of the class is created
    
    def __new__(cls, *args: Any, **kwargs: Any) -> T:
        if not hasattr(cls, "_instance"):
            cls._instance = super(BaseRepresentation, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        default_args: List[Any],
        default_kwargs: Dict[str, Any],
        stateful: bool = False,
        fatal: bool = False,
        strict: bool = True,
        column_based: bool = False,
        bind: Optional[Literal["type", "name"]] = "name",
        **kwargs: Dict[str, Any]
    ):
        """
        Initialize the representation with the default arguments and keyword arguments.

        Args:
            default_args (List[Any]): List of default arguments.
            default_kwargs (Dict[str, Any]): Dictionary of default keyword arguments.
            stateful (bool): Whether the representation is stateful. Defaults to False.
            fatal (bool): Whether the representation is fatal. Defaults to False.
            strict (bool): Whether to enforce strict behavior. Defaults to True.
            column_based (bool): Whether the representation is column based. Defaults to False.

        """
        self.default_args = default_args
        self.default_kwargs = default_kwargs
        self.stateful = stateful
        self.fatal = fatal
        self.strict = strict
        self.column_based = column_based
        self.kwargs = kwargs
        self._type = None  # type: Optional[TypeVar]
        self.bind = bind

    @abstractmethod
    def generic_factory(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        Abstract method to create a generic representation of the type.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Callable[..., Any]: A callable that represents the generic factory.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    @abstractmethod
    def serialize(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Abstract method to serialize the representation.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Dict[str, Any]: A dictionary representing the serialized object.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def deserialize(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        Abstract method to deserialize the representation.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Callable[..., Any]: A callable that represents the deserialized object.
        """
        raise NotImplementedError("Subclasses must implement this method.")


    def get_parser_defaults(self):
        return {
            "stateful": self.stateful,
            "fatal": self.fatal,
            "strict": self.strict,
            "column_based": self.column_based,
        }
    
    def get_str_representation(self) -> str:
        """
        Get the string representation of the type.

        Returns:
            str: String representation of the type.
        """
        return self._type.__name__

    def get_default_args(self) -> List[Any]:
        """
        Get the default arguments for the representation.

        Returns:
            List[Any]: List of default arguments.
        """
        return self.default_args

    def get_default_kwargs(self) -> Dict[str, Any]:
        """
        Get the default keyword arguments for the representation.

        Returns:
            Dict[str, Any]: Dictionary of default keyword arguments.
        """
        return self.default_kwargs

    def get_tdeserializer(self) -> Tuple[TypeVar, Callable[..., Any]]:
        """
        Get the type and deserializer for the representation.

        Returns:
            Tuple[TypeVar, Callable[..., Any]]: A tuple containing the type and deserializer function.
        """
        return (self._type, self.deserialize)

    def set_type(self, typ: TypeVar) -> None:
        """
        Set the type for the representation.

        Args:
            typ (TypeVar): The type to set.
        """
        self._type = typ

    def is_stateful(self) -> bool:
        """
        Check if the representation is stateful.

        Returns:
            bool: True if stateful, False otherwise.
        """
        return self.stateful

    def is_fatal(self) -> bool:
        """
        Check if the representation is fatal.

        Returns:
            bool: True if fatal, False otherwise.
        """
        return self.fatal

    def is_strict(self) -> bool:
        """
        Check if the representation is strict.

        Returns:
            bool: True if strict, False otherwise.
        """
        return self.strict

    def is_column_based(self) -> bool:
        """
        Check if the representation is column based.

        Returns:
            bool: True if column based, False otherwise.
        """
        return self.column_based


    def __eq__(self, value):
        """
        Check if the representation is equal to another value.

        Args:
            value: The value to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """
        return   value == self._type.__name__ or value.__name__ == self._type.__name__
    

    def __repr__(self) -> str:
        """
        Get the string representation of the representation.

        Returns:
            str: String representation.
        """
        return self._type.__name__ if self.bind == "name" else str(type(self))

    def __str__(self):
        return self._type.__name__ if self.bind == "name" else str(type(self))