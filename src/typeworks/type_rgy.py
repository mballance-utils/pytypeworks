
from typing import Any, Dict, Tuple
from .impl.typeinfo import TypeInfo
from .impl.method_proxy import MethodProxy


class TypeRgyMeta(type):
    
    class TypeCategory(object):
        
        def __init__(self, category):
            self.category = category
            self.is_elab = False
            self.type_m : Dict[Any,Tuple[TypeInfo,callable]]= {}
        
        def elab(self):
            if self.is_elab:
                return
            
            for T,elab_f in self.type_m.values():
                if elab_f is not None:
                    elab_f(T)
            
            self.is_elab = True
            
        def get_types(self):
            return list(map(lambda val: val[0], self.type_m.values()))
            
        def register_type(self, ti : TypeInfo, elab_f):
            if ti.T in self.type_m.keys():
                raise Exception("Duplicate type %s registered" % ti.T.__qualname__)
            self.type_m[ti.T] = (ti, elab_f)

    class MethodCategory(object):

        def __init__(self, category):
            self.category = category
            self.is_elab = False
            self.method_m = {}

        def register_method(self, T : MethodProxy):
            if T in self.method_m.keys():
                raise Exception("Duplicate method %s registered" % T.__qualname__)
            self.method_m[T] = T

        def get_methods(self):
            return list(self.method_m.values())
    
    def __init__(self, name, bases, dct):
        self.type_category_m : Dict[Any,TypeRgyMeta.TypeCategory] = {}
        self.method_category_m : Dict[Any,TypeRgyMeta.MethodCategory] = {}
        self.is_elab = False
    
    def elab(self, category=None):
        if self.is_elab:
            return
        
        if category is not None:
            if category in self.type_category_m.keys():
                self.type_category_m[category].elab()
            if category in self.method_category_m.keys():
                self.method_category_m[category].elab()
        else:
            for key,val in self.type_category_m.items():
                val.elab()
            for key,val in self.method_category_m.items():
                val.elab()
            self.is_elab = True
    
    def inst(self):
        return self
    
    def reset(self):
        self.type_category_m.clear()
        self.is_elab = False

    def register_method(self, category, T):
        if category not in self.method_category_m.keys():
            self.method_category_m[category] = TypeRgyMeta.MethodCategory(category)
        self.method_category_m[category].register_method(T)
    
    def register_type(self, category, T : TypeInfo, elab_f=None):
        if category not in self.type_category_m.keys():
            self.type_category_m[category] = TypeRgyMeta.TypeCategory(category)
        self.type_category_m[category].register_type(T, elab_f)
        
    def get_categories(self):
        return list(self.type_category_m.keys())
    
    def get_methods(self, category=None):
        if category is None:
            ret = []
            for key in  self.method_category_m.keys():
                ret.extend(self.method_category_m[key].get_methods())
            return ret
        elif category in self.method_category_m.keys():
            return self.method_category_m[category].get_methods()
        else:
            return []

    def get_types(self, category):
        if category in self.type_category_m.keys():
            return self.type_category_m[category].get_types()
        else:
            return []
        
        
class TypeRgy(metaclass=TypeRgyMeta):
    pass

