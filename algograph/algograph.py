import itertools

TO = '->'
SPACE = ' '
INDENT = ' ' * 4

COLON = ':'
SEMI = ';'
PUNCT = {COLON, SEMI}

IF = 'IF'
ELSE = 'ELSE'
ELIF = 'ELIF'
KEYWORDS = {IF, ELSE, ELIF}

COMMA = ', '
YES = '[label=yes]'
NO = '[label=no]'

DIGRAPH_BEGIN = 'digraph {'
DIGRAPH_END = '}'


def iterrawtoken(algorithm):
    lines = [line for line in algorithm.splitlines() if line.strip()]
    old = len(list(itertools.takewhile(str.isspace, lines[0].expandtabs())))
    level = 0

    for line in lines:
        indent = len(list(itertools.takewhile(str.isspace, line.expandtabs())))
        if indent > old:
            level += 1
        elif indent < old:
            level -= 1

        tokens = line.strip().split()
        colon_inline = False

        for token in tokens:
            punct = None
            if token[-1] in PUNCT:
                token, punct = token[:-1], token[-1]

            if token.upper() in KEYWORDS:
                yield level, token.upper(), None

            else:
                yield level, 'ID', token

            if punct == COLON:
                yield level, 'PUNCT', COLON
                level += 1
                colon_inline = True

            elif punct == SEMI:
                yield level, 'PUNCT', SEMI

        if colon_inline:
            level -= 1

        old = indent


def itertoken(algorithm):
    tokens = iterrawtoken(algorithm)

    while True:
        try:
            level, token, value = next(tokens)
        except StopIteration:
            break

        if token == IF or token == ELIF:
            value = next(tokens)[2]
            next(tokens)    # COLON

        elif token == ELSE:
            next(tokens)    # COLON

        elif token == 'PUNCT':
            continue

        yield level, token, value


def algo2dot(algorithm):
    dot = []

    tokens = itertoken(algorithm)

    previous = 0, None, None
    branching = []
    branch = None
    types = {
        'terminator': [],
        'decision': []
    }

    while True:
        try:
            level, token, value = next(tokens)
        except StopIteration:
            break

        if token == 'IF':
            _, _, value = next(tokens)
            branching.append((level, token, value))
            types['decision'].append(value)
            branch = True
            next(tokens)    # COLON

        elif token == 'ELSE':
            previous, branching[-1] = branching[-1], previous
            branch = False
            next(tokens)    # COLON
            continue

        elif token == 'SEMI':
            continue

        if level < previous[0]:
            dot.append((branching.pop()[2], TO, value))

        if branch and previous[1] == 'IF':
            dot.append((previous[2], TO, value, YES))
            branch = None

        elif branch is False:
            dot.append((previous[2], TO, value, NO))
            branch = None

        else:
            dot.append((previous[2], TO, value))

        previous = level, token, value

    del dot[0]
    types['terminator'].append(dot[0][0])
    types['terminator'].append(dot[-1][2])

    dot = [INDENT + SPACE.join(line) for line in dot]
    for type_ in 'terminator decision'.split():
        types[type_] = COMMA.join(types[type_])

    header = [INDENT + '{} [shape=box style=rounded]'.format(types['terminator']),
              INDENT + 'node [shape=box]'
    ]
    if types['decision']:
        header.append(
              INDENT + '{} [shape=diamond]'.format(types['decision'])
        )
    header.append('')

    return '\n'.join([DIGRAPH_BEGIN] + header + dot + [DIGRAPH_END])
