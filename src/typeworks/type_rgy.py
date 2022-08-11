
from typing import Any, Dict, Tuple
from .impl.typeinfo import TypeInfo


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
    
    def __init__(self, name, bases, dct):
        self.type_category_m : Dict[Any,TypeRgyMeta.TypeCategory]= {}
        self.is_elab = False
    
    def elab(self, category=None):
        if self.is_elab:
            return
        
        if category is not None:
            if category in self.type_category_m.keys():
                self.type_category_m[category].elab()
        else:
            for key,val in self.type_category_m.items():
                val.elab()
            self.is_elab = True
    
    def inst(self):
        return self
    
    def reset(self):
        self.type_category_m.clear()
        self.is_elab = False
        pass
    
    def register_type(self, category, T : TypeInfo, elab_f=None):
        if category not in self.type_category_m.keys():
            self.type_category_m[category] = TypeRgyMeta.TypeCategory(category)
        self.type_category_m[category].register_type(T, elab_f)
        
    def get_categories(self):
        return list(self.type_category_m.keys())
    
    def get_types(self, category):
        if category in self.type_category_m.keys():
            return self.type_category_m[category].get_types()
        else:
            return []
        
class TypeRgy(metaclass=TypeRgyMeta):
    pass

