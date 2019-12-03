from algograph.node import Node as N

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
