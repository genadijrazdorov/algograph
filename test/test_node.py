from algograph.node import Node as N, Graph

import pytest


@pytest.fixture
def start_end():
    return N('start', {N('end'): None})


class TestNode:
    def test_children(self, start_end):
        assert start_end.children == {N('end'): None}

    def test_hash(self, start_end):
        assert hash(start_end) == hash('start')

    def test__eq__(self, start_end):
        assert start_end == N('start')
        assert start_end != N('end')

    def test__lt__(self, start_end):
        assert start_end < N('z')

    def test__len__(self, start_end):
        assert len(start_end) == 1

    def test__iter__(self, start_end):
        assert tuple(iter(start_end)) == tuple({N('end'): None})

    def test__getitem__(self, start_end):
        assert start_end[N('end')] == None

    def test__delitem__(self, start_end):
        del start_end[N('end')]
        assert not start_end.children

    def test__setitem__(self, start_end):
        g = N('start')
        g[N('end')] = None
        assert list(g.children) == list(start_end.children)

    def test__repr__(self, start_end):
        assert repr(start_end) == "<Node 'start'>"


class TestGraph:
    def test__iter__(self, start_end):
        assert list(Graph(start_end)) == [N('start'), N('end')]

    def test__eq__(self, start_end):
        assert Graph(start_end) == Graph(N('start', {N('end'): None}))
        assert Graph(start_end) != Graph(N('start'))
        assert Graph(start_end) != Graph(N('start', {N('end', {N('extra'): None}): None}))
        assert Graph(start_end) != Graph(N('start', {N('end'): True}))

        assert Graph(N('q', {N('y'): True, N('n'): False})) == \
            Graph(N('q', {N('n'): False, N('y'): True}))
