from algograph.token import NEWLINE
from algograph.parser import Parser, RULE
from algograph.node import Node as N, Graph as G

from .test_token import id_

import pytest


def parse(doc):
    doc = doc.splitlines()
    if not doc[0].strip():
        doc = doc[1:]
    doc = [line.lstrip()[2:] for line in doc]
    doc = '\n'.join(doc)
    return Parser(doc + '\n').parse()


@pytest.fixture
def start_end():
    return 'start; end', G(N('start', {N('end'): None}))


@pytest.fixture
def expr():
    class EXPR(RULE):
        def __init__(self, id_, not_=False):
            super().__init__(id_, not_)
            self.ID = id_
            self.NOT = not_

    return EXPR


class Test_RULE:
    def test__eq__(self, expr, id_):
        assert expr(id_('proba')) == expr(id_('proba'))
        assert expr(id_('proba')) != expr(id_('p'))
        assert expr(id_('proba')) != NEWLINE()

    def test__repr__(self, expr, id_):
        assert repr(expr(id_('proba'))) == "EXPR(ID('proba'), False)"


class TestParser:
    def test_start_end(self, start_end):
        algo, graph = start_end
        assert Parser(algo).parse() == graph

    def test_if(self):
        assert parse('''
                     | if q:
                     |   y
                     ''') == G(N('q', {N('y'): True}))

    def test_multistatemnt_suite(self):
        assert parse('''
                     | if q:
                     |   first
                     |   second
                     ''') == G(N('q', {N('first', {N('second'): None}): True}))

    def test_multilevel_suite(self):
        assert parse('''
                     | if q:
                     |   if q2:
                     |     first
                     |     second
                     ''') == G(N('q', {N('q2', {N('first', {N('second'): None}): True}): True}))

    def test_if_not(self):
        assert parse('''
                     | if not q:
                     |   y
                     ''') == G(N('q', {N('y'): False}))

    def test_suite_error(self):
        with pytest.raises(SyntaxError):
            parse('''
                     | if q:
                     |   y
                     |  e
            ''')

    def test_if_error(self):
        with pytest.raises(SyntaxError):
            parse('''
                     | q
                     |   y
                     | e
            ''')

    def test_if_else(self):
        assert parse('''
                     | if q:
                     |   y
                     | else:
                     |   n
                     ''') == G(N('q', {N('y'): True, N('n'): False}))

    def test_if_elif_elif_else(self):
        assert parse('''
                     | if q:
                     |   y
                     | elif q2:
                     |   y2
                     | elif q3:
                     |   y3
                     | else:
                     |   n
                     ''') == \
                    G(N('q', {
                        N('y'): True,
                        N('q2', {
                            N('y2'): True,
                            N('q3', {
                                N('y3'): True,
                                N('n'): False
                            }): False
                        }): False
                    }))

    def test_if_is(self):
        assert parse('''
                     | if s is o1:
                     |   y10
                     |   y11
                     | elif s is o2:
                     |   y2
                     | elif s is o3:
                     |   y3
                     | else:
                     |   n
                     ''') == \
                    G(N('s', {
                        N('y10', {N('y11'): None}): 'o1',
                        N('y2'): 'o2',
                        N('y3'): 'o3',
                        N('n'): False
                    }))
