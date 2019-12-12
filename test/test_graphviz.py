from algograph.io.graphviz import Graphviz as Gv
from algograph.node import Graph as G, Node as N

import pytest


def equalize(text):
    return ' '.join(text.strip().split())


class TestGraphviz:
    @pytest.mark.xfail
    def test_fail(self):
        assert False

    def test_run(self):
        graph = G(N('start', {N('end'): None}))
        result = Gv(graph).run()
        result = equalize(result.stdout)
        assert result == equalize(r'''
            digraph {
                node [label="\N"];
                start -> end;
            }
        ''')
