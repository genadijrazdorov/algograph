from algograph.io.graphviz import Graphviz as Gv
from algograph.node import Graph as G, Node as N

import pytest
import xml.etree.ElementTree as ET
import sys


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

    def test_formats(self):
        assert Gv().formats()[:2] == 'bmp canon'.split()

    def test_wrong_format(self, start_end):
        with pytest.raises(ValueError) as err:
            Gv(start_end).run(format='?')

        assert "Wrong '?' format" in str(err.value)

    # @pytest.mark.skipif(sys.platform != 'win32', reason='Applicabile only on win32 platform')
    @pytest.mark.xfail
    def test_graphviz_not_found(self, start_end, monkeypatch):
        monkeypatch.setattr(Gv, 'path', [])

        with pytest.raises(FileNotFoundError):
            Gv(start_end).run()

    def test_tosvg(self, start_end):
        svg = Gv(start_end).tosvg()

        assert isinstance(svg, ET.Element)
        assert svg.tag.endswith('}svg')

    def test_todot(self, start_end):
        dot = Gv(start_end).todot()
        assert 'digraph {' in dot
        assert 'start -> end' in dot

    @pytest.mark.xfail
    def test_tojson(self, start_end):
        json = Gv(start_end).tojson()

        assert False

