
class DeclRgyMeta(type):
    
    def __init__(self, name, bases, dct):
        pass
    
    def inst(self):
        return self
    pass

class DeclRgy(metaclass=DeclRgyMeta):
    pass