
class TypeRgy(object):

    _inst = None

    def __init__(self):
        pass

    def load_done(self):
        pass

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst

    @classmethod
    def reset(cls):
        cls._inst = None
