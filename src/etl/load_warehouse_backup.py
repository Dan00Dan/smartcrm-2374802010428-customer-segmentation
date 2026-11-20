
from pathlib import Path
import re
import unicodedata

import pandas as pd


# =========================================================
# 0. CẤU HÌNH VÀ HÀM CHUẨN HÓA
# =========================================================

DEFAULT_ROOT = Path(__file__).resolve().parents[2]


def normalize_phone(value):
    """Chuẩn hóa số điện thoại Việt Nam về dạng 0xxxxxxxxx."""
    if pd.isna(value):
        return ""

    phone = re.sub(r"\D", "", str(value).strip())

    if phone.startswith("0084"):
        phone = "0" + phone[4:]
    elif phone.startswith("84") and len(phone) == 11:
        phone = "0" + phone[2:]

    return phone


def normalize_name(value):
    """Chuẩn hóa tên: bỏ dấu, khoảng trắng và ký tự đặc biệt."""
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    text = re.sub(r"[^a-z0-9]", "", text)

    return text


# =========================================================
# 1. NẠP KHO DỮ LIỆU
# =========================================================

def load_warehouse(root=None):
    """
    Nạp dữ liệu vào Data Warehouse theo khóa nghiệp vụ.

    - Ghép khách hàng bằng số điện thoại duy nhất.
    - Nếu điện thoại trùng: thử ghép điện thoại + tên.
    - Không đủ căn cứ: gán UNKNOWN.
    - Không tự gộp hồ sơ khách hàng.
    - Chặn công bố phân khúc khi chưa xác minh trạng thái đơn.
    - Hỗ trợ dữ liệu kiểm thử không có ten_khach.
    - Ghi snapshot, không cộng dồn dữ liệu.
    """

    root = Path(root) if root is not None else Path.cwd()

    customers_file = (
        root / "data" / "raw" / "customers_raw.csv"
    )

    orders_file = (
        root / "data" / "processed" / "orders_normalized.csv"
    )

    warehouse_dir = root / "data" / "warehouse"
    docs_dir = root / "docs"

    # ---------------------------------------------------------
    # 1.1 KIỂM TRA FILE NGUỒN
    # ---------------------------------------------------------

    if not customers_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu khách hàng: {customers_file}"
        )

    if not orders_file.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dữ liệu đơn hàng: {orders_file}"
        )

    customers = pd.read_csv(
        customers_file,
        dtype=str,
    )

    orders = pd.read_csv(
        orders_file,
        dtype=str,
    )

    # ---------------------------------------------------------
    # 1.2 KIỂM TRA CỘT BẮT BUỘC
    # ---------------------------------------------------------

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

    # =========================================================
    # 2. DIMENSION KHÁCH HÀNG
    # =========================================================

    customers["record_id"] = (
        customers["record_id"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    if customers["record_id"].eq("").any():
        raise ValueError(
            "Có hồ sơ khách hàng thiếu record_id."
        )

    if customers["record_id"].duplicated().any():
        raise ValueError(
            "record_id bị trùng; dừng nạp để rà soát."
        )

    customers["phone_norm"] = (
        customers["so_dien_thoai"]
        .map(normalize_phone)
    )

    customers["name_norm"] = (
        customers["ho_ten"]
        .map(normalize_name)
    )

    customer_dim = customers[
        ["record_id", "ho_ten"]
    ].rename(
        columns={
            "record_id": "customer_key",
            "ho_ten": "full_name",
        }
    )

    # ---------------------------------------------------------
    # 2.1 ÁNH XẠ THEO SỐ ĐIỆN THOẠI DUY NHẤT
    # ---------------------------------------------------------

    phone_counts = (
        customers.loc[
            customers["phone_norm"].ne("")
        ]
        .groupby("phone_norm")["record_id"]
        .nunique()
    )

    unique_phones = set(
        phone_counts[
            phone_counts == 1
        ].index
    )

    phone_to_customer = (
        customers.loc[
            customers["phone_norm"].isin(unique_phones)
        ]
        .set_index("phone_norm")["record_id"]
        .to_dict()
    )

    # ---------------------------------------------------------
    # 2.2 ÁNH XẠ THEO ĐIỆN THOẠI + TÊN
    # ---------------------------------------------------------

    valid_customer_pairs = customers.loc[
        customers["phone_norm"].ne("")
        & customers["name_norm"].ne("")
    ].copy()

    pair_counts = (
        valid_customer_pairs
        .groupby(
            ["phone_norm", "name_norm"]
        )["record_id"]
        .nunique()
    )

    # Chỉ giữ cặp xác định được đúng một record_id.
    unique_pairs = (
        pair_counts[pair_counts == 1]
        .reset_index()[
            ["phone_norm", "name_norm"]
        ]
    )

    unique_customer_pairs = (
        valid_customer_pairs
        .merge(
            unique_pairs,
            on=["phone_norm", "name_norm"],
            how="inner",
        )
        .drop_duplicates(
            ["phone_norm", "name_norm", "record_id"]
        )
    )

    phone_name_to_customer = (
        unique_customer_pairs
        .set_index(
            ["phone_norm", "name_norm"]
        )["record_id"]
        .to_dict()
    )

    # ---------------------------------------------------------
    # 2.3 THÊM KHÁCH HÀNG UNKNOWN
    # ---------------------------------------------------------

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

    # =========================================================
    # 3. CHUẨN HÓA VÀ GHÉP ĐƠN HÀNG
    # =========================================================

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
        raise ValueError(
            "Có đơn hàng thiếu mã cửa hàng."
        )

    if orders["ma_don"].eq("").any():
        raise ValueError(
            "Có đơn hàng thiếu mã đơn."
        )

    # Khóa nghiệp vụ đơn hàng.
    orders["store_order_key"] = (
        orders["ma_cua_hang"]
        + "|"
        + orders["ma_don"]
    )

    if orders["store_order_key"].duplicated().any():
        raise ValueError(
            "Khóa cửa hàng + mã đơn bị trùng; "
            "dừng nạp để rà soát."
        )

    # ---------------------------------------------------------
    # 3.1 CHUẨN HÓA ĐIỆN THOẠI
    # ---------------------------------------------------------

    orders["phone_norm"] = (
        orders["so_dien_thoai"]
        .map(normalize_phone)
    )

    # ---------------------------------------------------------
    # 3.2 CHUẨN HÓA TÊN KHÁCH HÀNG
    # ---------------------------------------------------------
    # ten_khach là cột tùy chọn.
    # Nếu không có cột này, không đối chiếu theo tên.

    if "ten_khach" in orders.columns:
        orders["name_norm"] = (
            orders["ten_khach"]
            .map(normalize_name)
        )
    else:
        orders["name_norm"] = ""

    # ---------------------------------------------------------
    # 3.3 BƯỚC 1: GHÉP BẰNG ĐIỆN THOẠI DUY NHẤT
    # ---------------------------------------------------------

    orders["customer_key"] = (
        orders["phone_norm"]
        .map(phone_to_customer)
    )

    # ---------------------------------------------------------
    # 3.4 BƯỚC 2: GHÉP BẰNG ĐIỆN THOẠI + TÊN
    # ---------------------------------------------------------

    unresolved = orders["customer_key"].isna()

    matched_by_phone_name = pd.Series(
        [
            phone_name_to_customer.get(
                (phone, name)
            )
            for phone, name in zip(
                orders.loc[unresolved, "phone_norm"],
                orders.loc[unresolved, "name_norm"],
            )
        ],
        index=orders.index[unresolved],
        dtype="object",
    )

    orders.loc[
        unresolved,
        "customer_key"
    ] = matched_by_phone_name

    # ---------------------------------------------------------
    # 3.5 BƯỚC 3: GÁN UNKNOWN
    # ---------------------------------------------------------

    orders["customer_key"] = (
        orders["customer_key"]
        .fillna("UNKNOWN")
        .astype(str)
    )

    # =========================================================
    # 4. CHUẨN HÓA NGÀY, TIỀN VÀ TRẠNG THÁI
    # =========================================================

    orders["order_date"] = pd.to_datetime(
        orders["ngay"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )

    orders["amount"] = pd.to_numeric(
        orders["thanh_tien"],
        errors="coerce",
    )

    orders["analysis_month"] = (
        orders["order_date"]
        .dt.strftime("%Y-%m")
    )

    # Nguồn chưa có trạng thái hoàn tất.
    orders["order_status"] = "UNKNOWN"
    orders["segment_publishable"] = False

    # =========================================================
    # 5. FACT ĐƠN HÀNG
    # =========================================================

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

    # Tương thích các bài test cũ.
    fact_order["customer_id"] = (
        fact_order["customer_key"]
    )

    # =========================================================
    # 6. DIMENSION KỲ PHÂN TÍCH
    # =========================================================

    months = sorted(
        fact_order["analysis_month"]
        .dropna()
        .unique()
    )

    dim_period = pd.DataFrame(
        {"analysis_month": months}
    )

    dim_period["period_key"] = (
        dim_period["analysis_month"]
        .str.replace("-", "", regex=False)
    )

    dim_period["cutoff_date"] = (
        pd.to_datetime(
            dim_period["analysis_month"] + "-01"
        )
        + pd.offsets.MonthBegin(1)
    ).dt.strftime("%Y-%m-%d")

    dim_period["status"] = (
        "BLOCKED_SOURCE_VALIDATION"
    )

    dim_period = dim_period[
        [
            "period_key",
            "analysis_month",
            "cutoff_date",
            "status",
        ]
    ]

    # =========================================================
    # 7. GHI NHẬN VẤN ĐỀ CHẤT LƯỢNG DỮ LIỆU
    # =========================================================

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

    # =========================================================
    # 8. GHI DỮ LIỆU WAREHOUSE
    # =========================================================

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

    fact_order.to_csv(
        warehouse_dir / "fact_order.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Tương thích tên file số nhiều.
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

    # =========================================================
    # 9. BÁO CÁO NẠP KHO
    # =========================================================

    unknown_count = (
        fact_order["customer_key"]
        .eq("UNKNOWN")
        .sum()
    )

    report = [
        "# Báo cáo nạp kho dữ liệu",
        "",
        f"- Hồ sơ khách hàng (gồm UNKNOWN): {len(customer_dim):,}",
        f"- Đơn hàng đã nạp: {len(fact_order):,}",
        f"- Số vấn đề chất lượng dữ liệu: {len(issues):,}",
        f"- Đơn chưa xác định khách: {unknown_count:,}",
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
