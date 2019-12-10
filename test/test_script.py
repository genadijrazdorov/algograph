from algograph.script import script, DESCRIPTION

import pytest
import subprocess


def run(args, input=None, check=True):
    if input is None:
        return subprocess.run(args.split(),
                                check=check,
                                text=True,
                                capture_output=True
                                )
    else:
        return subprocess.run(args.split(),
                                check=check,
                                text=True,
                                capture_output=True,
                                input=input
                                )



class TestScript:
    def test_help(self):
        result = run('algograph -h')
        assert DESCRIPTION in result.stdout

    def test_usage(self):
        result = run('algograph', check=False)
        assert 'usage: algograph [-h] ' in result.stderr

    def test_start_end(self):
        result = run('algograph -', input='start; end')
        assert result.stdout == 'digraph {\n  start -> end\n}\n'

    @pytest.mark.xfail(reason='Not working due to graphviz path change')
    def test_graphviz(self):
        result = run('algograph --to=svg -', input='start; end', check=False)
        assert '<!-- start -->' in result.stdout
        assert '<!-- end -->' in result.stdout

