
TO = '->'
SPACE = ' '
INDENT = '\t'

DIGRAPH_BEGIN = 'digraph {'
DIGRAPH_END = '}'


def iterlines(algorithm):
    for line in algorithm.splitlines():
        yield from line.split('; ')


def algo2dot(algorithm):
    dot = [DIGRAPH_BEGIN]
    lines = iterlines(algorithm)
    dot.append('\t' + next(lines))

    for line in lines:
        dot[-1] += SPACE + TO + SPACE + line
        dot.append('\t' + line)

    del dot[-1]
    dot.append(DIGRAPH_END)
    return '\n'.join(dot)
