
import typeworks
from .impl.method_info import MethodInfo
from .impl.method_proxy import MethodProxy
from .impl.typeinfo import TypeInfo
import logging
import typing

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

    def register(self, T, Tp):
        vars = T.__code__.co_varnames
        if len(vars) > 0 and vars[0] == "self":
            typeworks.DeclRgy.push_decl(
                self.get_category(),
                Tp,
                typeworks.enclosing_scopename(T))
        else:
            typeworks.TypeRgy.register_method(
                self.get_category(),
                Tp)

    def post_register(self):
        pass

    def get_signature(self):
        rtype = None
        params = []
        ann = self.T.__annotations__

        var_c = self.T.__code__.co_argcount
        dflt_l = [] if self.T.__defaults__ is None else self.T.__defaults__
        vars = self.T.__code__.co_varnames
        if len(vars) > 0 and vars[0] == "self":
            is_method = True
            vars = vars[1:]
        else:
            is_method = False
        for i,var in enumerate(vars):
            type = ann[var] if var in ann.keys() else None
            dflt = dflt_l[i-len(dflt_l)] if (var_c-i-1) < len(dflt_l) else None
            params.append((var,type,dflt))

        if "return" in ann.keys():
            rtype = ann["return"]

        return (is_method, rtype, params)
    
    def validate_hints(self):
        ann = self.T.__annotations__
        vars = self.T.__code__.co_varnames
        if len(vars) > 0 and vars[0] == "self":
            vars = vars[1:]
        for var in vars:
            if var not in ann.keys():
                raise Exception("Parameter %s does not have a type annotation" % var)

    def __call__(self, T):
        self.T = T

        self.pre_decorate(T)

        Tp = self.decorate(T)

        self.post_decorate(T, Tp)

        self.pre_register()

        self.register(T, Tp)

        self.post_register()

        return Tp

