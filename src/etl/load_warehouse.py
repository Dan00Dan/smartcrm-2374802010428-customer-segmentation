from pathlib import Path
import re

import pandas as pd


# Thư mục mặc định của dự án.
DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def normalize_phone(value):
    """Chuẩn hóa số điện thoại về chữ số, không tự đổi mã quốc gia."""
    if pd.isna(value):
        return ""
    return re.sub(r"\D", "", str(value))


def load_warehouse(root=None):
    """
    Nạp dữ liệu vào kho theo khóa nghiệp vụ.

    - Chỉ ghép khách hàng khi số điện thoại khớp duy nhất một hồ sơ.
    - Không tự ghép theo tên hoặc tự gộp hồ sơ trùng.
    - Đơn chưa xác định khách được gán UNKNOWN.
    - Chặn công bố phân khúc khi chưa xác minh trạng thái đơn hàng.
    - Cho phép truyền thư mục root để phục vụ kiểm thử.
    - Ghi lại snapshot, không cộng dồn khi chạy nhiều lần.
    """

    # Khi kiểm thử, cho phép sử dụng thư mục tạm.
    # Khi chạy thông thường, sử dụng thư mục dự án.
    root = Path(root) if root is not None else Path.cwd()

    customers_file = root / "data" / "raw" / "customers_raw.csv"
    orders_file = root / "data" / "processed" / "orders_normalized.csv"
    warehouse_dir = root / "data" / "warehouse"
    docs_dir = root / "docs"

    # Kiểm tra sự tồn tại của dữ liệu nguồn.
    if not customers_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu khách hàng: {customers_file}"
        )

    if not orders_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu đơn hàng: {orders_file}"
        )

    # Đọc dữ liệu nguồn.
    customers = pd.read_csv(customers_file, dtype=str)
    orders = pd.read_csv(orders_file, dtype=str)

    # Kiểm tra các cột bắt buộc.
    required_customer = {
        "record_id",
        "ho_ten",
        "so_dien_thoai",
    }

    required_order = {
        "ma_don",
        "ma_cua_hang",
        "ngay",
        "so_dien_thoai",
        "thanh_tien",
    }

    if not required_customer.issubset(customers.columns):
        missing = required_customer - set(customers.columns)
        raise ValueError(
            f"customers_raw.csv thiếu cột bắt buộc: {sorted(missing)}"
        )

    if not required_order.issubset(orders.columns):
        missing = required_order - set(orders.columns)
        raise ValueError(
            f"orders_normalized.csv thiếu cột bắt buộc: {sorted(missing)}"
        )

    # ---------------------------------------------------------
    # 1. KIỂM TRA HỒ SƠ KHÁCH HÀNG
    # ---------------------------------------------------------

    customers["record_id"] = (
        customers["record_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    if customers["record_id"].eq("").any():
        raise ValueError("Có hồ sơ khách hàng thiếu record_id.")

    if customers["record_id"].duplicated().any():
        raise ValueError(
            "record_id bị trùng; dừng nạp để rà soát."
        )

    customers["phone_norm"] = customers["so_dien_thoai"].map(
        normalize_phone
    )

    # Tạo dimension khách hàng.
    customer_dim = customers[
        ["record_id", "ho_ten"]
    ].rename(
        columns={
            "record_id": "customer_key",
            "ho_ten": "full_name",
        }
    )

    # Chỉ sử dụng số điện thoại xuất hiện ở đúng một hồ sơ.
    phone_counts = (
        customers.loc[customers["phone_norm"].ne("")]
        .groupby("phone_norm")["record_id"]
        .nunique()
    )

    unique_phones = set(
        phone_counts[phone_counts == 1].index
    )

    phone_to_customer = (
        customers.loc[
            customers["phone_norm"].isin(unique_phones)
        ]
        .set_index("phone_norm")["record_id"]
        .to_dict()
    )

    # Thêm hồ sơ UNKNOWN.
    unknown_row = pd.DataFrame(
        [
            {
                "customer_key": "UNKNOWN",
                "full_name": "Không xác định",
            }
        ]
    )

    customer_dim = pd.concat(
        [unknown_row, customer_dim],
        ignore_index=True,
    )

    # ---------------------------------------------------------
    # 2. KIỂM TRA VÀ CHUẨN HÓA ĐƠN HÀNG
    # ---------------------------------------------------------

    orders["ma_cua_hang"] = (
        orders["ma_cua_hang"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    orders["ma_don"] = (
        orders["ma_don"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    if orders["ma_cua_hang"].eq("").any():
        raise ValueError("Có đơn hàng thiếu mã cửa hàng.")

    if orders["ma_don"].eq("").any():
        raise ValueError("Có đơn hàng thiếu mã đơn.")

    # Khóa nghiệp vụ tạm thời: mã cửa hàng + mã đơn.
    orders["store_order_key"] = (
        orders["ma_cua_hang"] + "|" + orders["ma_don"]
    )

    if orders["store_order_key"].duplicated().any():
        raise ValueError(
            "Khóa cửa hàng + mã đơn bị trùng; dừng nạp để rà soát."
        )

    # Ghép khách hàng bằng số điện thoại duy nhất.
    orders["phone_norm"] = orders["so_dien_thoai"].map(
        normalize_phone
    )

    orders["customer_key"] = orders["phone_norm"].map(
        phone_to_customer
    )

    orders["customer_key"] = (
        orders["customer_key"].fillna("UNKNOWN")
    )

    # Chuyển ngày và số tiền sang kiểu dữ liệu phù hợp.
    orders["order_date"] = pd.to_datetime(
        orders["ngay"],
        errors="coerce",
    )

    orders["amount"] = pd.to_numeric(
        orders["thanh_tien"],
        errors="coerce",
    )

    orders["analysis_month"] = (
        orders["order_date"].dt.strftime("%Y-%m")
    )

    # Chưa có trạng thái đơn đã hoàn tất trong nguồn.
    # Không tự giả định đơn hàng đã hoàn tất.
    orders["order_status"] = "UNKNOWN"
    orders["segment_publishable"] = False

    # Tạo bảng fact đơn hàng.
    fact_order = orders[
        [
            "store_order_key",
            "ma_don",
            "ma_cua_hang",
            "customer_key",
            "order_date",
            "analysis_month",
            "amount",
            "order_status",
            "segment_publishable",
        ]
    ].rename(
        columns={
            "store_order_key": "order_business_key",
            "ma_don": "order_id_source",
            "ma_cua_hang": "store_id",
        }
    )

    # Thêm customer_id để tương thích với các bài test cũ.
    fact_order["customer_id"] = fact_order["customer_key"]

    # ---------------------------------------------------------
    # 3. TẠO DIMENSION KỲ PHÂN TÍCH
    # ---------------------------------------------------------

    months = sorted(
        fact_order["analysis_month"].dropna().unique()
    )

    dim_period = pd.DataFrame(
        {"analysis_month": months}
    )

    dim_period["period_key"] = (
        dim_period["analysis_month"].str.replace(
            "-", "",
            regex=False,
        )
    )

    # Ngày chốt là ngày đầu tiên của tháng kế tiếp.
    dim_period["cutoff_date"] = (
        pd.to_datetime(
            dim_period["analysis_month"] + "-01"
        )
        + pd.offsets.MonthBegin(1)
    ).dt.strftime("%Y-%m-%d")

    dim_period["status"] = "BLOCKED_SOURCE_VALIDATION"

    dim_period = dim_period[
        [
            "period_key",
            "analysis_month",
            "cutoff_date",
            "status",
        ]
    ]

    # ---------------------------------------------------------
    # 4. GHI NHẬN VẤN ĐỀ CHẤT LƯỢNG DỮ LIỆU
    # ---------------------------------------------------------

    issue_records = []

    for _, row in fact_order.iterrows():

        if row["customer_key"] == "UNKNOWN":
            issue_records.append(
                {
                    "order_business_key": row["order_business_key"],
                    "order_id_source": row["order_id_source"],
                    "store_id": row["store_id"],
                    "issue_code": "CUSTOMER_NOT_RESOLVED",
                }
            )

        if pd.isna(row["order_date"]):
            issue_records.append(
                {
                    "order_business_key": row["order_business_key"],
                    "order_id_source": row["order_id_source"],
                    "store_id": row["store_id"],
                    "issue_code": "INVALID_ORDER_DATE",
                }
            )

        if pd.isna(row["amount"]):
            issue_records.append(
                {
                    "order_business_key": row["order_business_key"],
                    "order_id_source": row["order_id_source"],
                    "store_id": row["store_id"],
                    "issue_code": "INVALID_ORDER_AMOUNT",
                }
            )

    issues = pd.DataFrame(
        issue_records,
        columns=[
            "order_business_key",
            "order_id_source",
            "store_id",
            "issue_code",
        ],
    )

    # ---------------------------------------------------------
    # 5. GHI DỮ LIỆU KHO
    # ---------------------------------------------------------

    warehouse_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    docs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    customer_dim.to_csv(
        warehouse_dir / "dim_customer.csv",
        index=False,
        encoding="utf-8-sig",
    )

    dim_period.to_csv(
        warehouse_dir / "dim_period.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Giữ tên file số ít để tương thích với cấu trúc kho hiện tại.
    fact_order.to_csv(
        warehouse_dir / "fact_order.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Ghi thêm tên file số nhiều để tương thích với các bài test.
    fact_order.to_csv(
        warehouse_dir / "fact_orders.csv",
        index=False,
        encoding="utf-8-sig",
    )

    issues.to_csv(
        warehouse_dir / "data_quality_issues.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ---------------------------------------------------------
    # 6. TẠO BÁO CÁO
    # ---------------------------------------------------------

    report = [
        "# Báo cáo nạp kho dữ liệu",
        "",
        f"- Hồ sơ khách hàng (gồm UNKNOWN): {len(customer_dim):,}",
        f"- Đơn hàng đã nạp: {len(fact_order):,}",
        f"- Số vấn đề chất lượng dữ liệu: {len(issues):,}",
        (
            "- Đơn chưa xác định khách: "
            f"{fact_order['customer_key'].eq('UNKNOWN').sum():,}"
        ),
        (
            "- Khóa đơn hàng trùng trong kho: "
            f"{fact_order['order_business_key'].duplicated().sum()}"
        ),
        "- Trạng thái đơn hoàn tất: chưa có trong dữ liệu nguồn.",
        "- Công bố phân khúc: ĐANG CHẶN cho đến khi xác minh dữ liệu nguồn.",
        "- Cách nạp: ghi lại snapshot; chạy lại không cộng dồn bản ghi.",
        "",
        (
            "Lưu ý: khóa cửa hàng + mã đơn là khóa kỹ thuật tạm dùng "
            "theo dữ liệu hiện có, cần được xác nhận về mặt nghiệp vụ."
        ),
    ]

    (docs_dir / "bao-cao-nap-kho.md").write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print("NAP KHO DU LIEU HOAN TAT")
    print(f"So ho so dim_customer: {len(customer_dim):,}")
    print(f"So don fact_order: {len(fact_order):,}")
    print(f"So van de chat luong du lieu: {len(issues):,}")
    print("Cong bo phan khuc: BLOCKED_SOURCE_VALIDATION")
    print(f"Ket qua: {warehouse_dir}")


if __name__ == "__main__":
    load_warehouse()