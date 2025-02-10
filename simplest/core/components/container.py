from typing import List, Dict, Any, Callable, NoReturn, Union, Literal
from ..base.renderable import Renderable
from ..base.layoutable import Layoutable

class Container(Renderable, Layoutable):
    def __init__(self, *args, **kwargs):
        Renderable.__init__(self, *args, **kwargs)
        Layoutable.__init__(self)
        self._base_component = None  # type: Callable[..., Any]
        self._top_render = False  # type: bool

    def render(self, *args, **kwargs):
        self.lrender(self._base_component, *args, **kwargs)

    