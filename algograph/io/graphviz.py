from .dot import DOT

import subprocess
import sys
import pathlib
import shlex

PATH_TO_GRAPHVIZ = (
    r'C:\Program Files (x86)\Graphviz2.38\bin',
    r'C:\ProgramData\Anaconda3\Library\bin'
)


class Graphviz:
    # https://graphviz.gitlab.io/_pages/doc/info/output.html
    def __init__(self, graph, format='svg', *args):
        self.graph = graph

    def run(self, *args):
        args = [shlex.quote(arg) for arg in args]
        process = subprocess.run(
            # FIXME: how to make it universal win/lin
            ' '.join(['/usr/bin/env &&', 'dot', '-Tcanon', *args]),
            #'set',
            shell=True,
            capture_output=True,
            input=DOT(self.graph).encode(),
            text=True,
            check=False,
            #env=dict(PATH=';'.join(str(pathlib.Path(path)) for path in PATH_TO_GRAPHVIZ))
            #env=dict(PATH=';'.join(PATH_TO_GRAPHVIZ), TERM='cmd')
            env=dict(PATH=';'.join(PATH_TO_GRAPHVIZ))
        )
        return process

    def encode(self):
        pass
