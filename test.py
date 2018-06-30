#!/usr/bin/env python
import unittest

from postfix import convert_to_postfix


class ConverterTestCase(unittest.TestCase):
    def test_convert_plus(self):
        postfix = convert_to_postfix('5+ 7')
        self.assertEqual('5.0,7.0,+', str(postfix))

    def test_convert_plus_float(self):
        postfix = convert_to_postfix('5.44+7')
        self.assertEqual('5.44,7.0,+', str(postfix))

    def test_convert_minus(self):
        postfix = convert_to_postfix('5.44+7-1')
        self.assertEqual('5.44,7.0,+,1.0,-', str(postfix))

    def test_convert_negative(self):
        postfix = convert_to_postfix('-5.44+7-1--1')
        self.assertEqual('5.44,(-),7.0,+,1.0,-,1.0,(-),-', str(postfix))


if __name__ == '__main__':
    unittest.main()
