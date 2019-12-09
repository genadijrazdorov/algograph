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
            ID('start'),
            LITERAL(';'),
            ID('end'),
            NEWLINE()
        ]

    def test_unknown_token(self):
        with pytest.raises(ValueError) as err:
            tokenize('| start; 9 end')

        assert "Unknown token '9' at line 0" in str(err.value)

    def test_newline(self):
        assert tokenize('| start\n|\n| end') == [
            ID('start'),
            NEWLINE(),
            ID('end'),
            NEWLINE()
        ]

    def test_indent_dedent(self):
        assert tokenize('''
                | if q:
                |   y
                | end
            ''') == [
                IF(),
                ID('q'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                ID('y'),
                NEWLINE(),
                DEDENT(2),
                ID('end'),
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
                IF(),
                ID('q'),
                IS(),
                ID('a'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                ID('one'),
                NEWLINE(),
                DEDENT(2),
                ELIF(),
                ID('q'),
                IS(),
                NOT(),
                ID('b'),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                ID('two'),
                NEWLINE(),
                DEDENT(2),
                ELSE(),
                LITERAL(':'),
                NEWLINE(),
                INDENT(2),
                ID('three'),
                NEWLINE(),
                DEDENT(2),
                ID('end'),
                NEWLINE()
        ]
