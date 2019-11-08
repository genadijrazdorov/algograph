import algograph


import pytest


class TestAlgograph:
    @pytest.mark.xfail
    def test_fail(self):
        algograph
        assert False
