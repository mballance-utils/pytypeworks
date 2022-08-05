
from .type_rgy import TypeRgy


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

