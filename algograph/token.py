class TOKEN:
    tokens = {}
    regex = None

    def __init__(self, value=None):
        super().__init__()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__[0] != "_":
            cls.tokens[cls.__name__] = cls

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class _VTOKEN(TOKEN):
    def __init__(self, value=None):
        super().__init__()
        self.value = value

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.value)

    def __eq__(self, other):
        return super().__eq__(other) and self.value == other.value
