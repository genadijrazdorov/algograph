from algograph.token import TOKEN

import pytest


@pytest.fixture
def keyword():
    class KEYWORD(TOKEN):
        regex = r'\bif\b'

    return KEYWORD


@pytest.fixture
def id_():
    class ID(TOKEN):
        regex = r'[a-zA-Z_][a-zA-Z0-9_]*'

    return ID


class TestTOKEN:
    def test_name(self, keyword):
        assert keyword().name == 'KEYWORD'

    def test__eq__(self, keyword, id_):
        assert keyword() == keyword()
        assert keyword() != TOKEN()
        assert keyword() != None

        assert id_('proba') == id_('proba')
        assert id_('proba') != id_('p')


    def test__repr__(self, keyword, id_):
        assert repr(keyword('if')) == "KEYWORD('if')"
        assert repr(id_('proba')) == "ID('proba')"
