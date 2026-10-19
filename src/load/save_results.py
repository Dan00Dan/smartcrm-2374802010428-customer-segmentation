
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "docs"


def save_results(
    valid_df: pd.DataFrame,
    reject_df: pd.DataFrame,
    quality_result: dict,
) -> None:
    """Lưu dữ liệu đã xử lý và báo cáo chất lượng."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    valid_path = OUTPUT_DIR / "orders_normalized.csv"
    reject_path = OUTPUT_DIR / "orders_reject.csv"
    report_path = REPORT_DIR / "bao-cao-chat-luong.md"

    valid_df.to_csv(valid_path, index=False, encoding="utf-8-sig")
    reject_df.to_csv(reject_path, index=False, encoding="utf-8-sig")

    report = f"""# Báo cáo chất lượng dữ liệu đơn hàng

## 1. Tổng quan

- Số dòng đầu vào: {quality_result["rows_before"]:,}
- Số dòng hợp lệ: {quality_result["valid_rows"]:,}
- Số dòng bị từ chối: {quality_result["rejected_rows"]:,}
- Tổng dòng sau phân loại: {quality_result["rows_after"]:,}

## 2. Kết quả kiểm tra

- Bảo toàn số dòng: {quality_result["row_count_matches"]}
- Dòng từ chối có lý do: {quality_result["reject_has_reason"]}

## 3. File đầu ra

- Dữ liệu hợp lệ: `data/processed/orders_normalized.csv`
- Dữ liệu bị từ chối: `data/processed/orders_reject.csv`
"""

    report_path.write_text(report, encoding="utf-8")

    print(f"Báo cáo chất lượng: {report_path}")
    print(f"Dữ liệu hợp lệ: {valid_path}")
    print(f"Dữ liệu bị từ chối: {reject_path}")
