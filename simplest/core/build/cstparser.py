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
        self._stateful = False
        self._fatal = True
        self._errhandler = None
        self._strict = True
        self._autoconfig = True
    
    @property
    def config(self):
        return {
            "stateful": self._stateful,
            "fatal": self._fatal,
            "errhandler": self._errhandler,
            "strict": self._strict,
        }
    

    def set_config(self, **kwargs):
        if not kwargs:
            return self.config
        
        if "stateful" in kwargs:
            self.set_stateful(kwargs["stateful"])
        if "fatal" in kwargs:
            self.set_fatal(kwargs["fatal"])
        if "errhandler" in kwargs:
            self.set_errhandler(kwargs["errhandler"])
        if "strict" in kwargs:
            self.set_strict(kwargs["strict"])
        return self.config

    def set_stateful(self, stateful: bool) -> "StreamlitComponentParser":
        self._stateful = stateful
        return self
    
    def set_fatal(self, fatal: bool) -> "StreamlitComponentParser":
        self._fatal = fatal
        return self
    
    def set_errhandler(self, errhandler: Callable[[Exception], Union[NoReturn, bool]]) -> "StreamlitComponentParser":
        self._errhandler = errhandler
        return self
    
    def set_strict(self, strict: bool) -> "StreamlitComponentParser":
        self._strict = strict
        return self

    def set_autoconfig(self, autoconfig: bool) -> "StreamlitComponentParser":
        self._autoconfig = autoconfig
        return self
    
    
    def is_autoconfig(self) -> bool:
        return self._autoconfig


    def parse(
        self,
        stateful: bool = False,
        fatal: bool = True,
        errhandler: Callable[[Exception], Union[NoReturn, bool]] = None,
        strict: bool = True,
    ) -> Union[IElement, VElement]:
        if self.is_autoconfig():
            stateful = self.config["stateful"]
            fatal = self.config["fatal"]
            errhandler = self.config["errhandler"]
            strict = self.config["strict"]
    
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

    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            com = self.parse()
        else:
            com = self.parse(*args, **kwargs)
        
        return com()
    
    def __str__(self):
        return f"StreamlitComponentParser({self.component.__name__}): {self.config}"
    
    def __repr__(self):
        return self.__str__()