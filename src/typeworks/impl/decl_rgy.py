
class DeclRgyMeta(type):
    
    def __init__(self, name, bases, dct):
        self._decl_m = {}
        self._inner_type_m = {}
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

    def add_inner_type(self, T):
        print("Add name: %s" % T.__name__)
#        self._inner_type_m[T.__name__] = T
        qname_l = T.__qualname__.split('.')
        i = len(qname_l)-1

        while i >= 0:
            if qname_l[i] == "<locals>":
                break
            name = ".".join(qname_l[i:])
            self._inner_type_m[name] = T
            i -= 1

    @property
    def inner_types(self):
        return self._inner_type_m

    def clear_inner_types(self):
        self._inner_type_m.clear()
        
    
    def inst(self):
        return self
    pass

class DeclRgy(metaclass=DeclRgyMeta):
    pass