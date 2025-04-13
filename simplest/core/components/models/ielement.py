from typing import Dict, Any, Callable, Tuple
from pydantic import BaseModel, Field, field_validator



class IElementConfig(BaseModel):
    """
    Configuration model for IElement initialization parameters.
    """
    args: Tuple[Any, ...] = Field(default=())
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('kwargs')
    def validate_key_in_kwargs(cls, v):
        """Ensure key exists in kwargs for stateful components."""
        if 'key' not in v:
            v['key'] = f"element_{id(v)}"
        return v


class BaseComponentConfig(BaseModel):
    """
    Configuration model for base component validation.
    """
    component: Callable[..., Any]
    
    @field_validator('component')
    def validate_component(cls, v):
        """Validate that component is callable."""
        if not callable(v):
            raise ValueError("Base component must be callable")
        return v


class StateKeyConfig(BaseModel):
    """
    Configuration model for state key validation.
    """
    key: str
    
    @field_validator('key')
    def validate_key(cls, v):
        """Validate that key is a non-empty string."""
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Key must be a non-empty string")
        return v