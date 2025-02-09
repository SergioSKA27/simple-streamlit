from ..base.renderable import Renderable

class VElement(Renderable):
    """
    Base class for all stateless visual elements.
    e.g. Text, Image, HTML, etc.
    """

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
    
    def render(self, *args, **kwargs):
        return self._base_component(*self.args, **self.kwargs)

    

