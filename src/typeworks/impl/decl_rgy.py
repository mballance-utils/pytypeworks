
from typing import Dict, List


class DeclRgyMeta(type):
    
    def __init__(self, name, bases, dct):
        self._decl_m = {}
        self._inner_type_m = {}
        self._scope_decl_m : Dict[str,Dict[object,List[object]]] = {}
        pass
    
    def push_decl(self, key, obj, scope=None):
        if scope not in self._scope_decl_m.keys():
            self._scope_decl_m[scope] = {}
        scope_m = self._scope_decl_m[scope]

        if key not in scope_m.keys():
            scope_m[key] = []
        scope_m[key].append(obj)
        
    def have_decl(self, key):
        return key in self._decl_m.keys() and len(self._decl_m[key]) > 0
    
    def pop_decl(self, key, scope=None):
        ret = []
        if scope is None:
            # Grab from all scopes
            for scope_m in self._scope_decl_m.values():
                if key in scope_m.keys():
                    ret.extend(scope_m[key])
                    scope_m[key].clear()
        else:
            if scope in self._scope_decl_m.keys():
                if key in self._scope_decl_m[scope].keys():
                    ret.extend(self._scope_decl_m[scope][key])
                    self._scope_decl_m[scope][key].clear()
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