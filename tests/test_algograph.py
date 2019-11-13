from algograph import algo2dot


import pytest

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
    return 'start; end', lstrip('''
            digraph {
                start, end [shape=box style=rounded]
                node [shape=box]

                start -> end
            }
    ''')

@pytest.fixture
def complete():
    return lstrip('''
            start
            middle
            if question:
                yes
            else:
                no
            end
        '''), lstrip('''
            digraph {
                start, end [shape=box style=rounded]
                node [shape=box]
                question [shape=diamond]

                start -> middle
                middle -> question
                question -> yes [label=yes]
                question -> no [label=no]
                yes -> end
                no -> end
            }
        ''')

@pytest.fixture
def elif_():
    return lstrip('''
                        start
                        if question:
                            yes
                        elif other_question:
                            other_yes
                        end
        '''), lstrip('''
            digraph {
                start, end [shape=box style=rounded]
                node [shape=box]
                question, other_question [shape=diamond]

                start -> question
                question -> yes [label=yes]
                question -> other_question [label=no]
                other_question -> other_yes [label=yes]
                other_question -> end [label=no]
                other_yes -> end
                yes -> end
            }
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
