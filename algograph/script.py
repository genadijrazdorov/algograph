from .algograph import algo2dot

import argparse


description = '''
An algorithm to graph translator.

Algograph takes algorithm description in python syntax and translates it to
graphviz compatible dot format.

'''

epilog = '''
Please visit https://github.com/genadijrazdorov/algograph
'''

def main():
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

    with open(args.algorithm.name[:-2] + 'dot', 'w') as outfh:
        outfh.write(algo2dot(args.algorithm.read()))