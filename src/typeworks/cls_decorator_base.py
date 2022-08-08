
import dataclasses

from typeworks.impl.typeinfo import TypeInfo

class ClsDecoratorBase(object):
    
    IS_SUBCLASS_TYPES = []
    TYPE_PROCESSING_HOOKS = []

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.typeinfo = None
        self.T = None
        
    def pre_decorate(self, T):
        pass
    
    def init_annotated_field(self, key, value, has_init):
        pass
    
    def set_field_initial(self, key, init):
        setattr(self.T, key, init)
    
    def decorate(self, T):
        return dataclasses.dataclass(T, **self.kwargs)
    
    def post_decorate(self, T, Tp):
        pass
    
    def get_typeinfo(self):
        if self.typeinfo is None:
            self.typeinfo = TypeInfo.get(self.T)
        return self.typeinfo
    
    def __call__(self, T):
        
        self.T = T
        
        print("IS_SUBCLASS_TYPES=%s" % str(type(self).IS_SUBCLASS_TYPES))

        ti = self.get_typeinfo()
        
        if hasattr(T, "__post_init__"):
            ti._post_init = T.__post_init__
        
        self.pre_decorate(T)
        
        for key,value in getattr(T, "__annotations__", {}).items():
            self.init_annotated_field(key, value, hasattr(T, key))
            # if not hasattr(T, key):
            #     print("key=%s value=%s" % (str(key), str(value)))
            #     found = False
                
            #     for sc in type(self).IS_SUBCLASS_TYPES:
            #         if issubclass(value, sc[0]):
            #             print("is subclass of %s default=%s" % (str(sc[0]), str(sc[1])))
            #             setattr(T, key, dataclasses.field(init=False, default=sc[1]))
            #             found = True
            #             break
                    
        Tp = self.decorate(T)
        
        ti.Tp = Tp
        ti._decorator_init = Tp.__init__
        
        self.post_decorate(T, Tp)
        
        for m in type(self).TYPE_PROCESSING_HOOKS:
            print("TypeProcessingHook: %s" % str(m))
            m(self, T)

        # TODO: Check the registered method-based decorators

        # TODO: Check the registered class-based decorators

        # TODO: Check for unrecognized/unsupported decorators

        # TODO: Hand-off to the implementation to 
        # - Manipulate the type and provide the return
        # - Register associated mementos (?)
        
        return Tp
    
