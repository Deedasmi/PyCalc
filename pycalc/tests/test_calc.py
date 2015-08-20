"""
Unit tests
"""
__author__ = 'Deedasmi'
import unittest

from pycalc import calc


class TestCalcMethods(unittest.TestCase):
    """
    Test class
    """
    
    def test_math(self):
        """
        Simple unit tests
        :return:
        """
        self.assertAlmostEqual(calc.calculate("4 * 10 / 15 + ( 6 - 2 * 3 )"), 2.6666666, 3)
        self.assertEqual(calc.calculate("2 +5/1 + (2* 5)/2"), 12)
        self.assertAlmostEqual(calc.calculate("7^2+16 / (4^4)"), 49.0625, 3)
        self.assertEqual(calc.calculate("(1+2)+(2+3)"), 8)
        self.assertEqual(calc.calculate("1+ ( ( ( 3 + 2) * 2) - 4)"), 7)
        self.assertAlmostEqual(calc.calculate("pi*2"), 6.2831, 3)
        self.assertEqual(calc.calculate("(2*.5)^3"), 1)
        calc.handle_user_defined_input("Matt = 20")
        self.assertAlmostEqual(calc.calculate("Matt * pi"), 62.8318, 3)

    def test_negative(self):
        """
        Check negatives
        :return:
        """
        self.assertEqual(calc.calculate("(-4) + 2"), -2)
        self.assertEqual(calc.calculate("(4 * 2 + 4)  * -2"), -24)

    def test_UDF(self):
        """
        Make sure errors are handled in UDF
        :return:
        """
        with self.assertRaises(SyntaxWarning):
            calc.handle_user_defined_input("bob = 4")
            calc.calculate("bob2 + 4")

    def test_symbol_errors(self):
        """
        Validate some of the stranger symbol issues
        :return:
        """
        with self.assertRaises(SyntaxWarning):
            calc.calculate("2 + (%)")
            calc.calculate("2 + 2)")
            calc.calculate("2 + () + 5")
            calc.calculate("2 + ((%) +2)")

    def test_saved(self):
        """
        Test saved value feature
        :return:
        """
        calc.saved = 5
        self.assertEqual(calc.calculate("+2"), 7)
        self.assertEqual(calc.calculate("2 { 6 / 2 [ 5 ] }"), 30)

    def test_operator_errors(self):
        """
        More operator errors
        :return:
        """
        with self.assertRaises(SyntaxWarning):
            calc.calculate("2 + * 4")
            calc.calculate("2 ! 4")
            calc.handle_user_defined_input("matt = 4 = 5")

    def test_modulo(self):
        """
        Modulo feature tests
        :return:
        """
        self.assertEqual(calc.calculate("2 % 2"), 0)
        self.assertEqual(calc.calculate("2 * 2 % 2"), 0)
        self.assertEqual(calc.calculate("(2 + 3) % 2 / 5"), 0.2)

    def test_UDV(self):
        """
        Don't allow silly UDV input
        :return:
        """
        with self.assertRaises(UserWarning):
            calc.handle_user_defined_input("2 = 8")

    def test_paren(self):
        """
        Make sure invalid parens is thrown
        :return:
        """
        with self.assertRaises(SyntaxWarning):
            calc.find_matching_parenthesis(0, "( 2 + 5")

    def test_simple_math(self):
        """
        Simply errors
        :return:
        """
        self.assertEqual(calc.do_simple_math(4, 6, "+"), 10)
        with self.assertRaises(ZeroDivisionError):
            calc.do_simple_math(1, 0, "/")

    if __name__ == "__main__":
        test_math()
        test_simple_math()
        test_paren()
        test_UDV()
