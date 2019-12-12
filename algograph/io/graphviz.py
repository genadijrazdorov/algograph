from .dot import DOT

import subprocess
import sys
import pathlib
import shlex

PATH_TO_GRAPHVIZ = ';'.join((
    r'C:\Program Files (x86)\Graphviz2.38\bin',
    r'C:\ProgramData\Anaconda3\Library\bin'
))


class Graphviz:
    # https://graphviz.gitlab.io/_pages/doc/info/output.html
    def __init__(self, graph, format='svg', *args):
        self.graph = graph

    def run(self, *args):
        args = [shlex.quote(arg) for arg in args]
        process = subprocess.run(
            # FIXME: how to make it universal win/lin
            ' '.join(['dot', '-Tcanon', *args]),
            shell=True,
            capture_output=True,
            input=DOT(self.graph).encode(),
            text=True,
            check=False,
            env=dict(PATH=PATH_TO_GRAPHVIZ) if sys.platform == 'win32' else None
        )
        return process

    def encode(self):
        pass
