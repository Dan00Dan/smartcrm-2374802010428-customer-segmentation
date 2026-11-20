
import unittest

import pandas as pd

from src.quality.check_quality import measure_column_quality


class TestMeasureColumnQuality(unittest.TestCase):

    def test_measures_completeness_by_column(self):
        df = pd.DataFrame({
            "ngay": ["2025-08-17", "", None],
            "thanh_tien": [1000, 2000, None],
        })

        result = measure_column_quality(df)
        date_result = result[result["column"] == "ngay"].iloc[0]

        self.assertEqual(date_result["completeness_percent"], 33.33)

    def test_measures_date_validity(self):
        df = pd.DataFrame({
            "ngay": [
                "2025-08-17",
                "17/08/2025",
                "2025-02-30",
            ]
        })

        result = measure_column_quality(df)
        date_result = result.iloc[0]

        self.assertAlmostEqual(
            date_result["validity_percent"],
            66.67,
            places=2,
        )

    def test_measures_date_consistency(self):
        df = pd.DataFrame({
            "ngay": [
                "2025-08-17",
                "17/08/2025",
            ]
        })

        result = measure_column_quality(df)
        date_result = result.iloc[0]

        self.assertEqual(date_result["consistency_percent"], 50.0)

    def test_unknown_rules_are_not_assumed_valid(self):
        df = pd.DataFrame({
            "ghi_chu": ["Ghi chú A", "Ghi chú B"]
        })

        result = measure_column_quality(df)

        self.assertTrue(pd.isna(result.iloc[0]["validity_percent"]))
        self.assertTrue(pd.isna(result.iloc[0]["consistency_percent"]))

    def test_negative_amount_is_invalid(self):
        df = pd.DataFrame({
            "thanh_tien": [1000, -500, 0]
        })

        result = measure_column_quality(df)

        self.assertAlmostEqual(
            result.iloc[0]["validity_percent"],
            66.67,
            places=2,
        )

    def test_negative_amount_is_inconsistent(self):
        df = pd.DataFrame({
            "thanh_tien": [1000, -500, 0]
        })

        result = measure_column_quality(df)

        self.assertAlmostEqual(
            result.iloc[0]["consistency_percent"],
            66.67,
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
