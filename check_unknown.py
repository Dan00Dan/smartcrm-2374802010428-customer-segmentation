
from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parent

customers_file = ROOT / "data/raw/customers_raw.csv"
orders_file = ROOT / "data/processed/orders_normalized.csv"
fact_file = ROOT / "data/warehouse/fact_order.csv"


def normalize_phone(value):
    if pd.isna(value):
        return ""

    phone = re.sub(r"\D", "", str(value))

    if phone.startswith("0084"):
        phone = "0" + phone[4:]
    elif phone.startswith("84") and len(phone) == 11:
        phone = "0" + phone[2:]

    return phone


customers = pd.read_csv(customers_file, dtype=str)
orders = pd.read_csv(orders_file, dtype=str)
fact = pd.read_csv(fact_file, dtype=str)

customers["phone_norm"] = customers["so_dien_thoai"].map(
    normalize_phone
)
orders["phone_norm"] = orders["so_dien_thoai"].map(
    normalize_phone
)

phone_counts = (
    customers[customers["phone_norm"] != ""]
    .groupby("phone_norm")["record_id"]
    .nunique()
)

unique_phones = set(phone_counts[phone_counts == 1].index)
customer_phones = set(customers["phone_norm"])

orders["phone_type"] = "Số điện thoại khớp duy nhất"

orders.loc[
    orders["phone_norm"] == "",
    "phone_type"
] = "Thiếu số điện thoại"

orders.loc[
    (orders["phone_norm"] != "")
    & (~orders["phone_norm"].isin(customer_phones)),
    "phone_type"
] = "Không có trong hồ sơ khách hàng"

orders.loc[
    (orders["phone_norm"] != "")
    & (orders["phone_norm"].isin(customer_phones))
    & (~orders["phone_norm"].isin(unique_phones)),
    "phone_type"
] = "Số điện thoại trùng hồ sơ"

print("\n===== THỐNG KÊ SỐ ĐIỆN THOẠI ĐƠN HÀNG =====")
print(orders["phone_type"].value_counts())

print("\n===== KIỂM TRA UNKNOWN TRONG FACT =====")
unknown = fact[fact["customer_key"] == "UNKNOWN"]

print("Tổng UNKNOWN:", len(unknown))

unknown_keys = set(unknown["order_business_key"])


order_keys = (
    orders["ma_cua_hang"].astype(str).str.strip()
    + "|"
    + orders["ma_don"].astype(str).str.strip()
)

unknown_orders = orders[order_keys.isin(unknown_keys)].copy()


# Gắn khóa đơn hàng để đối chiếu với fact_order
unknown_orders["order_business_key"] = order_keys.loc[
    unknown_orders.index
]

# Thống kê nguyên nhân riêng trong nhóm UNKNOWN
unknown_detail = unknown.merge(
    unknown_orders[
        ["order_business_key", "phone_norm", "phone_type"]
    ],
    on="order_business_key",
    how="left",
)

print("\n===== NGUYÊN NHÂN RIÊNG CỦA UNKNOWN =====")
print(unknown_detail["phone_type"].value_counts(dropna=False))

print("\n===== UNKNOWN CÓ SỐ ĐIỆN THOẠI KHỚP =====")
print(
    unknown_detail[
        unknown_detail["phone_type"]
        == "Số điện thoại khớp duy nhất"
    ].shape[0]
)

unknown_detail.to_csv(
    ROOT / "unknown_analysis.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã xuất: unknown_analysis.csv")



# Xuất dữ liệu kiểm tra để xem chi tiết
unknown.to_csv(
    ROOT / "unknown_records.csv",
    index=False,
    encoding="utf-8-sig"
)

orders.to_csv(
    ROOT / "phone_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nĐã xuất:")
print("- unknown_records.csv")
print("- phone_analysis.csv")


# Kiểm tra các hồ sơ khách hàng có số điện thoại trùng
duplicate_phones = customers[
    customers["phone_norm"].isin(
        phone_counts[phone_counts > 1].index
    )
].sort_values("phone_norm")

duplicate_phones.to_csv(
    ROOT / "duplicate_customer_phones.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\n===== KIỂM TRA HỒ SƠ TRÙNG SỐ ĐIỆN THOẠI =====")
