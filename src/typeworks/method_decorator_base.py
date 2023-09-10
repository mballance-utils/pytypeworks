
import typeworks
from .impl.method_info import MethodInfo
from .impl.method_proxy import MethodProxy
from .impl.typeinfo import TypeInfo
import logging

class MethodDecoratorBase(object):

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.methodinfo = None
        self.T = None
        self.logger = logging.getLogger(type(self).__name__)

    def get_category(self):
        raise Exception("Class %s does not implement get_category" % str(type(self)))

    def pre_decorate(self, T):
        pass

    def decorate(self, T):
        return MethodProxy(T)
    
    def post_decorate(self, T, Tp):
        pass

    def pre_register(self):
        pass

    def post_register(self):
        pass

    def get_methodinfo(self):
        if self.methodinfo is None:
            self.methodinfo = TypeInfo.get(self.T)
        return self.methodinfo

    def __call__(self, T):
        self.T = T

        mi = self.get_methodinfo()

        self.pre_decorate(T)

        mi.Tp = self.decorate(T)

        self.post_decorate(T, mi.Tp)

        self.pre_register()

        from .impl.decl_rgy import DeclRgy
        DeclRgy.push_decl(
            self.get_category(),
            mi,
            typeworks.enclosing_scopename(self.T)
        )
        
        return mi.Tp

