
from pathlib import Path

import pandas as pd

from transform.normalize_dates import normalize_date
from transform.normalize_amount import normalize_amount


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "orders_2024_2026.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"


def process_orders():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_FILE, dtype=str, keep_default_na=False)
    rows_before = len(df)

    original_dates = df["ngay"].copy()
    original_amounts = df["thanh_tien"].copy()

    normalized_dates = original_dates.map(normalize_date)
    normalized_amounts = original_amounts.map(normalize_amount)

    # Ngày hoặc số tiền không hợp lệ đều bị từ chối.
    invalid_date = normalized_dates.isna()
    invalid_amount = normalized_amounts.isna()
    invalid_mask = invalid_date | invalid_amount

    valid_df = df.loc[~invalid_mask].copy()
    valid_df["ngay"] = normalized_dates.loc[~invalid_mask].dt.strftime(
        "%Y-%m-%d"
    )
    valid_df["thanh_tien"] = normalized_amounts.loc[~invalid_mask]

    reject_df = df.loc[invalid_mask].copy()

    def rejection_reason(index):
        reasons = []

        if invalid_date.loc[index]:
            value = original_dates.loc[index]
            reasons.append(
                "Ngày bị trống"
                if not str(value).strip()
                else f"Không chuyển đổi được ngày: {value}"
            )

        if invalid_amount.loc[index]:
            value = original_amounts.loc[index]
            reasons.append(
                "Số tiền bị trống"
                if not str(value).strip()
                else f"Số tiền không hợp lệ: {value}"
            )

        return "; ".join(reasons)

    reject_df["ly_do_tu_choi"] = [
        rejection_reason(index) for index in reject_df.index
    ]

    valid_path = OUTPUT_DIR / "orders_normalized.csv"
    reject_path = OUTPUT_DIR / "orders_reject.csv"

    valid_df.to_csv(valid_path, index=False, encoding="utf-8-sig")
    reject_df.to_csv(reject_path, index=False, encoding="utf-8-sig")

    print("\n===== KẾT QUẢ XỬ LÝ ĐƠN HÀNG =====")
    print(f"Số dòng ban đầu: {rows_before:,}")
    print(f"Số dòng hợp lệ: {len(valid_df):,}")
    print(f"Số dòng bị từ chối: {len(reject_df):,}")
    print(f"Tổng sau phân loại: {len(valid_df) + len(reject_df):,}")
    print(f"\nFile dữ liệu chuẩn hóa: {valid_path}")
    print(f"File reject: {reject_path}")


if __name__ == "__main__":
    process_orders()
