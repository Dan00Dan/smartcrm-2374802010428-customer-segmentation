import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src.etl import load_warehouse as warehouse


class TestLoadWarehouse(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        (self.root / "data" / "raw").mkdir(parents=True)
        (self.root / "data" / "processed").mkdir(parents=True)
        (self.root / "data" / "warehouse").mkdir(parents=True)
        (self.root / "docs").mkdir(parents=True)

        pd.DataFrame({
            "record_id": ["C001", "C002"],
            "ho_ten": ["Nguyen Van A", "Tran Thi B"],
            "so_dien_thoai": ["900000001", "900000002"],
        }).to_csv(
            self.root / "data" / "raw" / "customers_raw.csv",
            index=False,
        )

        self.orders = pd.DataFrame({
            "ma_don": ["HD001", "HD002"],
            "ma_cua_hang": ["CH01", "CH01"],
            "ngay": ["2026-01-10", "2026-01-12"],
            "so_dien_thoai": ["0900000001", "0999999999"],
            "thanh_tien": [1000000, 2000000],
        })

        self.orders.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        self.patches = [
            patch.object(warehouse, "ROOT", self.root),
            patch.object(
                warehouse,
                "CUSTOMERS_FILE",
                self.root / "data" / "raw" / "customers_raw.csv",
            ),
            patch.object(
                warehouse,
                "ORDERS_FILE",
                self.root / "data" / "processed" / "orders_normalized.csv",
            ),
            patch.object(
                warehouse,
                "WAREHOUSE_DIR",
                self.root / "data" / "warehouse",
            ),
        ]

        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def test_loads_orders_and_marks_unresolved_customer(self):
        warehouse.load_warehouse()

        fact = pd.read_csv(
            self.root / "data" / "warehouse" / "fact_order.csv",
            dtype={"customer_key": str},
        )
        issues = pd.read_csv(
            self.root / "data" / "warehouse" / "data_quality_issues.csv"
        )

        self.assertEqual(len(fact), 2)
        self.assertEqual(fact["order_business_key"].nunique(), 2)
        self.assertEqual(
            fact.loc[
                fact["order_id_source"] == "HD002", "customer_key"
            ].iloc[0],
            "UNKNOWN",
        )
        self.assertEqual(len(issues), 1)
        self.assertFalse(fact["segment_publishable"].any())

    def test_second_load_does_not_append_duplicate_rows(self):
        warehouse.load_warehouse()
        warehouse.load_warehouse()

        fact = pd.read_csv(
            self.root / "data" / "warehouse" / "fact_order.csv"
        )

        self.assertEqual(len(fact), 2)
        self.assertEqual(fact["order_business_key"].nunique(), 2)

    def test_duplicate_business_key_is_rejected(self):
        duplicated = pd.concat(
            [self.orders, self.orders.iloc[[0]]],
            ignore_index=True,
        )
        duplicated.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        with self.assertRaisesRegex(ValueError, "(?i)khóa cửa hàng"):
            warehouse.load_warehouse()

    def test_missing_required_column_is_rejected(self):
        incomplete = self.orders.drop(columns=["thanh_tien"])
        incomplete.to_csv(
            self.root / "data" / "processed" / "orders_normalized.csv",
            index=False,
        )

        with self.assertRaisesRegex(ValueError, "thiếu cột bắt buộc"):
            warehouse.load_warehouse()


if __name__ == "__main__":
    unittest.main()
