#!/usr/bin/env python
import argparse
from postfix import convert_to_postfix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate formula')
    parser.add_argument('formula', metavar='"a+b*c"', type=str, nargs=1, help='String with formula')
    args = parser.parse_args()

    postfix_expression = convert_to_postfix(args.formula)

    print(str(postfix_expression))
