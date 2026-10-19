
from extract.read_data import read_csv_data, print_data_profile
from transform.process_orders import process_orders


def main():
    customers = read_csv_data("customers_raw.csv")
    orders = read_csv_data("orders_2024_2026.csv")

    print_data_profile(customers, "customers_raw.csv")
    print_data_profile(orders, "orders_2024_2026.csv")

    process_orders()


if __name__ == "__main__":
    main()
