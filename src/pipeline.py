
from pathlib import Path

import pandas as pd

from src.etl.load_warehouse import load_warehouse
from src.extract.read_data import read_csv_data, print_data_profile
from src.transform.process_orders import process_orders
from src.quality.check_quality import check_quality
from src.load.save_results import save_results


# Xác định thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    """
    Thực hiện quy trình ETL:
    1. Đọc dữ liệu nguồn.
    2. Chuẩn hóa và phân loại đơn hàng.
    3. Kiểm tra chất lượng dữ liệu (D3).
    4. Nạp Data Warehouse và giả danh thông tin (D4).
    5. Lưu kết quả và báo cáo.
    """

    # =====================================================
    # 1. ĐỌC DỮ LIỆU NGUỒN
    # =====================================================

    customers = read_csv_data("customers_raw.csv")

    orders = read_csv_data(
        "orders_2024_2026.csv",
        dtype=str,
        keep_default_na=False,
    )

    # Hiển thị thông tin tổng quan dữ liệu
    print_data_profile(customers, "customers_raw.csv")
    print_data_profile(orders, "orders_2024_2026.csv")

    # =====================================================
    # 2. CHUẨN HÓA VÀ PHÂN LOẠI ĐƠN HÀNG
    # =====================================================

    # Sử dụng lại DataFrame đã đọc ở bước 1,
    # tránh đọc file CSV lần thứ hai.
    valid_df, reject_df, rows_before = process_orders(orders)

    # =====================================================
    # 3. KIỂM TRA CHẤT LƯỢNG DỮ LIỆU - D3
    # =====================================================

    quality_result = check_quality(
        valid_df,
        reject_df,
        rows_before,
    )

    # =====================================================
    # 4. NẠP WAREHOUSE VÀ GIẢ DANH THÔNG TIN - D4
    # =====================================================

    # Kết hợp dữ liệu hợp lệ và dữ liệu bị từ chối trong bộ nhớ.
    # Không cần xuất thông tin cá nhân ra CSV trung gian.
    warehouse_orders = pd.concat(
        [valid_df, reject_df],
        ignore_index=True,
    )

    load_warehouse(
        root=PROJECT_ROOT,
        orders_df=warehouse_orders,
    )

    # =====================================================
    # 5. LƯU DỮ LIỆU VÀ BÁO CÁO
    # =====================================================

    save_results(
        valid_df,
        reject_df,
        quality_result,
    )

    # =====================================================
    # 6. THÔNG BÁO HOÀN TẤT
    # =====================================================

    print("\n======================================")
    print("PIPELINE ETL HOAN TAT")
    print("Da kiem tra chat luong du lieu (D3)")
    print("Da nap Warehouse va gia danh (D4)")
    print("======================================")


if __name__ == "__main__":
    main()
