"""
Unit Test Suite for Scientific Calculator
=========================================
Tests first-principles math functions, edge cases, operator precedence,
and expression parsing.
"""

import unittest
import math
import fundamental_math as fm
from calculator_engine import CalculatorEngine


class TestFundamentalMath(unittest.TestCase):
    def test_constants(self):
        self.assertAlmostEqual(fm.PI, math.pi, places=14)
        self.assertAlmostEqual(fm.E, math.e, places=14)
        self.assertAlmostEqual(fm.LN2, math.log(2), places=14)

    def test_sin_cos_tan(self):
        # Degrees
        angles_deg = [0, 30, 45, 60, 90, 150, 180, 270, 360, -30, -90, 720]
        for deg in angles_deg:
            rad = math.radians(deg)
            self.assertAlmostEqual(fm.sin(deg, is_degrees=True), math.sin(rad), places=12)
            self.assertAlmostEqual(fm.cos(deg, is_degrees=True), math.cos(rad), places=12)

        # Tan values
        self.assertAlmostEqual(fm.tan(0, is_degrees=True), 0.0, places=12)
        self.assertAlmostEqual(fm.tan(45, is_degrees=True), 1.0, places=12)
        self.assertAlmostEqual(fm.tan(60, is_degrees=True), math.sqrt(3), places=12)

        # Tan asymptote at 90 deg raises ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            fm.tan(90, is_degrees=True)

    def test_inverse_trig(self):
        for val in [0.0, 0.5, math.sqrt(2)/2, math.sqrt(3)/2, 1.0, -0.5, -1.0]:
            self.assertAlmostEqual(fm.asin(val), math.asin(val), places=12)
            self.assertAlmostEqual(fm.acos(val), math.acos(val), places=12)

        for val in [-10.0, -1.0, 0.0, 1.0, 5.0]:
            self.assertAlmostEqual(fm.atan(val), math.atan(val), places=12)

    def test_roots(self):
        self.assertAlmostEqual(fm.sqrt(0), 0.0)
        self.assertAlmostEqual(fm.sqrt(2), math.sqrt(2), places=14)
        self.assertAlmostEqual(fm.sqrt(100), 10.0, places=14)
        self.assertAlmostEqual(fm.cbrt(27), 3.0, places=14)
        self.assertAlmostEqual(fm.cbrt(-27), -3.0, places=14)

        with self.assertRaises(ValueError):
            fm.sqrt(-4)

    def test_exponential_and_log(self):
        for x in [0.1, 1.0, 2.5, 10.0, 100.0]:
            self.assertAlmostEqual(fm.ln(x), math.log(x), places=13)
            self.assertAlmostEqual(fm.log10(x), math.log10(x), places=13)

        for x in [-2.0, 0.0, 1.5, 5.0]:
            self.assertAlmostEqual(fm.exp(x), math.exp(x), places=11)

    def test_powers(self):
        self.assertAlmostEqual(fm.power(2, 3), 8.0)
        self.assertAlmostEqual(fm.power(4, 0.5), 2.0)
        self.assertAlmostEqual(fm.power(2.5, 3.2), 2.5 ** 3.2, places=12)

    def test_combinatorics(self):
        self.assertEqual(fm.factorial(0), 1)
        self.assertEqual(fm.factorial(5), 120)
        self.assertEqual(fm.permutations(5, 2), 20)
        self.assertEqual(fm.combinations(5, 2), 10)


class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.calc_deg = CalculatorEngine(angle_mode='DEG')
        self.calc_rad = CalculatorEngine(angle_mode='RAD')

    def test_arithmetic(self):
        self.assertAlmostEqual(self.calc_deg.calculate("1 + 2 * 3"), 7.0)
        self.assertAlmostEqual(self.calc_deg.calculate("(1 + 2) * 3"), 9.0)
        self.assertAlmostEqual(self.calc_deg.calculate("10 / 2 - 3"), 2.0)
        self.assertAlmostEqual(self.calc_deg.calculate("2^3^2"), 512.0)  # right-assoc
        self.assertAlmostEqual(self.calc_deg.calculate("10 % 3"), 1.0)

    def test_unary_operators(self):
        self.assertAlmostEqual(self.calc_deg.calculate("-5 + 10"), 5.0)
        self.assertAlmostEqual(self.calc_deg.calculate("3 * -2"), -6.0)
        self.assertAlmostEqual(self.calc_deg.calculate("-(3 + 2)"), -5.0)
        self.assertAlmostEqual(self.calc_deg.calculate("(-2)^2"), 4.0)

    def test_implicit_multiplication(self):
        self.assertAlmostEqual(self.calc_deg.calculate("2pi"), 2.0 * fm.PI, places=12)
        self.assertAlmostEqual(self.calc_deg.calculate("2(3 + 4)"), 14.0)
        self.assertAlmostEqual(self.calc_deg.calculate("(2)(3)"), 6.0)
        self.assertAlmostEqual(self.calc_deg.calculate("2sin(30)"), 1.0, places=12)

    def test_trigonometric_expressions(self):
        self.assertAlmostEqual(self.calc_deg.calculate("sin(30) + cos(60)"), 1.0, places=12)
        self.assertAlmostEqual(self.calc_deg.calculate("tan(45)"), 1.0, places=12)
        self.assertAlmostEqual(self.calc_deg.calculate("sin(45)^2 + cos(45)^2"), 1.0, places=12)

        # Radian mode
        self.assertAlmostEqual(self.calc_rad.calculate("sin(pi/2)"), 1.0, places=12)
        self.assertAlmostEqual(self.calc_rad.calculate("cos(pi)"), -1.0, places=12)

    def test_scientific_functions(self):
        self.assertAlmostEqual(self.calc_deg.calculate("sqrt(25) + cbrt(8)"), 7.0)
        self.assertAlmostEqual(self.calc_deg.calculate("ln(e)"), 1.0, places=12)
        self.assertAlmostEqual(self.calc_deg.calculate("log(1000)"), 3.0, places=12)
        self.assertAlmostEqual(self.calc_deg.calculate("fact(6)"), 720.0)

    def test_ans_variable(self):
        self.calc_deg.calculate("10 + 5")
        res = self.calc_deg.calculate("ans * 2")
        self.assertEqual(res, 30.0)


if __name__ == '__main__':
    unittest.main()
