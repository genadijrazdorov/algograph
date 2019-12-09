from algograph.lexer import *

import pytest


def tokenize(doc):
    doc = doc.splitlines()
    if not doc[0].strip():
        doc = doc[1:]
    doc = '\n'.join(line.lstrip()[2:] for line in doc)
    return list(Lexer(doc).tokenize())


class TestLexer:
    def test_start_end(self):
        assert tokenize('| start; end') == [
            IDENTIFIER('start'),
            LITERAL(';'),
            IDENTIFIER('end'),
            NEWLINE()
        ]

    def test_unknown_token(self):
        with pytest.raises(ValueError) as err:
            tokenize('| start; 9 end')

        assert "Unknown token '9' at line 0" in str(err.value)

    def test_newline(self):
        assert tokenize('| start\n|\n| end') == [
            IDENTIFIER('start'),
            NEWLINE(),
            IDENTIFIER('end'),
            NEWLINE()
        ]

    def test_indent_dedent(self):
        assert tokenize('''
                | if q:
                |   y
                | end
            ''') == [
                KEYWORD('if'),
                IDENTIFIER('q'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                IDENTIFIER('y'),
                NEWLINE(),
                DEDENT(2),
                IDENTIFIER('end'),
                NEWLINE()
        ]

    def test_keywords(self):
        assert tokenize('''
                | if q is a:
                |   one
                | elif q is not b:
                |   two
                | else:
                |   three
                | end
            ''') == [
                KEYWORD('if'),
                IDENTIFIER('q'),
                KEYWORD('is'),
                IDENTIFIER('a'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                IDENTIFIER('one'),
                NEWLINE(),
                DEDENT(2),
                KEYWORD('elif'),
                IDENTIFIER('q'),
                KEYWORD('is'),
                KEYWORD('not'),
                IDENTIFIER('b'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                IDENTIFIER('two'),
                NEWLINE(),
                DEDENT(2),
                KEYWORD('else'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                IDENTIFIER('three'),
                NEWLINE(),
                DEDENT(2),
                IDENTIFIER('end'),
                NEWLINE()
        ]
