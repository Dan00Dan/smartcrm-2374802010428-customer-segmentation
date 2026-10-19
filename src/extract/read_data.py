
from pathlib import Path

import pandas as pd


# Xác định thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def read_csv_data(filename: str) -> pd.DataFrame:
    """Đọc một file CSV từ thư mục data/raw."""
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {file_path}")

    return pd.read_csv(file_path, low_memory=False)


def print_data_profile(df: pd.DataFrame, filename: str) -> None:
    """In số dòng, số cột và tỷ lệ dữ liệu trống."""
    print(f"\n===== {filename} =====")
    print(f"Số dòng: {len(df):,}")
    print(f"Số cột: {len(df.columns)}")
    print("\nTỷ lệ ô trống theo cột (%):")
    print((df.isna().mean() * 100).round(2).to_string())
