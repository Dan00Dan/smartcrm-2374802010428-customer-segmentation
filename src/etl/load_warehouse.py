from pathlib import Path
import re
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CUSTOMERS_FILE = ROOT / "data" / "raw" / "customers_raw.csv"
ORDERS_FILE = ROOT / "data" / "processed" / "orders_normalized.csv"
WAREHOUSE_DIR = ROOT / "data" / "warehouse"


def normalize_phone(value):
    """Chuẩn hóa số điện thoại về chữ số; không tự đổi mã quốc gia."""
    if pd.isna(value):
        return ""
    return re.sub(r"\D", "", str(value))


def load_warehouse():
    """
    Nạp dữ liệu theo khóa nghiệp vụ.
    Số điện thoại chỉ dùng để ghép khi khớp duy nhất một hồ sơ.
    Đơn chưa xác định khách được gán UNKNOWN, không tự ghép theo tên.
    Kết quả phân khúc chưa được công bố vì chưa có trạng thái đơn hàng.
    """
    customers = pd.read_csv(CUSTOMERS_FILE, dtype=str)
    orders = pd.read_csv(ORDERS_FILE)

    required_customer = {"record_id", "ho_ten", "so_dien_thoai"}
    required_order = {
        "ma_don", "ma_cua_hang", "ngay",
        "so_dien_thoai", "thanh_tien"
    }

    if not required_customer.issubset(customers.columns):
        raise ValueError("customers_raw.csv thiếu cột bắt buộc.")
    if not required_order.issubset(orders.columns):
        raise ValueError("orders_normalized.csv thiếu cột bắt buộc.")

    # Dimension khách hàng: record_id là mã hồ sơ nguồn.
    customers["phone_norm"] = customers["so_dien_thoai"].map(normalize_phone)
    customer_dim = customers[
        ["record_id", "ho_ten"]
    ].rename(columns={
        "record_id": "customer_key",
        "ho_ten": "full_name",
    })
    customer_dim.insert(0, "customer_key", customer_dim.pop("customer_key"))
    customer_dim = customer_dim.drop_duplicates(subset=["customer_key"])

    # Chỉ dùng số điện thoại xuất hiện đúng một lần trong hồ sơ khách hàng.
    phone_counts = (
        customers.loc[customers["phone_norm"].ne("")]
        .groupby("phone_norm")["record_id"]
        .nunique()
    )
    unique_phones = set(phone_counts[phone_counts == 1].index)
    phone_to_customer = (
        customers.loc[customers["phone_norm"].isin(unique_phones)]
        .drop_duplicates("phone_norm")
        .set_index("phone_norm")["record_id"]
        .to_dict()
    )

    unknown_row = pd.DataFrame([{
        "customer_key": "UNKNOWN",
        "full_name": "Không xác định",
    }])
    customer_dim = pd.concat(
        [unknown_row, customer_dim], ignore_index=True
    )

    # Khóa nghiệp vụ hiện dùng tổ hợp mã cửa hàng + mã đơn.
    # Không dùng riêng ma_don vì mã này bị lặp giữa các cửa hàng.
    orders["store_order_key"] = (
        orders["ma_cua_hang"].fillna("").astype(str).str.strip()
        + "|"
        + orders["ma_don"].fillna("").astype(str).str.strip()
    )

    if orders["store_order_key"].eq("|").any():
        raise ValueError("Có đơn hàng thiếu mã cửa hàng hoặc mã đơn.")
    if orders["store_order_key"].duplicated().any():
        raise ValueError(
            "Khóa cửa hàng + mã đơn bị trùng; dừng nạp để rà soát."
        )

    orders["phone_norm"] = orders["so_dien_thoai"].map(normalize_phone)
    orders["customer_key"] = orders["phone_norm"].map(phone_to_customer)
    orders["customer_key"] = orders["customer_key"].fillna("UNKNOWN")

    orders["ngay"] = pd.to_datetime(orders["ngay"], errors="coerce")
    orders["analysis_month"] = orders["ngay"].dt.strftime("%Y-%m")

    # Chưa có cột trạng thái đơn hoàn tất: không giả định mọi đơn đều hợp lệ.
    orders["order_status"] = "UNKNOWN"
    orders["segment_publishable"] = False

    fact_order = orders[[
        "store_order_key", "ma_don", "ma_cua_hang",
        "customer_key", "ngay", "analysis_month",
        "thanh_tien", "order_status", "segment_publishable",
    ]].rename(columns={
        "store_order_key": "order_business_key",
        "ma_don": "order_id_source",
        "ma_cua_hang": "store_id",
        "ngay": "order_date",
        "thanh_tien": "amount",
    })

    # Dimension kỳ: kỳ phân tích và ngày chốt là ngày đầu tháng kế tiếp.
    months = sorted(fact_order["analysis_month"].dropna().unique())
    dim_period = pd.DataFrame({"analysis_month": months})
    dim_period["period_key"] = dim_period["analysis_month"].str.replace("-", "")
    dim_period["cutoff_date"] = (
        pd.to_datetime(dim_period["analysis_month"] + "-01")
        + pd.offsets.MonthBegin(1)
    ).dt.strftime("%Y-%m-%d")
    dim_period["status"] = "BLOCKED_SOURCE_VALIDATION"
    dim_period = dim_period[
        ["period_key", "analysis_month", "cutoff_date", "status"]
    ]

    # Bảng lỗi để truy vết đơn chưa ghép được hồ sơ.
    issues = fact_order.loc[
        fact_order["customer_key"].eq("UNKNOWN"),
        ["order_business_key", "order_id_source", "store_id"]
    ].copy()
    issues["issue_code"] = "CUSTOMER_NOT_RESOLVED"

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    # Ghi lại snapshot để chạy nhiều lần không tạo bản ghi trùng.
    customer_dim.to_csv(
        WAREHOUSE_DIR / "dim_customer.csv",
        index=False, encoding="utf-8-sig"
    )
    dim_period.to_csv(
        WAREHOUSE_DIR / "dim_period.csv",
        index=False, encoding="utf-8-sig"
    )
    fact_order.to_csv(
        WAREHOUSE_DIR / "fact_order.csv",
        index=False, encoding="utf-8-sig"
    )
    issues.to_csv(
        WAREHOUSE_DIR / "data_quality_issues.csv",
        index=False, encoding="utf-8-sig"
    )

    report = [
        "# Báo cáo nạp kho dữ liệu",
        "",
        f"- Hồ sơ khách hàng (gồm UNKNOWN): {len(customer_dim):,}",
        f"- Đơn hàng đã nạp: {len(fact_order):,}",
        f"- Đơn chưa xác định được khách: {len(issues):,}",
        f"- Khóa đơn hàng trùng: {fact_order['order_business_key'].duplicated().sum()}",
        "- Trạng thái đơn hoàn tất: chưa có trong dữ liệu nguồn.",
        "- Công bố phân khúc: ĐANG CHẶN cho đến khi xác minh dữ liệu nguồn.",
        "- Cách nạp: ghi lại snapshot; chạy lại không cộng dồn bản ghi.",
        "",
        "Lưu ý: khóa cửa hàng + mã đơn là khóa kỹ thuật tạm dùng theo dữ liệu hiện có, cần được xác nhận về mặt nghiệp vụ.",
    ]
    (ROOT / "docs" / "bao-cao-nap-kho.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    print("NAP KHO DU LIEU HOAN TAT")
    print(f"So ho so dim_customer: {len(customer_dim):,}")
    print(f"So don fact_order: {len(fact_order):,}")
    print(f"So don chua xac dinh khach: {len(issues):,}")
    print("Cong bo phan khuc: BLOCKED_SOURCE_VALIDATION")
    print(f"Ket qua: {WAREHOUSE_DIR}")


if __name__ == "__main__":
    load_warehouse()
