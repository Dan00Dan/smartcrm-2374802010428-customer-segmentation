import pandas as pd

from src.transform.segment_customers import assign_customer_segments


def make_customer(spending=0, orders=0, recent=0):
    return {
        "spending_12m": spending,
        "orders_12m": orders,
        "orders_90d": recent,
    }


def test_vip_by_spending_boundary():
    df = pd.DataFrame([make_customer(spending=30_000_000)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "VIP"


def test_vip_by_order_count():
    df = pd.DataFrame([make_customer(orders=8)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "VIP"


def test_regular_by_spending_boundary():
    df = pd.DataFrame([make_customer(spending=10_000_000)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "Thường xuyên"


def test_regular_by_order_count():
    df = pd.DataFrame([make_customer(orders=3)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "Thường xuyên"


def test_new_customer():
    df = pd.DataFrame([make_customer(recent=1)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "Mới"


def test_dormant_customer():
    df = pd.DataFrame([make_customer()])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "Ngủ đông"


def test_vip_has_priority_over_regular():
    df = pd.DataFrame([make_customer(spending=30_000_000, orders=3)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "VIP"


def test_regular_has_priority_over_new():
    df = pd.DataFrame([make_customer(orders=3, recent=1)])
    result = assign_customer_segments(df)
    assert result.loc[0, "customer_segment"] == "Thường xuyên"


def test_function_does_not_modify_original_dataframe():
    df = pd.DataFrame([make_customer(spending=30_000_000)])
    result = assign_customer_segments(df)
    assert "customer_segment" not in df.columns
    assert "customer_segment" in result.columns