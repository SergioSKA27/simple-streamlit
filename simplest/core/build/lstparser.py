from typing import List, Tuple, Dict, Any, Union, Callable, NoReturn, Literal
from ..components.container import Container


class StreamlitLayoutParser:
    def __init__(self, container: Callable[..., Any], *args, **kwargs):
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