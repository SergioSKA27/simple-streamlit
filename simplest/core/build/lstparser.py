from typing import List, Tuple, Dict, Any, Union, Callable, NoReturn, Literal
from ..components.container import Container


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

    def parse(
        self,
        fatal: bool = True,
        errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        column_based: bool = False,
        layers: Dict[Union[int, str], List[Callable[..., Any]]] = None,
        order: List[Union[int, str]] = None,
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
        comp._set_base_component(self.container).set_errhandler(errhandler).set_fatal(
            fatal
        ).set_column_based(column_based)
        if layers:
            for layer in layers:
                comp.add_layer(layer, layers[layer])
        if order:
            comp.oderf = order
        return comp