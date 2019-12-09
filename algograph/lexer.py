from .token import *

import re


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
            yield INDENT(indent - old)

        elif indent < old:
            yield DEDENT(old - indent)

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
