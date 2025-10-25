from typing import List, Dict, Any, Callable, Optional
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
