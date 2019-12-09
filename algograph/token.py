class TOKEN:
    tokens = {}
    regex = None

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, value=None):
        super().__init__()

    def __hash__(self):
        return hash(self.__class__)

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

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "{s.__class__.__name__}('{s.value}')".format(s=self)

    def __eq__(self, other):
        return super().__eq__(other) and self.value == other.value


class _DTOKEN(TOKEN):
    def __init__(self, *tokens):
        super().__init__()
        self.tokens = tokens

    def __hash__(self):
        return hash(self.tokens)

    def __repr__(self):
        tokens = ', '.join(str(t) for t in self.tokens)
        return "{s.__class__.__name__}({t})".format(s=self, t=tokens)

    def __eq__(self, other):
        return super().__eq__(other) and self.tokens == other.tokens


