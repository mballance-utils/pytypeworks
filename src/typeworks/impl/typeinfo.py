
class TypeInfo(object):
    
    def __init__(self, T):
        self.T = T 
        self.Tp = None
        self.bases_info = []
        self._decorator_init = None
        self._post_init = None
        pass
    
    def init(self, obj, args, kwargs):
        self._decorator_init(obj, *args, **kwargs)
        
        if self._post_init is not None:
            self._post_init(obj)
    
    @staticmethod
    def get(T, create=True):
        if not hasattr(T, "_typeinfo"):
            if create:
                setattr(T, "_typeinfo", TypeInfo(T))
            else:
                return None
        return T._typeinfo
    