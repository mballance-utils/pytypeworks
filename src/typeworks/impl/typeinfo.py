
class TypeInfo(object):
    
    def __init__(self, T):
        self.T = T 
        self.Tp = None
        self.bases_info = []
        self._decorator_init = None
        self._post_init = None
        pass
    
    def init(self, obj, args, kwargs):
        print("TypeInfo.init")
        self._decorator_init(obj, *args, **kwargs)
        
        if self._post_init is not None:
            self._post_init(obj)
    
    @staticmethod
    def get(T):
        if not hasattr(T, "_typeinfo"):
            setattr(T, "_typeinfo", TypeInfo(T))
        return T._typeinfo
    