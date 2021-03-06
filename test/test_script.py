from algograph.script import script, DESCRIPTION

import pytest

import sys
import io


@pytest.fixture(scope="session")
def startendfile(tmp_path_factory):
    path = tmp_path_factory.mktemp('algograph')
    path = path.joinpath('startend.py')
    path.write_text('start; end')
    return path


def run(args, input=None):
    argv = sys.argv
    sys.argv = args
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    if input:
        sys.stdin = io.StringIO(input)
        sys.stdin.name = '<stdin>'

    try:
        script()
    except SystemExit:
        pass

    obj = type('Process', (object,), {})()
    obj.stderr = sys.stderr.getvalue()
    obj.stdout = sys.stdout.getvalue()
    return obj


class TestScript:
    def test_help(self):
        result = run('algograph -h'.split())
        assert DESCRIPTION in result.stdout

    def test_usage(self):
        result = run(['algograph'])
        assert 'usage: algograph [-h] ' in result.stderr

    def test_start_end(self):
        result = run('algograph -'.split(), input='start; end')
        assert result.stdout == 'digraph {\n  start -> end\n}\n'

    def test_graphviz(self):
        result = run('algograph --to=svg -'.split(), input='start; end')
        assert '<!-- start -->' in result.stdout
        assert '<!-- end -->' in result.stdout

    def test_input_filename(self, startendfile):
        result = run(['algograph', str(startendfile)])
        assert result.stdout == 'digraph {\n  start -> end\n}\n'

    def test_out(self, tmp_path):
        path = tmp_path.joinpath('algograph.dot')
        result = run('algograph -o'.split() + [str(path), '-'], input='start; end')
        assert path.read_text() == 'digraph {\n  start -> end\n}'

    def test_auto_output(self, startendfile):
        result = run('algograph -O'.split() + [str(startendfile)])
        assert startendfile.with_suffix('.dot').read_text() == 'digraph {\n  start -> end\n}'

