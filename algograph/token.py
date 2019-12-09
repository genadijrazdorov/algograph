__all__ = '''
    TOKEN
    KEYWORD
    IDENTIFIER
    LITERAL
    NEWLINE
    INDENT
    DEDENT
    IGNORE
'''.split()


class TOKEN:
    '''a string with lexical meaning

    > A lexical token or simply token is a string with an assigned and thus
    identified meaning. (Wikipedia)

    '''
    tokens = {}
    regex = None

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, value=None):
        self.value = value

    def __hash__(self):
        return hash((self.name, self.value))

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__[0] != "_":
            cls.tokens[cls.__name__] = cls

    def __repr__(self):
        if self.value is None:
            return '{s.name}()'.format(s=self)
        else:
            return "{s.name}({s.value!r})".format(s=self)

    def __eq__(self, other):
        try:
            return (self.name, self.value) == (other.name, other.value)

        except AttributeError:
            return NotImplemented


class KEYWORD(TOKEN):
    regex = r'\b(?:' + r'|'.join('if is not elif else'.split()) + r')'


class IDENTIFIER(TOKEN):
    regex = r'[a-zA-Z_][a-zA-Z0-9_]*'


class LITERAL(TOKEN):
    regex = r'[:;]'


class NEWLINE(TOKEN):
    regex = r'\n+\s*'


class INDENT(TOKEN):
    pass


class DEDENT(TOKEN):
    pass


class IGNORE(TOKEN):
    regex = r'\s+|#.*'



