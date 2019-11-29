from algograph.token import TOKEN, _VTOKEN, _DTOKEN

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


@pytest.fixture
def expr():
    class EXPR(_DTOKEN):
        def __init__(self, id_, not_=False):
            super().__init__(id_, not_)
            self.ID = id_
            self.NOT = not_

    return EXPR


class TestTOKEN:
    def test__eq__(self, if_):
        assert if_() == if_()
        assert if_() != TOKEN()

    def test__repr__(self, if_):
        assert repr(if_()) == 'IF()'


class Test_VTOKEN:
    def test__eq__(self, id_):
        assert id_('proba') == id_('proba')
        assert id_('proba') != id_('p')

    def test__repr__(self, id_):
        assert repr(id_('proba')) == "ID('proba')"


class Test_DTOKEN:
    def test__eq__(self, expr, id_):
        assert expr(id_('proba')) == expr(id_('proba'))
        assert expr(id_('proba')) != expr(id_('p'))

    def test__repr__(self, expr, id_):
        assert repr(expr(id_('proba'))) == "EXPR(ID('proba'), False)"

