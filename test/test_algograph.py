from algograph import algo2dot


import pytest

_algo2dot = algo2dot

def algo2dot(algorithm):
    algorithm = algorithm.splitlines()
    algorithm.insert(0, 'start')
    algorithm.append('end')
    algorithm = '\n'.join(algorithm)

    dot = _algo2dot(algorithm)

    dot = [line[4:] for line in dot.splitlines()[1:-1]]

    dot.remove('start, end [shape=box style=rounded]')
    dot.remove('node [shape=box]')
    if not dot[0]:
        del dot[0]

    dot = [line for line in dot if 'start' not in line]
    dot = [line for line in dot if 'end' not in line]

    return '\n'.join(dot)

def lstrip(string):
    string = string.expandtabs()
    lines = iter(string.splitlines())
    line = next(lines)
    while not line.strip():
        line = next(lines)
    indent = len(line) - len(line.lstrip())
    return '\n'.join(line[indent:] for line in string.splitlines()[1:-1])

@pytest.fixture
def minimal():
    return 'first; second', lstrip('''
                first -> second
    ''')

@pytest.fixture
def complete():
    return lstrip('''
            middle
            if question:
                yes
            else:
                no
        '''), lstrip('''
            question [shape=diamond]

            middle -> question
            question -> yes [label=yes]
            question -> no [label=no]
        ''')

@pytest.fixture
def elif_():
    return lstrip('''
            if question:
                yes
            elif other_question:
                other_yes
        '''), lstrip('''
            question, other_question [shape=diamond]

            question -> yes [label=yes]
            question -> other_question [label=no]
            other_question -> other_yes [label=yes]
        ''')


class TestAlgograph:
    @pytest.mark.xfail
    def test_fail(self):
        assert False

    def test_start_end(self, minimal):
        algo, dot = minimal
        assert algo2dot(algo) == dot

    def test_complete(self, complete):
        algo, dot = complete
        assert algo2dot(algo) == dot

    def test_elif(self, elif_):
        algo, dot = elif_
        assert algo2dot(algo) == dot
