from algograph.io.dot import DOT
from algograph.parser import Parser

import argparse


description = '''
An algorithm to graph translator.

Algograph takes algorithm description in python syntax and translates it to
graphviz compatible dot format.

'''

epilog = '''
Please visit https://github.com/genadijrazdorov/algograph
'''

def script():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog
    )

    parser.add_argument(
        "algorithm",
        type=argparse.FileType(),
        help='algorithm file name'
    )

    args = parser.parse_args()

    name = args.algorithm.name
    if '.' in name:
        name, ext = name.rsplit('.', 1)

    graph = Parser(args.algorithm.read()).parse()
    dot = DOT(graph).encode()
    if name == '<stdin>':
        print(dot)
    else:
        with open(name + 'dot', 'w') as outfh:
            outfh.write(dot)
