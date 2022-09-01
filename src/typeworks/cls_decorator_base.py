
import dataclasses

import typeworks
from typeworks.impl.decl_rgy import DeclRgy
from typeworks.impl.typeinfo import TypeInfo
import typing

class ClsDecoratorBase(object):
    
    IS_SUBCLASS_TYPES = []
    TYPE_PROCESSING_HOOKS = []

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.typeinfo = None
        self.T = None
        
    def get_type_category(self):
        raise Exception("Class %s does not implement get_type_category" % str(type(self)))
    
    def get_type_elab_f(self):
        return None
        
    def pre_decorate(self, T):
        pass
    
    def pre_init_annotated_fields(self):
        pass
    
    def init_annotated_field(self, key, value, has_init):
        pass
    
    def post_init_annotated_fields(self):
        pass
    
    def set_field_initial(self, key, init):
        setattr(self.T, key, init)
        
    def add_field_decl(self, key, type, has_init, init=None):
        if type is None and not has_init:
            raise Exception("add_field_decl requires either a non-None type or an initial value")
        
        if type is not None:
            if not hasattr(self.T, "__annotations__"):
                setattr(self.T, "__annotations__", dict())
            self.T.__annotations__[key] = type
            
        if has_init:
            setattr(self.T, key, init)
    
    def decorate(self, T):
        return dataclasses.dataclass(T, **self.kwargs)
    
    def post_decorate(self, T, Tp):
        pass
    
    def pre_register(self):
        pass
    
    def post_register(self):
        pass
    
    def get_typeinfo(self):
        if self.typeinfo is None:
            self.typeinfo = TypeInfo.get(self.T)
        return self.typeinfo
    
    def __call__(self, T):
        
        self.T = T
        
        print("IS_SUBCLASS_TYPES=%s" % str(type(self).IS_SUBCLASS_TYPES))
        print("  T: %s" % T.__qualname__)

        ti = self.get_typeinfo()
        
        if hasattr(T, "__post_init__"):
            ti._post_init = T.__post_init__
        
        self.pre_decorate(T)

        self.pre_init_annotated_fields()
        local_ns = locals().copy()
        # for name,T in DeclRgy.inner_types.items():
        #     local_ns[name] = T
#        global_ns = globals().copy()
#        for name,T in DeclRgy.inner_types.items():
#            global_ns[name] = T
        # try:
        #     hints =  typing.get_type_hints(
        #         T, 
        #         localns=local_ns,
        #         globalns=global_ns)
        # except Exception as e:
        #     print("Exception: %s" % str(e))
        #     raise e

#        print("hints: %s" % str(hints))
        inner_types = DeclRgy.inner_types
        print("inner_types: %s" % str(inner_types))
        for key,value in getattr(T, "__annotations__", {}).items():
            print("key: %s ; type: %s" % (key, str(type(value))))
            if type(value) is str and value in inner_types.keys():
                print("Intercept %s" % key)
                value = inner_types[value]
#        for key,value in hints.items():
            print("FIELD: %s %s" % (str(key), str(value)))
            self.init_annotated_field(key, value, hasattr(T, key), getattr(T, key, None))
        self.post_init_annotated_fields()
                    
        Tp = self.decorate(T)
        
        ti.Tp = Tp
        ti._decorator_init = Tp.__init__
        
        self.post_decorate(T, Tp)
        
        for m in type(self).TYPE_PROCESSING_HOOKS:
            print("TypeProcessingHook: %s" % str(m))
            m(self, T)
            
        self.pre_register()
            
        typeworks.TypeRgy.register_type(
            self.get_type_category(),
            ti,
            self.get_type_elab_f())
        
        self.post_register()

        # TODO: Check the registered method-based decorators

        # TODO: Check the registered class-based decorators

        # TODO: Check for unrecognized/unsupported decorators

        # TODO: Hand-off to the implementation to 
        # - Manipulate the type and provide the return
        # - Register associated mementos (?)
        
        return Tp
    
