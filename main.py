#!/usr/bin/env python
import argparse
from postfix import convert_to_postfix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate formula')
    parser.add_argument('formula', metavar='"2+2*2"', type=str, help='String with formula')
    args = parser.parse_args()

    expression = convert_to_postfix(args.formula)
    print(expression.eval())
