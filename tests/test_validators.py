from __future__ import unicode_literals
import six

import unittest
import numpy as np
import re

from table_cleaner.validators import String, Int, Numeric, Bool, Regex, Email


class TestStringValidator(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        validator = String()
        test_cases = [("s", "s"),
                      ("test", "test"),
                      (1, "1"),
                      (None, "None")]
        for i,s in test_cases:
            verdicts = list(validator.validate(i))
            self.assertTrue(verdicts[0].valid)
            self.assertEqual(verdicts[0].value, s)

    def test_too_short(self):
        validator = String(min_length=1)
        verdicts = list(validator.validate(""))
        self.assertEqual(len(verdicts), 1)
        self.assertFalse(verdicts[0].valid)
        self.assertEqual(verdicts[0].reason, "too short")

        verdicts = list(validator.validate("test"))
        self.assertEqual(len(verdicts), 1)
        self.assertTrue(verdicts[0].valid)

    def test_too_long(self):
        validator = String(max_length=2)
        verdicts = list(validator.validate("test"))
        self.assertEqual(len(verdicts), 1)
        self.assertFalse(verdicts[0].valid)
        self.assertEqual(verdicts[0].reason, "too long")

        verdicts = list(validator.validate("t"))
        self.assertEqual(len(verdicts), 1)
        self.assertTrue(verdicts[0].valid, True)

    def test_invalid_args(self):
        String()
        String(min_length=1)
        String(max_length=1)
        String(min_length=1, max_length=3)

        self.assertRaises(ValueError, String,
                          min_length=10, max_length=5)


class TestNumericValidator(unittest.TestCase):
    def test_valid_dtypes(self):
        for key, values in six.iteritems(np.sctypes):
            if key == "others":
                continue

            for dt in values:
                class TempClass(Numeric):
                    dtype = dt
                TempClass()

    def test_invalid_dtypes(self):
        for dt in np.sctypes['others']:
            class TempClass(Numeric):
                dtype = dt
            self.assertRaises(ValueError, TempClass)
        class TempClass(Numeric):
            dtype = str
        self.assertRaises(ValueError, TempClass)

        class TempClass(Numeric):
            dtype = None
        self.assertRaises(ValueError, TempClass)


class TestIntValidator(unittest.TestCase):
    def test_basic(self):
        validator = Int()

        for v in [1, "2", 3.0, str("4")]:
            verdicts = list(validator.validate(v))
            self.assertEqual(len(verdicts), 1)
            self.assertTrue(verdicts[0].valid)
            self.assertEqual(verdicts[0].value, int(v))

        for v in ["dsa", object, Int, type]:
            verdicts = list(validator.validate(v))
            self.assertEqual(len(verdicts), 1)
            self.assertFalse(verdicts[0].valid)

    def test_too_small(self):
        validator = Int(min_value=1)

        verdicts = list(validator.validate(1))
        self.assertEqual(len(verdicts), 1)
        self.assertTrue(verdicts[0].valid)


        validator = Int(min_value=0)

        verdicts = list(validator.validate(-1))
        self.assertEqual(len(verdicts), 1)
        self.assertFalse(verdicts[0].valid)

    def test_too_high(self):
        validator = Int(max_value=10)

        verdicts = list(validator.validate(1))
        self.assertEqual(len(verdicts), 1)
        self.assertTrue(verdicts[0].valid)


        verdicts = list(validator.validate(12))
        self.assertEqual(len(verdicts), 1)
        self.assertFalse(verdicts[0].valid)

    def test_ranges(self):
        validator = Int(min_value=0, max_value=10)


        for v in [1, "2", 3.0, str("4")]:
            verdicts = list(validator.validate(v))
            self.assertEqual(len(verdicts), 1)
            self.assertTrue(verdicts[0].valid)
            self.assertEqual(verdicts[0].value, int(v))

        for v in [-1,40, "40", "-30"]:
            verdicts = list(validator.validate(v))
            self.assertEqual(len(verdicts), 1)
            self.assertFalse(verdicts[0].valid)

    def test_invalid_args(self):
        self.assertRaises(ValueError, Int, min_value=10, max_value=-1)


class TestBoolean(unittest.TestCase):
    def test_empty_arguments(self):
        self.assertRaises(ValueError, Bool, true_values=[])
        self.assertRaises(ValueError, Bool, false_values=[])
        self.assertRaises(ValueError, Bool, nan_values=[])

    def test_values_intersection(self):
        self.assertRaises(ValueError, Bool, \
                          true_values=["A"], false_values=["B", "A"])

        self.assertRaises(ValueError, Bool, \
                          true_values=["A"], nan_values=["B", "A"])

        self.assertRaises(ValueError, Bool, \
                          false_values=["A"], nan_values=["B", "A"])

    def test_basic(self):
        validator = Bool()

        cases = [("T", True),
                 ("F", False),
                 (np.nan, np.nan),
                 ("X", np.nan),
                 ("nan", np.nan),
                 (True, True),
                 (False, False)]

        for obj, value in cases:
            verdicts = list(validator.validate(obj))
            if np.isnan(value):
                self.assertTrue(np.isnan(verdicts[0].value))
            else:
                self.assertEqual(verdicts[0].value, value)
            self.assertTrue(verdicts[0].valid)

    def disallow_nan(self):
        validator = Bool(allow_nan=False)
        verdicts = list(validator.validate(np.nan))

        self.assertFalse(verdicts[0].valid)


class TestRegex(unittest.TestCase):
    def test_basic(self):
        test_cases = [(r"true", 0, ["true"], ["false", "f"],),
                      (r"^test", 0, ["test_123", "test"], ["123_test","123"])
                ]
        for expression, flags, matches, mismatches in test_cases:
            validator = Regex(regex=expression, flags=flags)
            for v in matches:
                verdicts = list(validator.validate(v))
                self.assertTrue(verdicts[0].valid)

            for v in mismatches:
                verdicts = list(validator.validate(v))
                self.assertFalse(verdicts[0].valid)


    def test_invalid_args(self):
        self.assertRaises(TypeError, Regex, regex=re.compile("test"), \
                flags=1)


class TestEmail(unittest.TestCase):
    def test_valid(self):
        test_cases = ("you@example.com", "you@localhost",
                "you.are.toast@example.com", "captain@sub.example.com")
        validator = Email()
        for email in test_cases:
            verdicts = list(validator.validate(email))
            self.assertTrue(verdicts[0].valid)


    def test_invalid(self):
        test_cases = ("dsadf you@example.com", "you@example",
                "you.are.toast@!example.com", "captain@sub.example.+com")
        validator = Email()
        for email in test_cases:
            verdicts = list(validator.validate(email))
            self.assertFalse(verdicts[0].valid)

if __name__ == '__main__':
    unittest.main()
