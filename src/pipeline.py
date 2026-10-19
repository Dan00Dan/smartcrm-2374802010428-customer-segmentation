
from src.extract.read_data import read_csv_data, print_data_profile
from src.transform.process_orders import process_orders
from src.quality.check_quality import check_quality
from src.load.save_results import save_results


def main():
    customers = read_csv_data("customers_raw.csv")
    orders = read_csv_data("orders_2024_2026.csv")

    print_data_profile(customers, "customers_raw.csv")
    print_data_profile(orders, "orders_2024_2026.csv")

    valid_df, reject_df, rows_before = process_orders()

    quality_result = check_quality(
        valid_df,
        reject_df,
        rows_before,
    )

    save_results(
        valid_df,
        reject_df,
        quality_result,
    )


if __name__ == "__main__":
    main()
