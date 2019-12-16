from algograph.io.graphviz import Graphviz as Gv
from algograph.node import Graph as G, Node as N

import pytest


def equalize(text):
    return ' '.join(text.strip().split())


@pytest.fixture
def start_end():
    return G(N('start', {N('end'): None}))


class TestGraphviz:
    @pytest.mark.xfail
    def test_fail(self):
        assert False

    def test_empty_graph(self):
        assert Gv().dot() == ''

    def test_start_end(self, start_end):
        graph = start_end
        dot = Gv(graph).run(format='canon')
        result = equalize(dot)
        assert result == equalize(r'''
            digraph {
                node [label="\N"];
                start -> end;
            }
        ''')

    def test_graphviz_not_found(self, start_end, monkeypatch):
        monkeypatch.setattr(Gv, 'path', [])

        with pytest.raises(FileNotFoundError):
            Gv(start_end).run()
