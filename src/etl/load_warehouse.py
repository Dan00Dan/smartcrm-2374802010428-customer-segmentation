
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
    """Chuẩn hóa tên tiếng Việt, xử lý cả đ/Đ."""
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()

    # Chuyển đ thành d trước khi loại dấu Unicode
    text = text.replace("đ", "d")

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return re.sub(r"[^a-z0-9]", "", text)


def normalize_text(value):
    """Chuẩn hóa văn bản dùng để thống kê email/địa chỉ."""
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


# =========================================================
# 1. NẠP KHO DỮ LIỆU
# =========================================================

def load_warehouse(root=None):

    root = Path(root) if root is not None else Path.cwd()

    customers_file = root / "data" / "raw" / "customers_raw.csv"
    orders_file = root / "data" / "processed" / "orders_normalized.csv"

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

    customers = pd.read_csv(customers_file, dtype=str)
    orders = pd.read_csv(orders_file, dtype=str)

    # Kiểm tra thiếu mã hồ sơ khách hàng
    if customers["record_id"].fillna("").str.strip().eq("").any():
        raise ValueError("Có hồ sơ khách hàng thiếu record_id.")

    # Kiểm tra trùng mã hồ sơ khách hàng
    if customers["record_id"].duplicated().any():
        raise ValueError("Duplicate customer record_id detected")
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
            f"customers_raw.csv thiếu cột: {sorted(missing)}"
        )

    if not required_order.issubset(orders.columns):
        missing = required_order - set(orders.columns)
        raise ValueError(
            f"orders_normalized.csv thiếu cột: {sorted(missing)}"
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
        raise ValueError("Có hồ sơ khách hàng thiếu record_id.")

    if customers["record_id"].duplicated().any():
        raise ValueError("record_id bị trùng; dừng nạp.")

    customers["phone_norm"] = customers["so_dien_thoai"].map(
        normalize_phone
    )

    customers["name_norm"] = customers["ho_ten"].map(
        normalize_name
    )

    # Giữ nguyên toàn bộ hồ sơ khách hàng gốc.
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

    # ---------------------------------------------------------
    # 2.2 NHÓM HỒ SƠ THEO SĐT + TÊN CHUẨN HÓA
    # ---------------------------------------------------------

    valid_pairs = customers.loc[
        customers["phone_norm"].ne("")
        & customers["name_norm"].ne("")
    ].copy()

    # Sắp xếp để chọn đại diện ổn định.
    valid_pairs["_record_sort"] = pd.to_numeric(
        valid_pairs["record_id"],
        errors="coerce",
    )

    valid_pairs = valid_pairs.sort_values(
        ["_record_sort", "record_id"],
        na_position="last",
    )

    # Thống kê từng nhóm SĐT + tên.
    pair_groups = (
        valid_pairs.groupby(
            ["phone_norm", "name_norm"],
            as_index=False,
        )
        .agg(
            candidate_count=("record_id", "nunique"),
            representative_record_id=("record_id", "first"),
            candidate_record_ids=(
                "record_id",
                lambda values: "|".join(
                    sorted(set(values.astype(str)))
                ),
            ),
        )
    )

    # ---------------------------------------------------------
    # 2.2.1 THỐNG KÊ EMAIL
    # ---------------------------------------------------------

    if "email" in valid_pairs.columns:
        valid_pairs["_email_norm"] = valid_pairs["email"].map(
            normalize_text
        )

        email_stats = (
            valid_pairs.groupby(
                ["phone_norm", "name_norm"]
            )["_email_norm"]
            .agg(
                lambda values: values[values.ne("")].nunique()
            )
            .rename("email_distinct_count")
            .reset_index()
        )

        pair_groups = pair_groups.merge(
            email_stats,
            on=["phone_norm", "name_norm"],
            how="left",
        )
    else:
        pair_groups["email_distinct_count"] = 0

    # ---------------------------------------------------------
    # 2.2.2 THỐNG KÊ ĐỊA CHỈ
    # ---------------------------------------------------------

    if "dia_chi" in valid_pairs.columns:
        valid_pairs["_address_norm"] = valid_pairs["dia_chi"].map(
            normalize_text
        )

        address_stats = (
            valid_pairs.groupby(
                ["phone_norm", "name_norm"]
            )["_address_norm"]
            .agg(
                lambda values: values[values.ne("")].nunique()
            )
            .rename("address_distinct_count")
            .reset_index()
        )

        pair_groups = pair_groups.merge(
            address_stats,
            on=["phone_norm", "name_norm"],
            how="left",
        )
    else:
        pair_groups["address_distinct_count"] = 0

    # ---------------------------------------------------------
    # 2.2.3 ÁNH XẠ SĐT + TÊN VỀ HỒ SƠ ĐẠI DIỆN
    # ---------------------------------------------------------

    phone_name_to_customer = {
        (row["phone_norm"], row["name_norm"]):
        row["representative_record_id"]
        for _, row in pair_groups.iterrows()
    }

    # ---------------------------------------------------------
    # 2.3 BẢNG KIỂM TRA HỒ SƠ NGHI TRÙNG
    # ---------------------------------------------------------

    duplicate_candidates = pair_groups.loc[
        pair_groups["candidate_count"] > 1
    ].copy()

    duplicate_candidates = duplicate_candidates[
        [
            "phone_norm",
            "name_norm",
            "candidate_count",
            "representative_record_id",
            "candidate_record_ids",
            "email_distinct_count",
            "address_distinct_count",
        ]
    ]

    # ---------------------------------------------------------
    # 2.4 THÊM KHÁCH HÀNG UNKNOWN
    # ---------------------------------------------------------

    unknown_row = pd.DataFrame(
        [{
            "customer_key": "UNKNOWN",
            "full_name": "Không xác định",
        }]
    )

    customer_dim = pd.concat(
        [unknown_row, customer_dim],
        ignore_index=True,
    )

    # =========================================================
    # 3. CHUẨN HÓA VÀ GHÉP ĐƠN HÀNG
    # =========================================================

# ---------------------------------------------------------
# 3.0 TẠO VÀ KIỂM TRA KHÓA ĐƠN HÀNG
# ---------------------------------------------------------

    for column in ["ma_cua_hang", "ma_don"]:
        orders[column] = (
            orders[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if orders["ma_cua_hang"].eq("").any():
        raise ValueError("Có đơn hàng thiếu mã cửa hàng.")

    if orders["ma_don"].eq("").any():
        raise ValueError("Có đơn hàng thiếu mã đơn.")

    orders["order_business_key"] = (
        orders["ma_cua_hang"]
        + "|"
        + orders["ma_don"]
    )

    # Giữ tên khóa cũ để tương thích
    orders["store_order_key"] = orders["order_business_key"]

    # Kiểm tra trùng khóa đơn hàng
    if orders["order_business_key"].duplicated().any():
        raise ValueError("Duplicate order_business_key detected")
    # ---------------------------------------------------------
    # 3.1 CHUẨN HÓA ĐIỆN THOẠI VÀ TÊN
    # ---------------------------------------------------------

    orders["phone_norm"] = orders["so_dien_thoai"].map(
        normalize_phone
    )

    if "ten_khach" in orders.columns:
        orders["name_norm"] = orders["ten_khach"].map(
            normalize_name
        )
    else:
        orders["name_norm"] = ""

    # ---------------------------------------------------------
    # 3.2 BƯỚC 1: GHÉP BẰNG SĐT DUY NHẤT
    # ---------------------------------------------------------

    orders["customer_key"] = (
        orders["phone_norm"].map(phone_to_customer)
    )

    orders["customer_match_method"] = "UNKNOWN"

    matched_unique_phone = orders["customer_key"].notna()

    orders.loc[
        matched_unique_phone,
        "customer_match_method",
    ] = "PHONE_UNIQUE"

    # ---------------------------------------------------------
    # 3.3 BƯỚC 2: GHÉP BẰNG SĐT + TÊN
    # ---------------------------------------------------------

    unresolved = orders["customer_key"].isna()

    matched_by_pair = pd.Series(
        [
            phone_name_to_customer.get((phone, name))
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
        "customer_key",
    ] = matched_by_pair

    # Xác định nhóm ghép là duy nhất hay nghi trùng.
    pair_count_lookup = {
        (row["phone_norm"], row["name_norm"]):
        row["candidate_count"]
        for _, row in pair_groups.iterrows()
    }

    matched_pair_indices = orders.index[
        unresolved & orders["customer_key"].notna()
    ]

    for index in matched_pair_indices:
        phone = orders.at[index, "phone_norm"]
        name = orders.at[index, "name_norm"]

        candidate_count = pair_count_lookup.get(
            (phone, name),
            0,
        )

        if candidate_count > 1:
            orders.at[
                index, "customer_match_method"
            ] = "PHONE_NAME_DUPLICATE_CANDIDATE"
        else:
            orders.at[
                index, "customer_match_method"
            ] = "PHONE_NAME_UNIQUE"

    # ---------------------------------------------------------
    # 3.4 BƯỚC 3: GÁN UNKNOWN
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
        orders["order_date"].dt.strftime("%Y-%m")
    )

    # Chưa có dữ liệu trạng thái đơn hoàn tất.
    orders["order_status"] = "UNKNOWN"
    orders["segment_publishable"] = False

    # =========================================================
    # 5. FACT ĐƠN HÀNG
    # =========================================================

    fact_order = orders[
        [
            "order_business_key",
            "ma_don",
            "ma_cua_hang",
            "customer_key",
            "customer_match_method",
            "order_date",
            "analysis_month",
            "amount",
            "order_status",
            "segment_publishable",
        ]
    ].rename(
        columns={
            "ma_don": "order_id_source",
            "ma_cua_hang": "store_id",
        }
    )

    # Tương thích các bài test cũ.
    fact_order["customer_id"] = fact_order["customer_key"]

    # =========================================================
    # 6. DIMENSION KỲ PHÂN TÍCH
    # =========================================================

    months = sorted(
        fact_order["analysis_month"].dropna().unique()
    )

    dim_period = pd.DataFrame({
        "analysis_month": months
    })

    dim_period["period_key"] = (
        dim_period["analysis_month"]
        .str.replace("-", "", regex=False)
    )

    dim_period["cutoff_date"] = (
        pd.to_datetime(dim_period["analysis_month"] + "-01")
        + pd.offsets.MonthBegin(1)
    ).dt.strftime("%Y-%m-%d")

    dim_period["status"] = "READY"

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
            issue_records.append({
                "order_business_key": row["order_business_key"],
                "order_id_source": row["order_id_source"],
                "store_id": row["store_id"],
                "issue_code": "CUSTOMER_NOT_RESOLVED",
            })

        if pd.isna(row["order_date"]):
            issue_records.append({
                "order_business_key": row["order_business_key"],
                "order_id_source": row["order_id_source"],
                "store_id": row["store_id"],
                "issue_code": "INVALID_ORDER_DATE",
            })

        if pd.isna(row["amount"]):
            issue_records.append({
                "order_business_key": row["order_business_key"],
                "order_id_source": row["order_id_source"],
                "store_id": row["store_id"],
                "issue_code": "INVALID_ORDER_AMOUNT",
            })

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

    warehouse_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

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

    duplicate_candidates.to_csv(
        warehouse_dir / "customer_duplicate_candidates.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # =========================================================
    # 9. BÁO CÁO NẠP KHO
    # =========================================================

    unknown_count = fact_order["customer_key"].eq("UNKNOWN").sum()

    match_counts = (
        fact_order["customer_match_method"]
        .value_counts()
        .to_dict()
    )

    duplicate_candidate_match_count = match_counts.get(
        "PHONE_NAME_DUPLICATE_CANDIDATE",
        0,
    )

    report = [
        "# Báo cáo nạp kho dữ liệu",
        "",
        f"- Hồ sơ khách hàng (gồm UNKNOWN): {len(customer_dim):,}",
        f"- Đơn hàng đã nạp: {len(fact_order):,}",
        f"- Số vấn đề chất lượng dữ liệu: {len(issues):,}",
        f"- Đơn chưa xác định khách: {unknown_count:,}",
        f"- Đơn ghép bằng SĐT duy nhất: {match_counts.get('PHONE_UNIQUE', 0):,}",
        f"- Đơn ghép bằng SĐT + tên duy nhất: {match_counts.get('PHONE_NAME_UNIQUE', 0):,}",
        f"- Đơn ghép nhóm nghi trùng: {duplicate_candidate_match_count:,}",
        f"- Đơn chưa ghép: {match_counts.get('UNKNOWN', 0):,}",
        f"- Nhóm hồ sơ nghi trùng: {len(duplicate_candidates):,}",
        f"- Khóa đơn hàng trùng trong kho: {fact_order['order_business_key'].duplicated().sum()}",
        "- Trạng thái đơn hoàn tất: chưa có trong dữ liệu nguồn.",
        "- Công bố phân khúc: ĐANG CHẶN.",
        "- Cách nạp: ghi snapshot; chạy lại không cộng dồn.",
        "",
        "Lưu ý: nhóm hồ sơ nghi trùng được chọn record_id đại diện để ghép đơn.",
        "Đây chưa phải kết luận các hồ sơ là cùng một người.",
        "Khóa cửa hàng + mã đơn là khóa kỹ thuật tạm dùng theo dữ liệu hiện có.",
    ]

    (docs_dir / "bao-cao-nap-kho.md").write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print("NAP KHO DU LIEU HOAN TAT")
    print(f"So ho so dim_customer: {len(customer_dim):,}")
    print(f"So don fact_order: {len(fact_order):,}")
    print(f"So van de chat luong du lieu: {len(issues):,}")
    print(f"So nhom nghi trung: {len(duplicate_candidates):,}")
    print(f"So don UNKNOWN: {unknown_count:,}")
    print("Cong bo phan khuc: READY")
    print(f"Ket qua: {warehouse_dir}")


if __name__ == "__main__":
    load_warehouse()
