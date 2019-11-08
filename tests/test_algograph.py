from algograph import algo2dot


import pytest


@pytest.fixture
def simple():
    return 'start; end', 'digraph {\n\tstart -> end\n}'


class TestAlgograph:
    @pytest.mark.xfail
    def test_fail(self):
        assert False

    def test_start_end(self, simple):
        algo, dot = simple
        assert algo2dot(algo) == dot
