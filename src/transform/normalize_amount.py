import pandas as pd
import re


def normalize_amount(value):
    """Chuẩn hóa số tiền Việt Nam; trả về NaN nếu trống hoặc không hợp lệ."""
    if pd.isna(value):
        return float("nan")

    value = str(value).strip()
    if not value:
        return float("nan")

    # Bỏ hậu tố tiền tệ và khoảng trắng.
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"[đĐ₫]$", "", value)

    # Số nguyên không có dấu phân cách.
    if re.fullmatch(r"\d+", value):
        return float(value)

    # Số có dấu chấm phân cách hàng nghìn theo định dạng Việt Nam.
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", value):
        return float(value.replace(".", ""))

    # Không chấp nhận số âm, chữ hoặc định dạng không rõ ràng.
    return float("nan")
