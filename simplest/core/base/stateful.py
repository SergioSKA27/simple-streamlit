from typing import List, Dict, Any, Callable, NoReturn, Union
from abc import ABC, abstractmethod

class Stateful(ABC):

    def __init__(self, *_, **kwargs):
        self.key = None
        self.editable = False
        self.strict = True
       
        if "key" in kwargs:
            self.key = kwargs["key"]

    @abstractmethod
    def track_state(self):
        raise NotImplementedError("The track_state method must be implemented")
    
    @abstractmethod
    def set_state(self, state: Any):
        raise NotImplementedError("The set_state method must be implemented")
      

    def set_key(self, key: str):
        self.key = key
        return self
    
    def set_editable(self, editable: bool):
        self.editable = editable
        return self
    
    def set_strict(self, strict: bool):
        self.strict = strict
        return self
    
    def set_state(self, state: Any):
        if not self.editable:
            raise Exception("The state is not editable")
        
        return self.set_state(state)
    
    def get_key(self):
        return self.key
    
    def get_state(self):
        return self.track_state()
    
    def get_state_tracker(self) -> Callable[[], Any]:
        return self.track_state
    
        



    

        






