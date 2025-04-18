from typing import List, Dict, Any, Callable, NoReturn, Union, Optional, Tuple
from pydantic import BaseModel, Field, field_validator

class RenderableConfig(BaseModel):
    """
    Configuration model for Renderable initialization parameters.
    """
    args: Tuple[Any, ...] = Field(default=())
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    fatal: bool = True
    top_render: bool = False


class ErrorHandlerConfig(BaseModel):
    """
    Configuration model for error handler.
    """
    handler: Optional[Callable[[Exception], Union[NoReturn, bool]]] = None

    @field_validator("handler")
    def validate_handler(cls, v):
        """Validate that handler is callable if provided."""
        if v is not None and not callable(v):
            raise ValueError("Error handler must be callable")
        return v


class EffectConfig(BaseModel):
    """
    Configuration model for effects.
    """
    effect: Callable[..., Any]

    @field_validator("effect")
    def validate_effect(cls, v):
        """Validate that effect is callable."""
        if not callable(v):
            raise ValueError("Effect must be callable")
        return v


class EffectsListConfig(BaseModel):
    """
    Configuration model for a list of effects.
    """
    effects: List[Callable[..., Any]] = Field(default_factory=list)

    @field_validator("effects")
    def validate_effects(cls, values):
        """Validate that all effects are callable."""
        if not all(callable(effect) for effect in values):
            raise ValueError("All effects must be callable")
        return values


class BaseComponentConfig(BaseModel):
    """
    Configuration model for base component.
    """
    base_component: Callable[..., Any]

    @field_validator("base_component")
    def validate_base_component(cls, v):
        """Validate that base_component is callable."""
        if not callable(v):
            raise ValueError("Base component must be callable")
        return v


