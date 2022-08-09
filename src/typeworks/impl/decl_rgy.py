
class DeclRgyMeta(type):
    
    def __init__(self, name, bases, dct):
        self._decl_m = {}
        pass
    
    def push_decl(self, key, obj):
        if key not in self._decl_m.keys():
            self._decl_m[key] = []
        self._decl_m[key].append(obj)
        
    def have_decl(self, key):
        return key in self._decl_m.keys() and len(self._decl_m[key]) > 0
    
    def pop_decl(self, key):
        if key in self._decl_m.keys():
            ret = self._decl_m[key].copy()
            self._decl_m[key].clear()
        else:
            ret = []
        return ret
        
    
    def inst(self):
        return self
    pass

class DeclRgy(metaclass=DeclRgyMeta):
    pass