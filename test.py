#!/usr/bin/env python
import unittest

from postfix import convert_to_postfix


class ConverterTestCase(unittest.TestCase):
    def test_convert_success_plus(self):
        postfix = convert_to_postfix('5+ 7')
        self.assertEqual(str(postfix), '5.0,7.0,+')

    def test_convert_success_plus_float(self):
        postfix = convert_to_postfix('5.44+7')
        self.assertEqual(str(postfix), '5.44,7.0,+')


if __name__ == '__main__':
    unittest.main()
