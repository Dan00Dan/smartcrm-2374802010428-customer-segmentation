
from pathlib import Path

import pandas as pd

from src.transform.normalize_dates import normalize_date
from src.transform.normalize_amount import normalize_amount


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "orders_2024_2026.csv"


def process_orders(df: pd.DataFrame | None = None):
    """
    Chuẩn hóa đơn hàng và tách dữ liệu hợp lệ, dữ liệu bị từ chối.

    Nếu nhận DataFrame từ pipeline thì sử dụng lại dữ liệu đã đọc,
    tránh đọc file CSV lần thứ hai.
    Nếu không truyền DataFrame thì tự đọc file CSV như trước.
    """

    # Đọc dữ liệu khi không nhận DataFrame từ bên ngoài
    if df is None:
        if not RAW_FILE.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file dữ liệu: {RAW_FILE}"
            )

        df = pd.read_csv(
            RAW_FILE,
            dtype=str,
            keep_default_na=False
        )
    else:
        # Tạo bản sao để không làm thay đổi DataFrame gốc
        df = df.copy()

    # Kiểm tra các cột bắt buộc
    required_columns = {"ngay", "thanh_tien"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "File đơn hàng thiếu cột bắt buộc: "
            + ", ".join(sorted(missing_columns))
        )

    rows_before = len(df)

    # Lưu dữ liệu gốc để phục vụ ghi nhận lỗi
    original_dates = df["ngay"].copy()
    original_amounts = df["thanh_tien"].copy()

    # Chuẩn hóa ngày và số tiền
    normalized_dates = original_dates.map(normalize_date)
    normalized_amounts = original_amounts.map(normalize_amount)

    # Xác định dữ liệu không hợp lệ
    invalid_date = normalized_dates.isna()
    invalid_amount = normalized_amounts.isna()
    invalid_mask = invalid_date | invalid_amount

    # Tách dữ liệu hợp lệ
    valid_df = df.loc[~invalid_mask].copy()

    valid_df["ngay"] = (
        normalized_dates.loc[~invalid_mask]
        .dt.strftime("%Y-%m-%d")
    )

    valid_df["thanh_tien"] = normalized_amounts.loc[~invalid_mask]

    # Tách dữ liệu bị từ chối
    reject_df = df.loc[invalid_mask].copy()

    # Xác định nguyên nhân từ chối từng dòng
    def rejection_reason(index):
        reasons = []

        if invalid_date.loc[index]:
            value = original_dates.loc[index]

            if not str(value).strip():
                reasons.append("Ngày bị trống")
            else:
                reasons.append(
                    f"Không chuyển đổi được ngày: {value}"
                )

        if invalid_amount.loc[index]:
            value = original_amounts.loc[index]

            if not str(value).strip():
                reasons.append("Số tiền bị trống")
            else:
                reasons.append(
                    f"Số tiền không hợp lệ: {value}"
                )

        return "; ".join(reasons)

    reject_df["ly_do_tu_choi"] = [
        rejection_reason(index) for index in reject_df.index
    ]

    # Thống kê kết quả xử lý
    rows_valid = len(valid_df)
    rows_rejected = len(reject_df)

    print("\n===== KẾT QUẢ PHÂN LOẠI ĐƠN HÀNG =====")
    print(f"Số dòng ban đầu: {rows_before:,}")
    print(f"Số dòng hợp lệ: {rows_valid:,}")
    print(f"Số dòng bị từ chối: {rows_rejected:,}")
    print(f"Tổng sau phân loại: {rows_valid + rows_rejected:,}")

    return valid_df, reject_df, rows_before


if __name__ == "__main__":
    valid_df, reject_df, rows_before = process_orders()
