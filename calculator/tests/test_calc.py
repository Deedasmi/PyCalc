__author__ = 'Deedasmi'
import unittest

from calculator import calc


class TestCalcMethods(unittest.TestCase):
    def test_math(self):
        self.assertAlmostEqual(calc.calculate("4 * 10 / 15 + ( 6 - 2 * 3 )"), 2.6666666, 3)
        self.assertEqual(calc.calculate("2 +5/1 + (2* 5)/2"), 12)
        self.assertAlmostEqual(calc.calculate("7^2+16 / (4^4)"), 49.0625, 3)
        self.assertEqual(calc.calculate("(1+2)+(2+3)"), 8)
        self.assertEqual(calc.calculate("1+ ( ( ( 3 + 2) * 2) - 4)"), 7)
        #self.assertAlmostEqual(calc.calculate("pi*2"), 6.2831, 3)
        self.assertEqual(calc.calculate("(2*.5)^3"), 1)
        #calc.handle_user_defined_input("Matt = 20")
        #self.assertAlmostEqual(calc.calculate("Matt * pi"), 62.8318, 3)
        
    @unittest.skipIf(calc.__version__ < 0.7, "Negative numbers")
    def testNegative(self):
        self.assertEqual(calc.calculate("(-4) + 2"), -2)
        self.assertEqual(calc.calculate("(4 * 2 + 4)  * -2"), -24)
        
    @unittest.skipIf(calc.__version__ < 0.7, "AlphaNumeric bug")
    def testIssue12(self):
        with self.assertRaises(SyntaxWarning):
            calc.handle_user_defined_input("bob = 4")
            calc.calculate("bob2 + 4")

    @unittest.skipIf(calc.__version__ < 0.67, "Fixes not yet implemented in v0.65")
    def test_moreFixes(self):
        with self.assertRaises(SyntaxWarning):
            calc.calculate("2 + (%)")
            calc.calculate("2 + 2)")
            calc.calculate("2 + () + 5")
            calc.calculate("2 + ((%) +2)")
            

    @unittest.skipIf(calc.__version__ < 0.67, "Features not yet implemented in v0.65")
    def test_moreFixes(self):
        calc.saved = 5
        self.assertEqual(calc.calculate("+2"), 7)
        self.assertEqual(calc.calculate("2 { 6 / 2 [ 5 ] }"), 30)



    @unittest.skipIf(calc.__version__ < 0.65, "Fixes not yet implemented in v.5")
    def test_futureFixes(self):
        with self.assertRaises(SyntaxWarning):
            calc.calculate("2 + * 4")
            calc.calculate("2 ! 4")
            calc.handle_user_defined_input("matt = 4 = 5")


    @unittest.skipIf(calc.__version__ < 0.6, "Features not implemented in v0.5")
    def test_futureFeatures(self):
        self.assertEqual(calc.calculate("2 % 2"), 0)
        self.assertEqual(calc.calculate("2 * 2 % 2"), 0)
        self.assertEqual(calc.calculate("(2 + 3) % 2 / 5"), 0.2)

    def test_UDV(self):
        with self.assertRaises(UserWarning):
            calc.handle_user_defined_input("2 = 8")

    def test_Paren(self):
        with self.assertRaises(SyntaxWarning):
            calc.find_matching_parenthesis(0, "( 2 + 5")

    def test_simpleMath(self):
        self.assertEqual(calc.do_simple_math(4, 6, "+"), 10)
        with self.assertRaises(ZeroDivisionError):
            calc.do_simple_math(1, 0, "/")


    if __name__ == "__main__":
        test_math()
        test_simpleMath()
        test_Paren()
        test_UDV()
