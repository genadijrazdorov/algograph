from algograph.parser import Parser
from algograph.node import Node as N

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
    return 'start; end', N('start', {N('end'): None})


class TestParser:
    def test_start_end(self, start_end):
        algo, graph = start_end
        assert Parser(algo).parse() == graph

    def test_if(self):
        assert parse('''
                     | if q:
                     |   y
                     ''') == N('q', {N('y'): True})

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
                     ''') == N('q', {N('y'): True, N('n'): False})

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
                    N('q', {
                        N('y'): True,
                        N('q2', {
                            N('y2'): True,
                            N('q3', {
                                N('y3'): True,
                                N('n'): False
                            }): False
                        }): False
                    })

    def test_if_is(self):
        assert parse('''
                     | if s is o1:
                     |   y1
                     | elif s is o2:
                     |   y2
                     | elif s is o3:
                     |   y3
                     | else:
                     |   n
                     ''') == \
                    N('s', {
                        N('y1'): 'o1',
                        N('y2'): 'o2',
                        N('y3'): 'o3',
                        N('n'): False
                    })
