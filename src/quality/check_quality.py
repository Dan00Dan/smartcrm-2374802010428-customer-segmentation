
from pathlib import Path
from numbers import Real
import math
import re

import pandas as pd

from src.transform.normalize_dates import normalize_date
from src.transform.normalize_amount import normalize_amount


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "docs"


def is_not_empty(value):
    """Kiểm tra giá trị không bị thiếu hoặc chỉ chứa khoảng trắng."""
    if pd.isna(value):
        return False

    return bool(str(value).strip())


def is_valid_amount(value):
    """Kiểm tra giá trị tiền có thể chuẩn hóa thành số không âm."""
    if pd.isna(value):
        return False

    if isinstance(value, Real):
        return math.isfinite(float(value)) and float(value) >= 0

    return not pd.isna(normalize_amount(value))


def is_consistent_date(value):
    """Kiểm tra ngày đã được chuẩn hóa theo YYYY-MM-DD."""
    if not is_not_empty(value):
        return False

    text = str(value).strip()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return False

    return not pd.isna(normalize_date(text))


def is_consistent_amount(value):
    """Kiểm tra thành tiền đã chuẩn hóa thành số không âm."""
    if pd.isna(value):
        return False

    return (
        isinstance(value, Real)
        and math.isfinite(float(value))
        and float(value) >= 0
    )


def measure_column_quality(data: pd.DataFrame) -> pd.DataFrame:
    """Đo Completeness, Validity và Consistency theo từng cột."""

    total_rows = len(data)
    records = []

    for column in data.columns:
        series = data[column]

        non_empty = series.map(is_not_empty)
        non_empty_count = int(non_empty.sum())

        completeness = (
            non_empty_count / total_rows * 100
            if total_rows > 0 else 0
        )

        validity = None
        consistency = None
        valid_count = None
        consistent_count = None

        if column == "ngay":
            valid_mask = series.map(
                lambda value: (
                    not pd.isna(normalize_date(value))
                    if is_not_empty(value)
                    else False
                )
            )

            consistent_mask = series.map(is_consistent_date)

        elif column == "thanh_tien":
            valid_mask = series.map(
                lambda value: (
                    is_valid_amount(value)
                    if is_not_empty(value)
                    else False
                )
            )

            consistent_mask = series.map(is_consistent_amount)

        else:
            valid_mask = None
            consistent_mask = None

        if valid_mask is not None:
            valid_count = int(valid_mask.sum())

            validity = (
                valid_count / non_empty_count * 100
                if non_empty_count > 0 else 0
            )

            consistent_count = int(consistent_mask.sum())

            consistency = (
                consistent_count / non_empty_count * 100
                if non_empty_count > 0 else 0
            )

        records.append({
            "column": column,
            "total_rows": total_rows,
            "non_empty": non_empty_count,
            "missing": total_rows - non_empty_count,
            "completeness_percent": round(completeness, 2),
            "valid": valid_count,
            "validity_percent": (
                round(validity, 2)
                if validity is not None else None
            ),
            "consistent": consistent_count,
            "consistency_percent": (
                round(consistency, 2)
                if consistency is not None else None
            ),
        })

    return pd.DataFrame(records)


def check_quality(
    valid_df: pd.DataFrame,
    reject_df: pd.DataFrame,
    rows_before: int,
) -> dict:
    """Kiểm tra bảo toàn dòng và đo chất lượng dữ liệu theo cột."""

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
                or (
                    reject_df["ly_do_tu_choi"]
                    .map(is_not_empty)
                    .all()
                )
            )
        ),
    }

    # Ghép lại các dòng để đánh giá toàn bộ dữ liệu đầu vào.
    combined_df = pd.concat(
        [valid_df, reject_df],
        ignore_index=True,
        sort=False,
    )

    # Loại cột lý do từ chối khỏi báo cáo chất lượng.
    combined_df = combined_df.drop(
        columns=["ly_do_tu_choi"],
        errors="ignore",
    )

    result["column_quality"] = measure_column_quality(
        combined_df
    ).to_dict(orient="records")

    print("\n===== KIỂM TRA CHẤT LƯỢNG =====")
    print(f"Bảo toàn số dòng: {result['row_count_matches']}")
    print(f"Dòng từ chối có lý do: {result['reject_has_reason']}")

    print("\n===== CHẤT LƯỢNG THEO CỘT =====")

    for item in result["column_quality"]:
        print(
            f"{item['column']}: "
            f"Completeness={item['completeness_percent']}%, "
            f"Validity={item['validity_percent']}, "
            f"Consistency={item['consistency_percent']}"
        )

    if not result["row_count_matches"]:
        raise ValueError(
            "Số dòng trước và sau phân loại không khớp."
        )

    if not result["reject_has_reason"]:
        raise ValueError(
            "Có dòng bị từ chối nhưng thiếu lý do."
        )

    return result
