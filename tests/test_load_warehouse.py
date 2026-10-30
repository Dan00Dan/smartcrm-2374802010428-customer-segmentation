import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.etl import load_warehouse as warehouse


class TestLoadWarehouse(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.root)

        (self.root / "data" / "raw").mkdir(parents=True)
        (self.root / "data" / "processed").mkdir(parents=True)
        (self.root / "data" / "warehouse").mkdir(parents=True)
        (self.root / "docs").mkdir(parents=True)

        self.customers = pd.DataFrame(
            [
                {
                    "record_id": "KH001",
                    "ho_ten": "Nguyen Van A",
                    "so_dien_thoai": "0900000001",
                },
                {
                    "record_id": "KH002",
                    "ho_ten": "Tran Thi B",
                    "so_dien_thoai": "0900000002",
                },
            ]
        )

        self.orders = pd.DataFrame(
            [
                {
                    "ma_don": "HD001",
                    "ma_cua_hang": "CH001",
                    "ngay": "2026-01-10",
                    "so_dien_thoai": "0900000001",
                    "thanh_tien": 500000,
                },
                {
                    "ma_don": "HD002",
                    "ma_cua_hang": "CH001",
                    "ngay": "2026-01-15",
                    "so_dien_thoai": "0999999999",
                    "thanh_tien": 300000,
                },
            ]
        )

        self.customers.to_csv(
            self.root / "data" / "raw" / "customers_raw.csv",
            index=False,
        )

        self.orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_loads_orders_and_marks_unresolved_customer(self):
        warehouse.load_warehouse()

        fact_orders = pd.read_csv(
            self.root / "data" / "warehouse" / "fact_orders.csv"
        )

        self.assertEqual(len(fact_orders), 2)

        unresolved_orders = fact_orders[
            fact_orders["customer_id"] == "UNKNOWN"
        ]

        self.assertEqual(len(unresolved_orders), 1)

    def test_second_load_does_not_append_duplicate_rows(self):
        warehouse.load_warehouse()
        warehouse.load_warehouse()

        fact_orders = pd.read_csv(
            self.root / "data" / "warehouse" / "fact_orders.csv"
        )

        self.assertEqual(len(fact_orders), 2)

    def test_duplicate_business_key_is_rejected(self):
        orders = pd.concat(
            [self.orders, self.orders.iloc[[0]]],
            ignore_index=True,
        )

        orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        with self.assertRaises(ValueError):
            warehouse.load_warehouse()

    def test_missing_required_column_is_rejected(self):
        orders = self.orders.drop(columns=["thanh_tien"])

        orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        with self.assertRaises(ValueError):
            warehouse.load_warehouse()

    def test_missing_customer_record_id_is_rejected(self):
        customers = self.customers.copy()
        customers.loc[0, "record_id"] = ""

        customers.to_csv(
            self.root / "data" / "raw" / "customers_raw.csv",
            index=False,
        )

        with self.assertRaises(ValueError):
            warehouse.load_warehouse()

    def test_duplicate_customer_record_id_is_rejected(self):
        customers = self.customers.copy()
        customers.loc[1, "record_id"] = customers.loc[0, "record_id"]

        customers.to_csv(
            self.root / "data" / "raw" / "customers_raw.csv",
            index=False,
        )

        with self.assertRaises(ValueError):
            warehouse.load_warehouse()

    def test_invalid_order_date_is_recorded_as_issue(self):
        orders = self.orders.copy()
        orders["ngay"] = orders["ngay"].astype(str)
        orders.loc[0, "ngay"] = "ngay-khong-hop-le"

        orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        warehouse.load_warehouse()

        issues = pd.read_csv(
            self.root / "data" / "warehouse" / "data_quality_issues.csv"
        )

        invalid_date_issues = issues[
            issues["issue_code"] == "INVALID_ORDER_DATE"
        ]

        self.assertEqual(len(invalid_date_issues), 1)
        self.assertEqual(
            invalid_date_issues.iloc[0]["order_id_source"],
            "HD001",
        )

    def test_invalid_order_amount_is_recorded_as_issue(self):
        orders = self.orders.copy()
        orders["thanh_tien"] = orders["thanh_tien"].astype(str)
        orders.loc[0, "thanh_tien"] = "khong-hop-le"

        orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        warehouse.load_warehouse()

        issues = pd.read_csv(
            self.root / "data" / "warehouse" / "data_quality_issues.csv"
        )

        invalid_amount_issues = issues[
            issues["issue_code"] == "INVALID_ORDER_AMOUNT"
        ]

        self.assertEqual(len(invalid_amount_issues), 1)
        self.assertEqual(
            invalid_amount_issues.iloc[0]["order_id_source"],
            "HD001",
        )


if __name__ == "__main__":
    unittest.main()