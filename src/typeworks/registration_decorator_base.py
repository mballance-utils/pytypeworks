

from typeworks.impl.decl_rgy import DeclRgy


class RegistrationDecoratorBase(object):
    """ 
    Base class for decorators that register an declaration's existence
    """
    
    def __init__(self, key, args, kwargs):
        self.key = key
        self.args = args
        self.kwargs = kwargs
        self.T = None
        
    def register_decl(self, T):
        DeclRgy.push_decl(self.key, T)
        
    def __call__(self, T):
        self.T = T
        
        self.register_decl(T)

        return T
    
    