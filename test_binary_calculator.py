"""
Unit Tests for Binary Calculator Module
"""

import unittest
from binary_calculator import (
    BinaryCalculator,
    normalize_binary,
    bin_to_dec,
    dec_to_bin,
)


class TestBinaryCalculator(unittest.TestCase):

    def test_normalize_binary(self):
        self.assertEqual(normalize_binary("0"), "0")
        self.assertEqual(normalize_binary("0000"), "0")
        self.assertEqual(normalize_binary("00101"), "101")
        self.assertEqual(normalize_binary("0b1101"), "1101")
        self.assertEqual(normalize_binary(" 1010  "), "1010")
        
        with self.assertRaises(ValueError):
            normalize_binary("")
        with self.assertRaises(ValueError):
            normalize_binary("10201")
        with self.assertRaises(ValueError):
            normalize_binary("abc")

    def test_conversions(self):
        self.assertEqual(bin_to_dec("0"), 0)
        self.assertEqual(bin_to_dec("1101"), 13)
        self.assertEqual(dec_to_bin(0), "0")
        self.assertEqual(dec_to_bin(13), "1101")
        self.assertEqual(dec_to_bin(255), "11111111")

    def test_addition(self):
        # 0 + 0 = 0
        res = BinaryCalculator.add("0", "0")
        self.assertEqual(res["result"], "0")
        self.assertEqual(res["result_dec"], 0)

        # 1 + 1 = 10 (1 + 1 = 2)
        res = BinaryCalculator.add("1", "1")
        self.assertEqual(res["result"], "10")
        self.assertEqual(res["result_dec"], 2)

        # 1101 + 1011 = 11000 (13 + 11 = 24)
        res = BinaryCalculator.add("1101", "1011")
        self.assertEqual(res["result"], "11000")
        self.assertEqual(res["result_dec"], 24)

        # 1111 + 1 = 10000 (15 + 1 = 16)
        res = BinaryCalculator.add("1111", "1")
        self.assertEqual(res["result"], "10000")
        self.assertEqual(res["result_dec"], 16)

        # Unequal lengths: 101 + 11 = 1000 (5 + 3 = 8)
        res = BinaryCalculator.add("101", "11")
        self.assertEqual(res["result"], "1000")
        self.assertEqual(res["result_dec"], 8)

    def test_subtraction(self):
        # 101 - 101 = 0
        res = BinaryCalculator.subtract("101", "101")
        self.assertEqual(res["result"], "0")
        self.assertEqual(res["result_dec"], 0)
        self.assertFalse(res["is_negative"])

        # 11001 - 1010 = 1111 (25 - 10 = 15)
        res = BinaryCalculator.subtract("11001", "1010")
        self.assertEqual(res["result"], "1111")
        self.assertEqual(res["result_dec"], 15)
        self.assertFalse(res["is_negative"])

        # Multiple borrows: 10000 - 1 = 1111 (16 - 1 = 15)
        res = BinaryCalculator.subtract("10000", "1")
        self.assertEqual(res["result"], "1111")
        self.assertEqual(res["result_dec"], 15)

        # Negative result: 10 - 110 = -100 (2 - 6 = -4)
        res = BinaryCalculator.subtract("10", "110")
        self.assertEqual(res["result"], "-100")
        self.assertEqual(res["result_dec"], -4)
        self.assertTrue(res["is_negative"])

    def test_multiplication(self):
        # Multiplication with 0
        res = BinaryCalculator.multiply("1101", "0")
        self.assertEqual(res["result"], "0")
        self.assertEqual(res["result_dec"], 0)

        # Multiplication with 1
        res = BinaryCalculator.multiply("1101", "1")
        self.assertEqual(res["result"], "1101")
        self.assertEqual(res["result_dec"], 13)

        # 101 * 11 = 1111 (5 * 3 = 15)
        res = BinaryCalculator.multiply("101", "11")
        self.assertEqual(res["result"], "1111")
        self.assertEqual(res["result_dec"], 15)
        self.assertEqual(len(res["partial_products"]), 2)

        # 1101 * 1010 = 10000010 (13 * 10 = 130)
        res = BinaryCalculator.multiply("1101", "1010")
        self.assertEqual(res["result"], "10000010")
        self.assertEqual(res["result_dec"], 130)

    def test_division(self):
        # Exact division: 110 / 10 = 11 R 0 (6 / 2 = 3 R 0)
        res = BinaryCalculator.divide("110", "10")
        self.assertEqual(res["quotient"], "11")
        self.assertEqual(res["remainder"], "0")
        self.assertEqual(res["quotient_dec"], 3)
        self.assertEqual(res["remainder_dec"], 0)

        # Division with remainder: 1101 / 10 = 110 R 1 (13 / 2 = 6 R 1)
        res = BinaryCalculator.divide("1101", "10")
        self.assertEqual(res["quotient"], "110")
        self.assertEqual(res["remainder"], "1")
        self.assertEqual(res["quotient_dec"], 6)
        self.assertEqual(res["remainder_dec"], 1)

        # Dividend smaller than divisor: 10 / 101 = 0 R 10 (2 / 5 = 0 R 2)
        res = BinaryCalculator.divide("10", "101")
        self.assertEqual(res["quotient"], "0")
        self.assertEqual(res["remainder"], "10")
        self.assertEqual(res["quotient_dec"], 0)
        self.assertEqual(res["remainder_dec"], 2)

        # 0 dividend: 0 / 111 = 0 R 0
        res = BinaryCalculator.divide("0", "111")
        self.assertEqual(res["quotient"], "0")
        self.assertEqual(res["remainder"], "0")

        # Division by zero
        with self.assertRaises(ZeroDivisionError):
            BinaryCalculator.divide("1010", "0")


if __name__ == "__main__":
    unittest.main()

