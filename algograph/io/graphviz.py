from .dot import DOT

import subprocess
import sys
import pathlib


GRAPHVIZ_PATH = (
    # Graphviz direct install
    r'C:\Program Files (x86)\Graphviz2.38\bin',
    # conda install
    r'C:\ProgramData\Anaconda3\Library\bin\graphviz'
)


class Graphviz:
    path = GRAPHVIZ_PATH

    # https://graphviz.gitlab.io/_pages/doc/info/output.html
    def __init__(self, graph=None, *args):
        self.graph = graph
        self.args = args

    def dot(self):
        if self.graph:
            return DOT(self.graph).encode()
        else:
            return ''

    def formats(self):
        err = self._run('-T?').stderr.strip()
        return err.split('Use one of: ', 1)[1].split()

    def _run(self, *args, input=''):
            if sys.platform == 'win32':
                ext = '.exe'
            else:
                ext = ''

            for path in ['.'] + list(self.path):
                path = pathlib.Path(path)
                prog = path.joinpath('dot').with_suffix(ext)
                try:
                    process = subprocess.run(
                        [str(prog), *args],
                        capture_output=True,
                        text=True,
                        input=input,
                    )

                except FileNotFoundError:
                    continue

                else:
                    break

            else:
                raise FileNotFoundError('dot was not found on {}'.format(self.path))

            return process

    def run(self, format='svg'):
        self.process = self._run('-T' + format, *self.args, input=self.dot())
        if self.process.returncode:
            if self.process.stderr.startswith('Format: '):
                raise ValueError("Wrong '{}' format. Please use one of the: {}.".format(format, self.formats()))
            raise ValueError(self.process.stderr.split('\nUsage: ', 1)[0])

        return self.process.stdout


