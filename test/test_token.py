from algograph.token import TOKEN, _VTOKEN

import pytest


class TTOKEN(TOKEN):
    regex = r'\bif\b'


class T_VTOKEN(_VTOKEN):
    regex = r'[a-zA-Z_][a-zA-Z0-9_]*'


class TestToken:
    def test__eq__(self):
        assert TTOKEN() == TTOKEN()
        assert TTOKEN() != TOKEN()

    def test__repr__(self):
        assert repr(TTOKEN()) == 'TTOKEN()'


class Test_VToken:
    def test__eq__(self):
        assert T_VTOKEN('proba') == T_VTOKEN('proba')
        assert T_VTOKEN('proba') != T_VTOKEN('p')

    def test__repr__(self):
        assert repr(T_VTOKEN('proba')) == "T_VTOKEN('proba')"
