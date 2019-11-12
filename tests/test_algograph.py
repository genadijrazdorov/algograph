from algograph import algo2dot


import pytest


@pytest.fixture
def minimal():
    return 'start; end', \
        '\n'.join(line[12:] for line in \
        '''
            digraph {
                start, end [shape=box style=rounded]
                node [shape=box]

                start -> end
            }
        '''.splitlines()[1:-1])

@pytest.fixture
def complete():
    return '\n'.join(line[12:] for line in \
        '''
            start
            middle
            if question:
                yes
            else:
                no
            end
        '''.splitlines()[1:-1]), \
        '\n'.join(line[12:] for line in \
        '''
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
        '''.splitlines()[1:-1])


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
