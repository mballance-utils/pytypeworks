
class TypeRgyMeta(type):
    
    def __init__(self, name, bases, dct):
        
        pass
    
    def load_done(self):
        pass
    
    def inst(self):
        return self
    
    def reset(self):
        pass
    
    def register_type(self, key, T):
        pass
        

class TypeRgy(metaclass=TypeRgyMeta):
    pass

