from algograph.token import TOKEN, _VTOKEN

import pytest


class IF(TOKEN):
    regex = r'\bif\b'


class ID(_VTOKEN):
    regex = r'[a-zA-Z_][a-zA-Z0-9_]*'


class TestToken:
    def test__eq__(self):
        assert IF() == IF()
        assert IF() != TOKEN()

    def test__repr__(self):
        assert repr(IF()) == 'IF()'


class Test_VToken:
    def test__eq__(self):
        assert ID('proba') == ID('proba')
        assert ID('proba') != ID('p')

    def test__repr__(self):
        assert repr(ID('proba')) == "ID('proba')"
