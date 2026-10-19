import pandas as pd
import re


def normalize_amount(value):
    """Chuẩn hóa số tiền Việt Nam; trả về NaN nếu trống hoặc không hợp lệ."""

    if pd.isna(value):
        return float("nan")

    value = str(value).strip()

    if not value:
        return float("nan")

    # Loại bỏ khoảng trắng bên trong chuỗi.
    value = re.sub(r"\s+", "", value)

    # Loại bỏ ký hiệu tiền Việt Nam ở cuối chuỗi.
    value = re.sub(r"[đĐ₫]$", "", value)

    # Trường hợp số nguyên, ví dụ: 34980500
    if re.fullmatch(r"\d+", value):
        return float(value)

    # Trường hợp có dấu chấm phân cách hàng nghìn, ví dụ: 34.980.500
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", value):
        return float(value.replace(".", ""))

    # Giá trị không hợp lệ hoặc không đúng định dạng hỗ trợ.
    return float("nan")
