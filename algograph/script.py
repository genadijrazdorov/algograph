from algograph.io.dot import DOT
from algograph.parser import Parser

import argparse
import subprocess


# FIXME: do not hard code this
PATH_TO_GRAPHVIZ = r'C:\ProgramData\Anaconda3\Library\bin'

DESCRIPTION = '''
An algorithm to graph translator.

Algograph takes algorithm description in python syntax and translates it to
graph.

'''

EPILOG = '''
Please visit https://github.com/genadijrazdorov/algograph
'''

def script():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )

    parser.add_argument(
        "algorithm",
        type=argparse.FileType(),
        help='algorithm file name'
    )
    parser.add_argument(
        '-t', '--to',
        default='dot',
        help='output format: [%(default)s], svg'
    )
    parser.add_argument(
        '-o', '--out',
        help='output filename'
    )

    parser.add_argument(
        '-O', '--auto-output',
        action='store_true',
        help='automatic output filename'
    )

    args = parser.parse_args()

    name = args.algorithm.name
    if '.' in name:
        name, ext = name.rsplit('.', 1)

    graph = Parser(args.algorithm.read()).parse()
    dot = DOT(graph).encode()

    if args.to == 'dot':
        result = dot
        ext = '.dot'

    elif args.to == 'svg':
        process = subprocess.run((PATH_TO_GRAPHVIZ  + r'\dot.bat -Tsvg').split(), input=dot, text=True, capture_output=True)
        result = process.stdout
        ext = '.svg'

    filename = None
    if args.out:
        filename = args.out

    elif args.auto_output and name != '<stdin>':
        filename = name + ext

    if filename:
        with open(filename, 'w') as outfh:
            outfh.write(result)

    elif name == '<stdin>':
        print(result)

    else:
        raise Exception
