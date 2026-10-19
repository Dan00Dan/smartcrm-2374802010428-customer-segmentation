
import pandas as pd


def normalize_date(value):
    """Chuẩn hóa ngày về YYYY-MM-DD; trả về NaT nếu không hợp lệ."""
    if pd.isna(value) or not str(value).strip():
        return pd.NaT

    value = str(value).strip()

    formats = (
        "%d/%m/%Y",  # 17/08/2025
        "%d/%m/%y",  # 17/08/25
        "%d-%m-%Y",  # 17-08-2025
        "%d-%m-%y",  # 12-8-26
        "%Y.%m.%d",  # 2025.03.22
        "%Y-%m-%d",  # 2025-03-22
    )

    for fmt in formats:
        try:
            return pd.to_datetime(value, format=fmt, errors="raise")
        except (ValueError, TypeError):
            continue

    return pd.NaT
