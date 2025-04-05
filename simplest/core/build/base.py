from typing import List, Dict, Any, Callable, Union, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator


class ParserConfig(BaseModel):
    """
    Pydantic model to validate the configuration of the Parser.
    """
    component: Callable[..., Any]
    args: List[Any] = Field(default_factory=list)
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    stateful: bool = False
    fatal: bool = False
    strict: bool = True
    autoconfig: bool = True
    errhandler: Optional[Callable[..., Any]] = None
    effects: List[Callable[..., Any]] = Field(default_factory=list)

    @field_validator("component")
    def validate_component(cls, value):
        if not callable(value):
            raise ValueError("The 'component' must be callable.")
        return value
    
    @field_validator("errhandler")
    def validate_errhandler(cls, value):
        if value is not None and not callable(value):
            raise ValueError("The 'errhandler' must be callable.")
        return value
    

    @field_validator("effects")
    def validate_effects(cls, value):
        if not isinstance(value, list) or not all(callable(effect) for effect in value):
            raise ValueError("All 'effects' must be callable.")
        return value
    
    



class Parser(ABC):
    """
    Abstract base class for parsers.
    """

    def __init__(self, component: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        # Validate inputs using the Pydantic model
        config = ParserConfig(
            component=component,
            args=list(args),
            kwargs=kwargs,
        )
        self.component = config.component
        self.args = config.args
        self.kwargs = config.kwargs
        self._stateful = config.stateful
        self._fatal = config.fatal
        self._strict = config.strict
        self.autoconfig = config.autoconfig
        self._effects: List[Callable[..., Any]] = []
        self._errhandler: Optional[Callable[..., Any]] = None

    @property
    def parserconfig(self) -> ParserConfig:
        """
        Returns the configuration of the parser as a Pydantic model.
        """
        return ParserConfig(
            component=self.component,
            args=self.args,
            kwargs=self.kwargs,
            stateful=self._stateful,
            fatal=self._fatal,
            strict=self._strict,
            autoconfig=self.autoconfig,
            errhandler=self._errhandler,
            effects=self._effects,
        )
    


    @abstractmethod
    def parse(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        Abstract method to parse the component.
        """
        raise NotImplementedError("Subclasses must implement this method.")



    def set_stateful(self, stateful: bool) -> "Parser":
        """
        Set the stateful property of the parser.
        """
        self._stateful = stateful
        return self
    
    def set_fatal(self, fatal: bool) -> "Parser":
        """
        Set the fatal property of the parser.
        """
        self._fatal = fatal
        return self
    
    def set_strict(self, strict: bool) -> "Parser":
        """
        Set the strict property of the parser.
        """
        self._strict = strict
        return self
    
    def set_autoconfig(self, autoconfig: bool) -> "Parser":
        """
        Set the autoconfig property of the parser.
        """
        self.autoconfig = autoconfig
        return self
    
    def set_errhandler(self, errhandler: Callable[..., Any]) -> "Parser":
        """
        Set the error handler of the parser.
        """
        if not callable(errhandler):
            raise ValueError("The 'errhandler' must be callable.")
        self._errhandler = errhandler
        return self
    

    def add_effect(self, effect: Callable[..., Any]) -> "Parser":
        """
        Add an effect to the parser.
        """
        if not callable(effect):
            raise ValueError("The 'effect' must be callable.")
        self._effects.append(effect)
        return self
    

    def add_effects(self, effects: List[Callable[..., Any]]) -> "Parser":
        """
        Add multiple effects to the parser.
        """
        if not isinstance(effects, list) or not all(callable(effect) for effect in effects):
            raise ValueError("All 'effects' must be callable.")
        self._effects.extend(effects)
        return self
    



    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call the parser with the given arguments.
        """
        comp = self.parse() if not args and not kwargs else self.parse(*args, **kwargs)
        return comp()
    
