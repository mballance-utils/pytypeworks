
import imp
from .type_rgy import TypeRgy
from .cls_decorator_base import *
from .registration_decorator_base import *
from .impl.decl_rgy import DeclRgy
from .type_rgy import TypeRgy
from .impl.typeinfo import TypeInfo


def reset():
    """
    Resets the library to its initial state. Primarily used by tests
    """
    TypeRgy.reset()

def load_done():
    """
    Performs post-load elaboration activity
    """
    TypeRgy.inst().load_done()

