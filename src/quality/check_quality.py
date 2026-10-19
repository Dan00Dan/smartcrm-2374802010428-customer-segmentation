
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "docs"


def check_quality(valid_df: pd.DataFrame, reject_df: pd.DataFrame,
                  rows_before: int) -> dict:
    """Kiểm tra số dòng và tính đầy đủ của kết quả xử lý."""

    valid_count = len(valid_df)
    reject_count = len(reject_df)
    total_after = valid_count + reject_count

    result = {
        "rows_before": rows_before,
        "valid_rows": valid_count,
        "rejected_rows": reject_count,
        "rows_after": total_after,
        "row_count_matches": rows_before == total_after,
        "reject_has_reason": (
            "ly_do_tu_choi" in reject_df.columns
            and (
                reject_df.empty
                or reject_df["ly_do_tu_choi"].notna().all()
            )
        ),
    }

    print("\n===== KIỂM TRA CHẤT LƯỢNG =====")
    print(f"Bảo toàn số dòng: {result['row_count_matches']}")
    print(f"Dòng từ chối có lý do: {result['reject_has_reason']}")

    if not result["row_count_matches"]:
        raise ValueError("Số dòng trước và sau phân loại không khớp.")

    if not result["reject_has_reason"]:
        raise ValueError("Có dòng bị từ chối nhưng thiếu lý do.")

    return result
