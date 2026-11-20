
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "docs"


# Các cột chứa thông tin định danh trực tiếp hoặc dữ liệu
# trung gian dùng để đối chiếu danh tính khách hàng.
PII_COLUMNS = {
    "ho_ten",
    "ten_khach",
    "so_dien_thoai",
    "phone",
    "phone_norm",
    "email",
    "dia_chi",
    "address",
    "name",
    "name_norm",
    "customer_name",
    "nhan_vien",
    "ghi_chu",
}

def remove_personal_information(df: pd.DataFrame) -> pd.DataFrame:
    """Loại bỏ thông tin định danh trực tiếp trước khi xuất CSV."""

    safe_df = df.copy()

    columns_to_drop = [
        column
        for column in safe_df.columns
        if column.lower() in PII_COLUMNS
    ]

    return safe_df.drop(columns=columns_to_drop, errors="ignore")


def save_results(
    valid_df: pd.DataFrame,
    reject_df: pd.DataFrame,
    quality_result: dict,
) -> None:
    """Lưu dữ liệu đã xử lý và báo cáo chất lượng an toàn."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    valid_path = OUTPUT_DIR / "orders_normalized.csv"
    reject_path = OUTPUT_DIR / "orders_reject.csv"
    report_path = REPORT_DIR / "bao-cao-chat-luong.md"
    quality_csv_path = REPORT_DIR / "data-quality-by-column.csv"

    # =====================================================
    # 1. LOẠI BỎ THÔNG TIN CÁ NHÂN
    # =====================================================

    safe_valid_df = remove_personal_information(valid_df)
    safe_reject_df = remove_personal_information(reject_df)

    # Chỉ lưu dữ liệu đã loại bỏ thông tin định danh.
    safe_valid_df.to_csv(
        valid_path,
        index=False,
        encoding="utf-8-sig",
    )

    safe_reject_df.to_csv(
        reject_path,
        index=False,
        encoding="utf-8-sig",
    )

    # =====================================================
    # 2. XUẤT THỐNG KÊ CHẤT LƯỢNG THEO CỘT
    # =====================================================

    quality_df = pd.DataFrame(
        quality_result["column_quality"]
    )

    quality_df.to_csv(
        quality_csv_path,
        index=False,
        encoding="utf-8-sig",
    )

    # =====================================================
    # 3. TẠO BẢNG BÁO CÁO CHẤT LƯỢNG
    # =====================================================

    table_rows = []

    for item in quality_result["column_quality"]:
        validity = (
            f"{item['validity_percent']:.2f}%"
            if item["validity_percent"] is not None
            else "N/A"
        )

        consistency = (
            f"{item['consistency_percent']:.2f}%"
            if item["consistency_percent"] is not None
            else "N/A"
        )

        table_rows.append(
            f"| {item['column']} "
            f"| {item['total_rows']} "
            f"| {item['non_empty']} "
            f"| {item['missing']} "
            f"| {item['completeness_percent']:.2f}% "
            f"| {validity} "
            f"| {consistency} |"
        )

    quality_table = "\n".join(table_rows)

    # =====================================================
    # 4. TẠO BÁO CÁO MARKDOWN
    # =====================================================

    report = f"""# Báo cáo chất lượng dữ liệu đơn hàng

## 1. Tổng quan

- Số dòng đầu vào: {quality_result["rows_before"]:,}
- Số dòng hợp lệ: {quality_result["valid_rows"]:,}
- Số dòng bị từ chối: {quality_result["rejected_rows"]:,}
- Tổng dòng sau phân loại: {quality_result["rows_after"]:,}

## 2. Kết quả kiểm tra

- Bảo toàn số dòng: {quality_result["row_count_matches"]}
- Dòng từ chối có lý do: {quality_result["reject_has_reason"]}

## 3. Đánh giá chất lượng theo từng cột

| Cột dữ liệu | Tổng dòng | Không thiếu | Thiếu | Completeness | Validity | Consistency |
|---|---:|---:|---:|---:|---:|---:|
{quality_table}

**Giải thích các chỉ số:**

- **Completeness:** Tỷ lệ dữ liệu không bị thiếu trên tổng số dòng.
- **Validity:** Tỷ lệ giá trị đáp ứng quy tắc hợp lệ trên số giá trị không thiếu.
- **Consistency:** Tỷ lệ giá trị đúng định dạng chuẩn trên số giá trị không thiếu.
- **N/A:** Chưa thiết lập quy tắc Validity hoặc Consistency cho cột đó.

## 4. Bảo vệ dữ liệu cá nhân

- Các file CSV đầu ra đã loại bỏ những cột định danh trực tiếp.
- Thông tin khách hàng được sử dụng trong bộ nhớ để đối chiếu.
- Warehouse sử dụng mã khách hàng giả danh HMAC-SHA256.
- Không xuất tên, số điện thoại, email và địa chỉ vào các bảng Warehouse.

## 5. File đầu ra

- Dữ liệu hợp lệ: `data/processed/orders_normalized.csv`
- Dữ liệu bị từ chối: `data/processed/orders_reject.csv`
- Báo cáo chất lượng CSV: `docs/data-quality-by-column.csv`
- Báo cáo tổng hợp: `docs/bao-cao-chat-luong.md`
"""

    report_path.write_text(
        report,
        encoding="utf-8",
    )

    print("\n===== LƯU KẾT QUẢ =====")
    print(f"Báo cáo chất lượng: {report_path}")
    print(f"Báo cáo CSV theo cột: {quality_csv_path}")
    print(f"Dữ liệu hợp lệ (đã loại PII): {valid_path}")
    print(f"Dữ liệu bị từ chối (đã loại PII): {reject_path}")
