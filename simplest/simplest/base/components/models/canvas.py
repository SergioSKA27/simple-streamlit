from typing import Callable, NoReturn, Union, Optional
from pydantic import BaseModel, field_validator


class CanvasConfig(BaseModel):
    """
    Configuration model for AppPage initialization parameters.
    
    Attributes:
        failsafe (bool): Whether to continue execution when errors occur. Default is False.
        failhandler (Optional[Callable[[Exception], Union[NoReturn, bool]]]): 
            A callable that handles exceptions. Default is None.
        strict (bool): Whether to enforce strict type checking. Default is True.
    """
    failsafe: bool = False
    failhandler: Optional[Callable[[Exception], Union[NoReturn, bool]]] = None
    strict: bool = True
    
    @field_validator("failhandler")
    def validate_failhandler(cls, value):
        """Validate that failhandler is callable if provided."""
        if value is not None and not callable(value):
            raise ValueError("failhandler must be callable")
        return value