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
