from algograph.script import script, description

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
        assert description in result.stdout

    def test_usage(self):
        result = run('algograph', check=False)
        assert 'usage: algograph [-h] algorithm' in result.stderr

    def test_start_end(self):
        result = run('algograph -', input='start; end')
        assert result.stdout == 'digraph {\n  start -> end\n}\n'

    def test_graphviz(self):
        result = run('algograph --to=svg -', input='start; end', check=False)
        assert '<!-- start -->' in result.stdout
        assert '<!-- end -->' in result.stdout
