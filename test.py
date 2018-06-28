#!/usr/bin/env python
import unittest

from postfix import convert_to_postfix


class ConverterTestCase(unittest.TestCase):
    def test_convert_success(self):
        postfix = convert_to_postfix('5+7')
        self.assertEqual(str(postfix), '57+')


if __name__ == '__main__':
    unittest.main()