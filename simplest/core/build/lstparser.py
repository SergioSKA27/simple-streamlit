from typing import List, Tuple, Dict, Any, Union, Callable, NoReturn, Literal
from .cstparser import StreamlitComponentParser
from ..components.container import Container
from ..handlers.schema import Schema
from ..handlers.layer import Layer


class StreamlitLayoutParser:
    def __init__(self, container: Callable[..., Any], *args, **kwargs):
        """
        Initialize the parser with a container and optional arguments.

        Args:
            container (Callable[..., Any]): A callable that will be used as the container.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.container = container
        self.args = args
        self.kwargs = kwargs
        self._stateful = False  # type: bool
        self._fatal = True  # type: bool
        self._errhandler = None  # type: Callable[[Exception], Union[NoReturn, bool]]
        self._strict = False
        self._colum_based = False  # type: bool
        self.schema = Schema(f"__{self.container.__name__}__")

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
            "fatal": self._fatal,
            "errhandler": self._errhandler,
            "strict": self._strict,
        }

    @property
    def body(self) -> Layer:
        """
        Returns the body layer of the parser.

        Returns:
            Layer: The body layer of the parser.
        """
        return self.schema.main_body

    def add_component(
        self, component: Callable[..., Any], *args, **kwargs
    ) -> StreamlitComponentParser:
        """
        Adds a component to the layout.

        Args:
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.

        Returns:
            Union[StreamlitComponentParser, StreamlitLayoutParser]: A StreamlitComponentParser object if the component is a container, otherwise a StreamlitLayoutParser object.
        """
        return self.schema.add_component(
            StreamlitComponentParser(component, *args, **kwargs)
        )

    def add_layer(self, idlayer: Union[int, str] = None) -> Layer:
        """
        Adds a new layer to the layout.

        Args:
            idlayer (Union[int, str], optional): The identifier of the layer to be added. Defaults to None.

        Returns:
            Layer: A Layer object representing the new layer.
        """
        return self.schema.add_layer(idlayer)

    def add_component_to_layer(
        self, idlayer: Union[int, str], component: Callable[..., Any], *args, **kwargs
    ) -> StreamlitComponentParser:
        """
        Adds a component to a specific layer.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the component will be added.
            component (Callable[..., Any]): The component to be added.
            *args: Additional positional arguments to be passed to the component.
            **kwargs: Additional keyword arguments to be passed to the component.

        Returns:
            StreamlitComponentParser: A StreamlitComponentParser object representing the added component.
        """
        return self.schema[idlayer].add_component(
            StreamlitComponentParser(component, *args, **kwargs)
        )

    def add_container(
        self, container: Callable[..., Any], *args, **kwargs
    ) -> "StreamlitLayoutParser":
        """
        Adds a container to the layout.

        Args:
            container (Callable[..., Any]): The container to be added.
            *args: Additional positional arguments to be passed to the container.
            **kwargs: Additional keyword arguments to be passed to the container.

        Returns:
            StreamlitLayoutParser: A StreamlitLayoutParser object representing the added container.
        """
        return self.schema.add_component(
            StreamlitLayoutParser(container, *args, **kwargs)
        )

    def add_container_to_layer(
        self, idlayer: Union[int, str], container: Callable[..., Any], *args, **kwargs
    ) -> "StreamlitLayoutParser":
        """
        Adds a container to a specific layer.

        Args:
            idlayer (Union[int, str]): The identifier of the layer to which the container will be added.
            container (Callable[..., Any]): The container to be added.
            *args: Additional positional arguments to be passed to the container.
            **kwargs: Additional keyword arguments to be passed to the container.

        Returns:
            StreamlitLayoutParser: A StreamlitLayoutParser object representing the added container.
        """
        return self.schema[idlayer].add_component(
            StreamlitLayoutParser(container, *args, **kwargs)
        )

    def parse(
        self,
        fatal: bool = True,
        errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        column_based: bool = False,
    ) -> Container:
        """
        Parses the input and constructs a Container object with the specified configuration.

        Args:
            fatal (bool): If True, the parser will raise exceptions on errors. Defaults to True.
            errhandler (Callable[[Exception], Union[NoReturn, bool]], optional): A custom error handler function. Defaults to None.
            column_based (bool): If True, the parser will operate in column-based mode. Defaults to False.
            layers (Dict[Union[int, str], List[Callable[..., Any]]], optional): A dictionary mapping layer identifiers to lists of callables. Defaults to None.
            order (List[Union[int, str]], optional): A list specifying the order of layers. Defaults to None.

        Returns:
            Container: A Container object configured with the specified parameters.
        """

        comp = Container(*self.args, **self.kwargs)
        comp._set_base_component(self.container).set_errhandler(
            errhandler if errhandler else self._errhandler
        ).set_fatal(fatal if fatal else self._fatal).set_column_based(
            column_based if column_based else self._colum_based
        ).set_component_parser(
            StreamlitComponentParser
        )
        self.schema.set_body_name(f"__{self.container.__name__}__")
        comp.schema = self.schema

        return comp

    def set_column_based(self, column_based: bool) -> "StreamlitLayoutParser":
        """
        Sets the layout to be column-based or not.

        Args:
            column_based (bool): If True, sets the layout to be column-based. If False, sets it to be row-based.

        Returns:
            StreamlitLayoutParser: The current StreamlitLayoutParser object.
        """
        self._colum_based = column_based
        return self

    def set_errhandler(
        self, errhandler: Callable[[Exception], Union[NoReturn, bool]]
    ) -> "StreamlitLayoutParser":
        """
        Sets a custom error handler for the parser.

        Args:
            errhandler (Callable[[Exception], Union[NoReturn, bool]]): A custom error handler function.

        Returns:
            StreamlitLayoutParser: The current StreamlitLayoutParser object.
        """
        self._errhandler = errhandler
        return self

    def set_fatal(self, fatal: bool) -> "StreamlitLayoutParser":
        """
        Sets the fatal flag for the parser.

        Args:
            fatal (bool): If True, the parser will raise exceptions on errors. If False, it will not.

        Returns:
            StreamlitLayoutParser: The current StreamlitLayoutParser object.
        """
        self._fatal = fatal
        return self

    def __getitem__(
        self, index: Union[int, str]
    ) -> Union[Layer, StreamlitComponentParser]:
        """
        Retrieves a layer or component by its index or key.

        Args:
            index (Union[int, str]): The index or key of the layer or component.

        Returns:
            Union[Layer, StreamlitComponentParser]: The layer or component corresponding to the given index or key.
        """
        return self.schema[index]

    def __len__(self) -> int:
        """
        Returns the number of layers in the layout.

        Returns:
            int: The number of layers in the layout.
        """
        return len(self.schema)

    def __repr__(self) -> str:
        """
        Returns a string representation of the StreamlitLayoutParser object.

        Returns:
            str: A string representation of the StreamlitLayoutParser object.
        """
        return f"StreamlitLayoutParser: {self.container.__name__}"

    def __str__(self) -> str:
        """
        Returns a string representation of the StreamlitLayoutParser object.

        Returns:
            str: A string representation of the StreamlitLayoutParser object.
        """
        return self.__repr__()

    def __call__(self, *args, **kwds):
        if not args and not kwds:
            comp = self.parse()
        else:
            comp = self.parse(*args, **kwds)

        return comp()

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the StreamlitLayoutParser object into a dictionary format.

        Returns:
            dict: A dictionary containing the serialized StreamlitLayoutParser object.
        """
        return {
            "component": self.container.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "fatal": self._fatal,
            "errhandler": self._errhandler,
            "strict": self._strict,
            "column_based": self._colum_based,
            "_type": "StreamlitLayoutParser",
            "schema": self.schema.serialize(),
        }
