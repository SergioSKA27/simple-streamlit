from typing import List, Dict, Any, Callable, NoReturn, Union
from abc import ABCMeta, abstractmethod

from ...err.nonrender import NonRenderError


class Renderable(metaclass=ABCMeta):

    def __init__(self, *args, **kwargs):
        # the arguments passed directly to the base component
        self.kwargs = kwargs
        self.args = args
        self._base_component = None  # type: Callable[..., Any]
        self.fatal = True  # type: bool
        self._errhandler = None  # type: Callable[[Exception], None]
        self._top_render = False  # type: bool

    @abstractmethod
    def render(self, *args, **kwargs):
        raise NotImplementedError("The render method must be implemented")

    def set_top_render(self, top_render: bool):
        self._top_render = top_render
        return self

    def set_fatal(self, fatal: bool):
        self.fatal = fatal
        return self

    def set_errhandler(self, handler: Callable[[Exception], Union[NoReturn, bool]]):
        self._errhandler = handler
        return self

    def is_top_render(self):
        return self._top_render

    def _set_base_component(self, base_component: Callable[..., Any]):
        self._base_component = base_component
        return self

    def _get_base_component(self):
        return self._base_component

    def _safe_render(self, *args, **kwargs) -> Union[NoReturn, Any]:
        try:
            return self.render(*args, **kwargs)
        except Exception as e:
            status = False
            if self._errhandler:
                # the error handler should return True if the error was handled
                # it also could be a NoReturn function(e.g. swithcpage,stop,rerun)
                status = self._errhandler(e)

            if not status:
                return NonRenderError(e, self.fatal, self)

    def __call__(self, *args, **kwargs):
        if not self._base_component:
            raise Exception("The base component is not set")

        if not args and not kwargs:
            return self._safe_render(*self.args, **self.kwargs)

        return self._safe_render(*args, **kwargs)
