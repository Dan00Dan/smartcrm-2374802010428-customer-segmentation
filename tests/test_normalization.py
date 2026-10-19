import unittest
import pandas as pd

from src.transform.normalize_dates import normalize_date
from src.transform.normalize_amount import normalize_amount

class TestNormalizeDate(unittest.TestCase):
    def test_valid_date(self):
        result = normalize_date("17/08/2025")
        self.assertEqual(result.strftime("%Y-%m-%d"), "2025-08-17")

    def test_another_date_format(self):
        result = normalize_date("2025-03-22")
        self.assertEqual(result.strftime("%Y-%m-%d"), "2025-03-22")

    def test_empty_date(self):
        self.assertTrue(pd.isna(normalize_date("")))

    def test_invalid_date(self):
        self.assertTrue(pd.isna(normalize_date("not-a-date")))

class TestNormalizeAmount(unittest.TestCase):
    def test_valid_amount(self):
        self.assertEqual(normalize_amount("11990000"), 11990000.0)

    def test_amount_with_spaces(self):
        self.assertEqual(normalize_amount(" 4990000 "), 4990000.0)

    def test_vietnamese_currency_format(self):
        self.assertEqual(
            normalize_amount("34.980.500đ"),
            34980500.0,
        )

    def test_currency_with_thousand_separator(self):
        self.assertEqual(
            normalize_amount("704.000đ"),
            704000.0,
        )

    def test_empty_amount(self):
        self.assertTrue(pd.isna(normalize_amount("")))

    def test_invalid_amount(self):
        self.assertTrue(pd.isna(normalize_amount("abc")))

    def test_negative_amount(self):
        self.assertTrue(pd.isna(normalize_amount("-100")))

if __name__ == "__main__":
    unittest.main()