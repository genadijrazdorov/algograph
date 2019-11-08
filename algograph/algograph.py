
TO = ' -> '

def iterlines(algorithm):
    for line in algorithm.splitlines():
        yield from line.split('; ')

def algo2dot(algorithm):
    dot = ['digraph {']
    lines = iterlines(algorithm)
    dot.append('\t' + next(lines))

    for line in lines:
        dot[-1] += TO + line
        dot.append('\t' + line)

    del dot[-1]
    dot.append('}')
    return '\n'.join(dot)
