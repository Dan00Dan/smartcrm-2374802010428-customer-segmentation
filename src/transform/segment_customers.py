import pandas as pd


def assign_customer_segments(segment_df):
    """
    Gán phân khúc khách hàng theo QT-12.
    Ưu tiên: VIP > Thường xuyên > Mới > Ngủ đông.
    """
    result = segment_df.copy()

    result["customer_segment"] = "Ngủ đông"

    # Khách mới: đúng 1 đơn trong 90 ngày
    result.loc[
        result["orders_90d"] == 1,
        "customer_segment",
    ] = "Mới"

    # Khách thường xuyên
    result.loc[
        (
            result["spending_12m"] >= 10_000_000
        )
        | (
            result["orders_12m"] >= 3
        ),
        "customer_segment",
    ] = "Thường xuyên"

    # Khách VIP
    result.loc[
        (
            result["spending_12m"] >= 30_000_000
        )
        | (
            result["orders_12m"] >= 8
        ),
        "customer_segment",
    ] = "VIP"

    return result