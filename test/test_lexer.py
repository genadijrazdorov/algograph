from algograph.lexer import Lexer, ID, LITERAL

import pytest


class TestLexer:
    def test_start_end(self):
        assert list(Lexer('start; end').tokenize()) == [
            ID('start'),
            LITERAL(';'),
            ID('end')
        ]

    ## def test_keywords(self):
    ##     assert list(tokenizer('\n'.join(line.strip()[2:] for line in '''
    ##         | if question:
    ##         |     yes
    ##         | else:
    ##         |     no
    ##         | middle
    ##     '''.splitlines()[1:-1]))) == [
    ##         KEYWORD('if'),
    ##         ID('question'),
    ##         PUNCT(':'),
    ##         ID('yes'),
    ##         KEYWORD('else'),
    ##         PUNCT(':'),
    ##         ID('no'),
    ##         ID('middle')
    ##     ]

