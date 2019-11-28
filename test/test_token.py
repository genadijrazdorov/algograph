from algograph.token import TOKEN, _VTOKEN

import pytest


@pytest.fixture
def if_():
    class IF(TOKEN):
        regex = r'\bif\b'

    return IF


@pytest.fixture
def id_():
    class ID(_VTOKEN):
        regex = r'[a-zA-Z_][a-zA-Z0-9_]*'

    return ID


class TestToken:
    def test__eq__(self, if_):
        assert if_() == if_()
        assert if_() != TOKEN()

    def test__repr__(self, if_):
        assert repr(if_()) == 'IF()'


class Test_VToken:
    def test__eq__(self, id_):
        assert id_('proba') == id_('proba')
        assert id_('proba') != id_('p')

    def test__repr__(self, id_):
        assert repr(id_('proba')) == "ID('proba')"
