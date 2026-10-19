
import unittest
from unittest.mock import patch

import pandas as pd

from src.transform.process_orders import process_orders


class TestProcessOrders(unittest.TestCase):

    @patch("src.transform.process_orders.pd.read_csv")
    @patch("src.transform.process_orders.RAW_FILE")
    def test_split_valid_and_rejected_orders(
        self,
        mock_raw_file,
        mock_read_csv,
    ):
        mock_raw_file.exists.return_value = True

        mock_read_csv.return_value = pd.DataFrame({
            "order_id": ["HD001", "HD002", "HD003"],
            "ngay": [
                "17/08/2025",
                "",
                "2025-03-22",
            ],
            "thanh_tien": [
                "11990000",
                "5000000",
                "abc",
            ],
        })

        valid_df, reject_df, rows_before = process_orders()

        self.assertEqual(rows_before, 3)
        self.assertEqual(len(valid_df), 1)
        self.assertEqual(len(reject_df), 2)

        self.assertEqual(
            valid_df.iloc[0]["ngay"],
            "2025-08-17",
        )
        self.assertEqual(
            valid_df.iloc[0]["thanh_tien"],
            11990000.0,
        )

        self.assertIn("ly_do_tu_choi", reject_df.columns)
        self.assertTrue(
            reject_df["ly_do_tu_choi"].notna().all()
        )
        self.assertTrue(
            reject_df["ly_do_tu_choi"].str.strip().ne("").all()
        )

        self.assertEqual(
            len(valid_df) + len(reject_df),
            rows_before,
        )


if __name__ == "__main__":
    unittest.main()
