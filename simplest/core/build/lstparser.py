from typing import List, Tuple, Dict, Any, Union, Callable, NoReturn, Literal

from ..components.container import Container
from ..handlers.schema import Schema
from ..handlers.layer import Layer

from .cstparser import StreamlitComponentParser
from .base import Parser


class StreamlitLayoutParser(Parser):
    def __init__(self, container: Callable[..., Any], *args, **kwargs):
        """
        Initialize the parser with a container and optional arguments.

        Args:
            container (Callable[..., Any]): A callable that will be used as the container.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(container, *args, **kwargs)
        self._colum_based = False  # type: bool
        self.schema = Schema(f"__children__")

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
        if self.parserconfig.autoconfig:
            fatal = self.parserconfig.fatal
            errhandler = self.parserconfig.errhandler
            column_based = self._colum_based

        comp._set_base_component(self.component).set_errhandler(errhandler).set_fatal(
            fatal
        ).set_column_based(column_based).set_component_parser(StreamlitComponentParser)
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

    def serialize(self) -> Dict[str, Any]:
        """
        Serializes the StreamlitLayoutParser object into a dictionary format.

        Returns:
            dict: A dictionary containing the serialized StreamlitLayoutParser object.
        """
        c = self.parse().serialize()
        return {
            "__base__": c,
            "__parser__": {
                "stateful": self.parserconfig.stateful,
                "fatal": self.parserconfig.fatal,
                "strict": self.parserconfig.strict,
                "column_based": self._colum_based,
            },
            "__type__": "StreamlitLayoutParser",
        }
