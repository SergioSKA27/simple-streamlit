from typing import Dict, Any, Callable, Union
from pydantic import BaseModel, field_validator


class ComponentParserValidator(BaseModel):
    """Validator for component parser"""
    parser: Callable[..., Any]
    
    @field_validator('parser')
    def must_be_callable(cls, v):
        if not callable(v):
            raise ValueError("Component parser must be callable")
        return v

class LayerIDValidator(BaseModel):
    """Validator for layer identifiers"""
    layer_id: Union[int, str]
