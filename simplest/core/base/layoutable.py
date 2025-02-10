from typing import List, Dict, Any, Callable, NoReturn, Union, Literal


class Layoutable:
    def __init__(self):
        self.layers = {}  # type: Dict[Union[int, str], List[Callable[..., Any]]]
        self._colum_based = False  # type: bool
        self.oderf = [] # type: List[Union[int, str]]
        
    def lrender(self,based_component: Callable[..., Any],*args, **kwargs):
        if self._colum_based:
            if not args and not kwargs:
                args = [len(self.layers)]

            k = 0
            c = based_component(*args, **kwargs) 
            for layer in self.oderf if self.oderf else self.layers.keys():
                with c[k]:
                    for component in self.layers[layer]:
                            component()
                k += 1
        else:
            
            c = based_component(*args, **kwargs)
            for layer in self.oderf if self.oderf else self.layers.keys():
                with c:
                    for component in self.layers[layer]:
                        component()
        

    def add_layer(self, idlayer: Union[int, str], components: List[Callable[..., Any]]):
        self.layers[idlayer] = components
        return self
    
    def add_component(self, idlayer: Union[int, str], component: Callable[..., Any]):
        if idlayer not in self.layers:
            self.layers[idlayer] = []
        self.layers[idlayer].append(component)
        return self
    
    def set_column_based(self, column_based: bool):
        self._colum_based = column_based
        return self
    
    def is_column_based(self):
        return self._colum_based

        
    

        