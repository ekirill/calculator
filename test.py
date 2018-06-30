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

    def test_convert_multiply(self):
        postfix = convert_to_postfix('1-5.44*7+5*2')
        self.assertEqual('1.0,5.44,7.0,*,-,5.0,2.0,*,+', str(postfix))

    def test_convert_division(self):
        postfix = convert_to_postfix('1-5.44/7+5*3/2')
        self.assertEqual('1.0,5.44,7.0,/,-,5.0,3.0,*,2.0,/,+', str(postfix))

    def test_convert_parenthesis(self):
        postfix = convert_to_postfix('(1-(5.44+3)*8)/7')
        self.assertEqual('1.0,5.44,3.0,+,8.0,*,-,7.0,/', str(postfix))


if __name__ == '__main__':
    unittest.main()
