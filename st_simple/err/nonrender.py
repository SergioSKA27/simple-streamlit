
class NonRenderError:
    def __init__(self, message: Exception, fatal: bool = True,component=None):
        self.message = message
        self.fatal = fatal
        self.component = component
    
    def was_fatal(self):
        return self.fatal
    
    def __call__(self):
        if self.was_fatal():
            raise self from self.message # raise the error with the original traceback
        
        return (self.message, self.component) 
    
    
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return f"NonRenderError({self.component.__class__.__name__}): {self.message}"
    
    def __bool__(self):
        return self.fatal
    