print("Số hồ sơ có điện thoại trùng:", len(duplicate_phones))
print("Số điện thoại bị trùng:", duplicate_phones["phone_norm"].nunique())
print("Đã xuất: duplicate_customer_phones.csv")

# Phân loại số điện thoại trùng theo tên khách hàng
duplicate_summary = (
    duplicate_phones.groupby("phone_norm")
    .agg(
        so_ho_so=("record_id", "nunique"),
        so_ten_khac_nhau=("ho_ten", "nunique"),
    )
    .reset_index()
)

duplicate_summary["nhom"] = duplicate_summary[
    "so_ten_khac_nhau"
].apply(
    lambda x: "Cùng tên" if x == 1 else "Khác tên"
)

print("\n===== PHÂN LOẠI SỐ ĐIỆN THOẠI TRÙNG =====")
print(duplicate_summary["nhom"].value_counts())

print("\n===== THỐNG KÊ SỐ HỒ SƠ THEO NHÓM =====")
print(
    duplicate_summary.groupby("nhom")["so_ho_so"]
    .agg(["count", "sum", "mean"])
)

duplicate_summary.to_csv(
    ROOT / "duplicate_phone_summary.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã xuất: duplicate_phone_summary.csv")

# Đối chiếu UNKNOWN với hồ sơ khách hàng có cùng số điện thoại
customer_candidates = (
    customers[customers["phone_norm"] != ""]
    .groupby("phone_norm")
    .agg(
        candidate_record_ids=("record_id", lambda x: " | ".join(x)),
        candidate_names=("ho_ten", lambda x: " | ".join(x)),
        candidate_count=("record_id", "nunique"),
    )
    .reset_index()
)

unknown_candidates = unknown_detail.merge(
    customer_candidates,
    on="phone_norm",
    how="left",
)

unknown_candidates.to_csv(
    ROOT / "unknown_phone_candidates.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\n===== KẾT QUẢ ĐỐI CHIẾU UNKNOWN =====")
print("Số UNKNOWN có hồ sơ ứng viên:",
      unknown_candidates["candidate_count"].notna().sum())
print("Số UNKNOWN không có hồ sơ ứng viên:",
      unknown_candidates["candidate_count"].isna().sum())

print("Đã xuất: unknown_phone_candidates.csv")

import unicodedata

def normalize_name(value):
    if pd.isna(value):
        return ""

    text = str(value).strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"[^a-z0-9]", "", text)


# Chuẩn hóa tên khách hàng ở hai nguồn
customers["name_norm"] = customers["ho_ten"].map(normalize_name)
orders["name_norm"] = orders["ten_khach"].map(normalize_name)

# Tạo danh sách ứng viên theo số điện thoại + tên
customer_candidates = customers[
    customers["phone_norm"] != ""
].copy()

customer_candidates["candidate_key"] = (
    customer_candidates["phone_norm"]
    + "|"
    + customer_candidates["name_norm"]
)

candidate_counts = (
    customer_candidates.groupby("candidate_key")["record_id"]
    .nunique()
)

orders["candidate_key"] = (
    orders["phone_norm"] + "|" + orders["name_norm"]
)

orders["name_match_count"] = (
    orders["candidate_key"].map(candidate_counts).fillna(0)
)

# Chỉ kiểm tra trong nhóm UNKNOWN
unknown_order_keys = set(unknown["order_business_key"])

orders["order_business_key"] = (
    orders["ma_cua_hang"].astype(str).str.strip()
    + "|"
    + orders["ma_don"].astype(str).str.strip()
)

unknown_name_check = orders[
    orders["order_business_key"].isin(unknown_order_keys)
].copy()

print("\n===== KIỂM TRA GHÉP THEO SỐ ĐIỆN THOẠI + TÊN =====")
print(
    unknown_name_check["name_match_count"]
    .value_counts()
    .sort_index()
)

unknown_name_check.to_csv(
    ROOT / "unknown_name_check.csv",
    index=False,
    encoding="utf-8-sig",
)

print("Đã xuất: unknown_name_check.csv")
