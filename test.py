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

    def test_convert_parenthesis_1(self):
        postfix = convert_to_postfix('(2*2+1)/2')
        self.assertEqual('2.0,2.0,*,1.0,+,2.0,/', str(postfix))

    def test_convert_parenthesis_2(self):
        postfix = convert_to_postfix('(1-(5.44+3)*8)/7')
        self.assertEqual('1.0,5.44,3.0,+,8.0,*,-,7.0,/', str(postfix))


class EvaluateTestCase(unittest.TestCase):
    def test_evaluate_1(self):
        expr = convert_to_postfix('1+3')
        self.assertEqual(4.0, expr.eval())

    def test_evaluate_2(self):
        expr = convert_to_postfix('2*2')
        self.assertEqual(4.0, expr.eval())

    def test_evaluate_3(self):
        expr = convert_to_postfix('2*2+1')
        self.assertEqual(5.0, expr.eval())

    def test_evaluate_4(self):
        expr = convert_to_postfix('(2*2+1)/2')
        self.assertEqual(2.5, expr.eval())

    def test_evaluate_5(self):
        expr = convert_to_postfix('(1-(5.44+3)*8)/7')
        self.assertEqual(-9.502857142857144, expr.eval())


if __name__ == '__main__':
    unittest.main()
