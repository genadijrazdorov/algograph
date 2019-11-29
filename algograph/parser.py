from .lexer import *
from .token import _DTOKEN
from .node import Node as N


NEWLINE = NEWLINE()
IS = IS()
NOT = NOT()
ELSE = ELSE()
IF = IF()
ELIF = ELIF()

SEMI = LITERAL(';')
COLON = LITERAL(':')


class STMT(_DTOKEN):
    def __init__(self, id_):
        super().__init__(id_)
        self.ID = id_


class EXPR(_DTOKEN):
    def __init__(self, id_, not_=False):
        super().__init__(id_, not_)
        self.ID = id_
        self.NOT = not_


class IS_EXPR(_DTOKEN):
    def __init__(self, id_, expr):
        super().__init__(id_, expr)
        self.ID = id_
        self.EXPR = expr


class SUITE(_DTOKEN):
    pass


class SWITCH(_DTOKEN):
    def __init__(self, is_expr, suite, elif_=None, else_=None):
        super().__init__(is_expr, suite, elif_, else_)
        self.IS_EXPR = is_expr
        self.SUITE = suite
        self.ELIF = elif_
        self.ELSE = else_


class IF_STMT(_DTOKEN):
    def __init__(self, expr, suite, elif_=None, else_=None):
        super().__init__(expr, suite, elif_, else_)
        self.EXPR = expr
        self.SUITE = suite
        self.ELIF = elif_
        self.ELSE = else_


class Parser:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.tokens = Lexer(algorithm).tokenize()

    def reduce(self):
        '''
            BRANCH  = IF_STMT | SWITCH
            IF_STMT = IF EXPR SUITE {ELIF EXPR SUITE} [ELSE SUITE]
            SWITCH  = IF IS_EXPR SUITE {ELIF IS_EXPR SUITE} [ELSE SUITE]
            IS_EXPR = ID IS EXPR
            EXPR    = [NOT] ID COLON NEWLINE
            SUITE   = INDENT STMT+ DEDENT
            STMT    = ID NEWLINE | BRANCH
            ELSE    = "else" COLON NEWLINE
            COLON   = ":"
        '''

        stack = self.stack
        token = stack[-1]

        # SEMI
        if token == SEMI:
            token = stack[-1] = NEWLINE

        # ELSE
        if stack[-3:] == [ELSE, COLON, NEWLINE]:
            del stack[-2:]

        # EXPR
        elif stack[-2:] == [COLON, NEWLINE]:
            id_ = stack[-3]
            not_ = (stack[-4] == NOT)
            token = EXPR(id_, not_)
            stack[-3 - not_:] = [token]

        # STMT
        elif stack[-1] == NEWLINE and isinstance(stack[-2], ID):
            token = STMT(stack[-2])
            stack[-2:] = [token]

        # IS_EXPR
        if stack[-2] == IS and isinstance(token, EXPR):
            id_ = stack[-3]
            token = IS_EXPR(id_, token)
            stack[-3:] = [token]

        # SUITE
        if isinstance(token, DEDENT):
            for i in range(len(stack)):
                i += 1
                if isinstance(stack[-i], INDENT):
                    break
            else:
                raise SyntaxError

            token = SUITE(*stack[-i + 1: -1])
            stack[-i:] = [token]

        # IF/SWITCH
        if token not in {ELIF, ELSE} and isinstance(stack[-2], SUITE):
            for i in range(2, len(stack) - 1):
                if stack[-i] == IF:
                    break
            else:
                raise SytaxError

            ifswitch = stack[-i: -1]

            else_ = None
            if ifswitch[-2] == ELSE:
                else_ = ifswitch.pop()
                ifswitch.pop()

            expr = ifswitch[1]
            suite = ifswitch[2]
            del ifswitch[:3]

            elif_ = list(zip(ifswitch[1::3], ifswitch[2::3]))

            if isinstance(expr, IS_EXPR):
                stack[-i: -1] = [SWITCH(expr, suite, elif_, else_)]

            else:
                stack[-i: -1] = [IF_STMT(expr, suite, elif_, else_)]

    def consume(self):
        stack = self.stack
        last = self.last

        if isinstance(stack[2], STMT):
            node = N(stack[2].ID.value)
            last[node] = None
            last = node
            del stack[2]

        elif isinstance(stack[2], IF_STMT):
            node = N(stack[2].EXPR.ID.value)
            yes = N(stack[2].SUITE.tokens[0])
            for t in stack[2].SUITE.tokens[1:]:
                yes[N(t.value)] = None
            node[yes] = True
            last[node] = None
            last = node
            del stack[2]

        elif isinstance(stack[2], SWITCH):
            pass

    def parse(self):
        top = self.last = N('top')
        sink = N('sink')
        stack = self.stack = [None, None]

        for token in self.tokens:
            stack.append(token)
            self.reduce()
            self.consume()

        # if last token is SUITE
        stack.append(NEWLINE)
        self.reduce()
        self.consume()

        del stack[:2], stack[-1]
        assert not stack
        return next(iter(top))
