from typing import List, Dict, Any, Callable, NoReturn, Union

from ..components.ielement import IElement
from ..components.velement import VElement


class StreamlitComponentParser:
    def __init__(
        self, component: Callable[..., Any], *args, **kwargs
    ):
        self.component = component
        self.args = args
        self.kwargs = kwargs

    def parse(
        self,
        stateful: bool = False,
        fatal: bool = True,
        errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ) -> Union[IElement, VElement]:
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

        return comp
