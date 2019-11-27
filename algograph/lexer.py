from .token import TOKEN, _VTOKEN

import re

__all__ = 'Lexer IF IS ELIF ELSE ID LITERAL NEWLINE INDENT DEDENT IGNORE'.split()


class IF(TOKEN):
    regex = r'\bif\b'


class IS(TOKEN):
    regex = r'\bis\b'


class ELIF(TOKEN):
    regex = r'\belif\b'


class ELSE(TOKEN):
    regex = r'\belse\b'


class ID(_VTOKEN):
    regex = r'[a-zA-Z_][a-zA-Z0-9_]*'


class LITERAL(_VTOKEN):
    regex = r'[:;]'


class NEWLINE(TOKEN):
    regex = r'\n+\s*'


class INDENT(_VTOKEN):
    pass


class DEDENT(_VTOKEN):
    pass


class IGNORE(_VTOKEN):
    regex = r'\s+|#.*'


class Lexer:
    def __init__(self, doc):
        self.doc = doc

    def newline(self, value):
        value = value.expandtabs()
        indent = len(value.lstrip('\n'))
        newlines = len(value) - indent

        self.line += newlines
        yield NEWLINE()

        old, self.indent = self.indent, indent

        if indent > old:
            yield INDENT(indent)

        elif indent < old:
            yield DEDENT(indent)

    def ignore(self, value):
        return []

    def tokenize(self):
        regex = []
        for token, cls in TOKEN.tokens.items():
            if cls.regex:
                regex.append('(?P<{}>{})'.format(token, cls.regex))
        regex = '|'.join(regex)

        self.indent = indent = 0
        self.line = line = 0
        self.index = index = 0

        try:
            for match in re.finditer(regex, self.doc + '\n'):
                token = match.lastgroup
                value = match.group(token)

                assert match.start() == index
                index = match.end()

                try:
                    yield from getattr(self, token.lower())(value)

                except AttributeError:
                    yield TOKEN.tokens[token](value)

        except AssertionError:
            unknown = self.doc[index: match.start()]
            message = "Unknown token '{}' at line {}"
            raise ValueError(message.format(unknown, line))
