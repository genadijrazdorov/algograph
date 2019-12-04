from algograph.node import Graph as G, Node as N
from algograph.io.dot import DOT

import pytest


def lstrip(string):
    return '\n'.join(line.lstrip()[2:] for line in string.splitlines()[1:-1])

class TestDOT:
    @pytest.mark.xfail
    def test_fail(self):
        assert False

    def test_start_end(self):
        assert DOT(G(N('start', {N('end'): None}))).encode() == \
            lstrip('''
                | digraph {
                |   start -> end
                | }
            ''')

    def test_if_else(self):
        assert DOT(G(N('q', {N('y'): True, N('n'): False}))).encode() == \
            lstrip('''
                   | digraph {
                   |   q -> y [label=True]
                   |   q -> n [label=False]
                   | }
            ''')
