from typing import List, Dict, Any, Callable, NoReturn, Union
from streamlit import session_state

from ..base.renderable import Renderable
from ..base.stateful import Stateful

class IElement(Renderable, Stateful):
    """
    Base class for all interactive elements.
    e.g. Button, Checkbox, etc.
    """
    
    def __init__(self, *args, **kwargs):
        Renderable.__init__(self, *args, **kwargs)
        Stateful.__init__(self, *args, **kwargs)
    
    def render(self, *args, **kwargs) -> Any:
        return self._base_component(*self.args, **self.kwargs)

    def track_state(self) -> Any:
        if self.key not in session_state:
            return None
        
        return session_state[self.key]
    
        
    
    