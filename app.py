from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
WAREHOUSE = ROOT / "data" / "warehouse"


# =========================================================
# 1. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart CRM - Dashboard dữ liệu",
    page_icon="📊",
    layout="wide",
)

st.title("Smart CRM — Dashboard dữ liệu khách hàng")

st.caption(
    "Chuyên đề Tốt nghiệp 1 | Track DA | "
    "L1: Tính và gán phân khúc khách hàng"
)

st.success(
    "Smart CRM | Dashboard phân tích dữ liệu "
    "và phân khúc khách hàng QT-12"
)


# =========================================================
# 2. LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    files = {
        "fact": WAREHOUSE / "fact_order.csv",
        "customers": WAREHOUSE / "dim_customer.csv",
        "periods": WAREHOUSE / "dim_period.csv",
        "issues": WAREHOUSE / "data_quality_issues.csv",
    }

    missing = [
        str(path)
        for path in files.values()
        if not path.exists()
    ]

    if missing:
        raise FileNotFoundError(
            "Chưa có đủ dữ liệu kho. "
            "Hãy chạy lệnh "
            "`python -m src.etl.load_warehouse` trước."
        )

    fact = pd.read_csv(files["fact"])
    customers = pd.read_csv(files["customers"])
    periods = pd.read_csv(files["periods"])
    issues = pd.read_csv(files["issues"])

    required = {
        "customer_key",
        "order_date",
        "analysis_month",
        "amount",
    }

    missing_columns = required - set(fact.columns)

    if missing_columns:
        raise ValueError(
            "Thiếu cột trong fact_order.csv: "
            + ", ".join(sorted(missing_columns))
        )

    if "customer_key" not in customers.columns:
        raise ValueError(
            "Thiếu cột customer_key trong dim_customer.csv"
        )

    fact["order_date"] = pd.to_datetime(
        fact["order_date"],
        errors="coerce",
    )

    fact["amount"] = pd.to_numeric(
        fact["amount"],
        errors="coerce",
    )

    fact["analysis_month"] = (
        fact["analysis_month"]
        .fillna("Không rõ")
        .astype(str)
    )

    fact["customer_key"] = (
        fact["customer_key"]
        .fillna("UNKNOWN")
        .astype(str)
    )

    customers["customer_key"] = (
        customers["customer_key"]
        .fillna("UNKNOWN")
        .astype(str)
    )

    return fact, customers, periods, issues



# =========================================================
# 3. SVG CHART
# =========================================================

def render_svg_chart(
    labels,
    values,
    title,
    y_label,
    chart_type="bar",
    reference_value=None,
    reference_label="Mốc tham chiếu",
):

    labels = [str(x) for x in labels]

    values = [
        float(v) if pd.notna(v) else 0.0
        for v in values
    ]

    st.subheader(title)

    if not labels:
        st.info("Không có dữ liệu để vẽ biểu đồ.")
        return

    width, height = 850, 340

    left, right, top, bottom = 75, 25, 40, 85

    plot_w = width - left - right
    plot_h = height - top - bottom

    # Bao gồm cả mốc tham chiếu trong giới hạn trục Y
    max_value = max(
        max(values, default=0),
        float(reference_value or 0)
    ) or 1

    step = plot_w / len(values)

    bar_w = min(42, step * 0.6)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="100%" '
        f'role="img" aria-label="{escape(title)}">',

        '<rect width="100%" height="100%" fill="white"/>',

        f'<text x="{left}" y="22" font-size="13" fill="#333">'
        f'{escape(y_label)}</text>',
    ]

    # Trục và lưới
    for i in range(5):

        ratio = i / 4

        y = top + plot_h * ratio

        value = max_value * (1 - ratio)

        parts.append(
            f'<line x1="{left}" y1="{y:.1f}" '
            f'x2="{width-right}" y2="{y:.1f}" '
            f'stroke="#dddddd" stroke-width="1"/>'
        )

        parts.append(
            f'<text x="{left-8}" y="{y+4:.1f}" '
            f'text-anchor="end" font-size="10" fill="#555">'
            f'{value:,.0f}</text>'
        )

    points = []

    for i, (label, value) in enumerate(
        zip(labels, values)
    ):

        x = left + step * (i + 0.5)

        y = top + plot_h * (1 - value / max_value)

        if chart_type == "bar":

            bar_h = top + plot_h - y

            parts.append(
                f'<rect x="{x-bar_w/2:.1f}" y="{y:.1f}" '
                f'width="{bar_w:.1f}" height="{bar_h:.1f}" '
                f'rx="3" fill="#4C78A8"/>'
            )

        else:
            points.append((x, y))

        parts.append(
            f'<text x="{x:.1f}" y="{top+plot_h+20}" '
            f'text-anchor="middle" font-size="10" fill="#333">'
            f'{escape(label)}</text>'
        )

        if chart_type == "bar":

            label_y = max(top + 12, y - 6)

            parts.append(
                f'<text x="{x:.1f}" y="{label_y:.1f}" '
                f'text-anchor="middle" font-size="10" fill="#333">'
                f'{value:,.0f}</text>'
            )

    # Biểu đồ đường
    if chart_type == "line" and points:

        coords = " ".join(
            f"{x:.1f},{y:.1f}"
            for x, y in points
        )

        parts.append(
            f'<polyline points="{coords}" fill="none" '
            f'stroke="#E45756" stroke-width="2.5"/>'
        )

        for x, y in points:

            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" '
                f'r="4" fill="#E45756"/>'
            )

    # Mốc tham chiếu
    if reference_value is not None:

        reference_value = float(reference_value)

        reference_y = (
            top + plot_h *
            (1 - reference_value / max_value)
        )

        parts.append(
            f'<line x1="{left}" y1="{reference_y:.1f}" '
            f'x2="{width-right}" y2="{reference_y:.1f}" '
            f'stroke="#F59E0B" stroke-width="2" '
            f'stroke-dasharray="7,4"/>'
        )

        parts.append(
            f'<text x="{width-right-5}" '
            f'y="{max(top+12, reference_y-6):.1f}" '
            f'text-anchor="end" font-size="11" '
            f'font-weight="bold" fill="#B45309">'
            f'{escape(reference_label)}: '
            f'{reference_value:,.1f}</text>'
        )

    parts.append("</svg>")

    st.markdown(
        "".join(parts),
        unsafe_allow_html=True,
    )

# =========================================================
# 4. HTML TABLE
# =========================================================

def render_html_table(dataframe, max_rows=100):

    if dataframe.empty:
        st.info("Không có dữ liệu phù hợp với điều kiện lọc.")
        return

    display_df = dataframe.head(max_rows)

    html = [
        '<div style="overflow-x:auto;max-height:500px;">',

        '<table style="border-collapse:collapse;width:100%;'
        'font-size:13px;">',

        "<thead><tr>",
    ]

    for column in display_df.columns:

        html.append(
            '<th style="position:sticky;top:0;background:#263445;color:#ffffff;'
            'padding:9px;border:1px solid #d5dbe3;text-align:left;">'
            + escape(str(column))
            + "</th>"
        )

    html.append("</tr></thead><tbody>")

    for row in display_df.itertuples(
        index=False,
        name=None,
    ):

        html.append("<tr>")

        for value in row:

            if pd.isna(value):
                text_value = ""

            elif isinstance(value, float):
                text_value = f"{value:,.2f}"

            else:
                text_value = str(value)

            html.append(
                '<td style="padding:8px;border:1px solid #d5dbe3;'
                'overflow-wrap:anywhere;">'
                + escape(text_value)
                + "</td>"
            )

        html.append("</tr>")

    html.append("</tbody></table></div>")

    st.markdown(
        "".join(html),
        unsafe_allow_html=True,
    )

    if len(dataframe) > max_rows:

        st.caption(
            f"Đang hiển thị {max_rows} dòng đầu tiên "
            f"trên tổng số {len(dataframe):,} dòng."
        )


# =========================================================
# 5. REFRESH DATA
# =========================================================

if st.button("🔄 Làm mới dữ liệu"):

    st.cache_data.clear()

    st.rerun()


# =========================================================
# 6. LOAD WAREHOUSE
# =========================================================

try:
    with st.spinner("ĐANG TRUY VẤN: Tải dữ liệu kho Smart CRM..."):
        fact, customers, periods, issues = load_data()

    st.success("TRUY VẤN THÀNH CÔNG: Đã tải dữ liệu kho Smart CRM.")

except FileNotFoundError as e:
    st.error("LỖI KẾT NỐI DỮ LIỆU: Không tìm thấy file kho dữ liệu.")
    st.code(str(e))
    st.stop()

except Exception as e:
    st.error("LỖI TRUY VẤN DỮ LIỆU: Không thể tải kho dữ liệu.")
    st.code(str(e))
    st.stop()

if fact.empty:

    st.info("Kho dữ liệu hiện chưa có đơn hàng để hiển thị.")

    st.stop()


# =========================================================
# 7. FILTER MONTH
# =========================================================

months = sorted(
    fact["analysis_month"].dropna().unique().tolist()
)

st.subheader("Bộ lọc dữ liệu")

selected_months = st.multiselect(
    "Chọn tháng phân tích",
    options=months,
    default=months,
)

if not selected_months:
    st.warning("TRẠNG THÁI BỘ LỌC: RỖNG")

    st.info(
        "Chưa chọn tháng phân tích. "
        "Vui lòng chọn ít nhất một tháng để xem dữ liệu."
    )

    st.caption("Minh chứng D4: Dashboard xử lý trường hợp bộ lọc rỗng.")
    st.stop()


view = fact[
    fact["analysis_month"].isin(selected_months)
].copy()

if view.empty:
    st.warning("TRẠNG THÁI BỘ LỌC: KHÔNG CÓ KẾT QUẢ")

    st.info(
        "Các tháng đã chọn không có dữ liệu phù hợp. "
        "Vui lòng thay đổi bộ lọc."
    )

    st.caption("Minh chứng D4: Bộ lọc có lựa chọn nhưng không trả về dữ liệu.")
    st.stop()


# =========================================================
# 8. OVERVIEW
# =========================================================

total_orders = len(view)

unknown_orders = int(
    view["customer_key"].eq("UNKNOWN").sum()
)

known_orders = total_orders - unknown_orders

total_amount = view["amount"].sum(min_count=1)

st.subheader("Tổng quan dữ liệu")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Số dòng đơn hàng",
    f"{total_orders:,}",
)

c2.metric(
    "Đơn chưa xác định khách",
    f"{unknown_orders:,}",
)

c3.metric(
    "Đơn có khóa khách hàng",
    f"{known_orders:,}",
)

c4.metric(
    "Tổng tiền ghi nhận (VND)",
    "Chưa xác định"
    if pd.isna(total_amount)
    else f"{total_amount:,.0f}",
)

st.caption(
    "Lưu ý: Số dòng đơn hàng là số bản ghi trong kho, "
    "không khẳng định tất cả là đơn hoàn tất. "
    "Tổng tiền là số tiền ghi nhận, chưa được xác nhận "
    "là doanh thu hợp lệ."
)



# =========================================================
# 9. MONTHLY CHARTS
# =========================================================

st.divider()

st.subheader("Biểu đồ so sánh theo tháng")

monthly_orders = (
    view.groupby("analysis_month", as_index=False)
    .size()
    .rename(columns={"size": "Số đơn"})
    .sort_values("analysis_month")
)

monthly_amount = (
    view.groupby("analysis_month", as_index=False)["amount"]
    .sum(min_count=1)
    .rename(
        columns={
            "amount": "Tổng tiền ghi nhận (VND)"
        }
    )
    .sort_values("analysis_month")
)

# Mốc tham chiếu: trung bình các tháng đang được phân tích
order_reference = monthly_orders["Số đơn"].mean()

amount_reference = monthly_amount[
    "Tổng tiền ghi nhận (VND)"
].mean()

chart1, chart2 = st.columns(2)

with chart1:

    render_svg_chart(
        monthly_orders["analysis_month"].tolist(),
        monthly_orders["Số đơn"].tolist(),
        "Số đơn hàng theo tháng",
        "Số bản ghi",
        chart_type="bar",
        reference_value=order_reference,
        reference_label="TB/tháng",
    )

    st.caption(
        "Đơn vị: số bản ghi đơn hàng | "
        "Mốc tham chiếu: trung bình số đơn "
        "của các tháng được chọn | "
        "Nguồn: fact_order trong kho Smart CRM."
    )

with chart2:

    render_svg_chart(
        monthly_amount["analysis_month"].tolist(),
        monthly_amount[
            "Tổng tiền ghi nhận (VND)"
        ].tolist(),
        "Tổng tiền ghi nhận theo tháng",
        "VND",
        chart_type="line",
        reference_value=amount_reference,
        reference_label="TB/tháng",
    )

    st.caption(
        "Đơn vị: VND | "
        "Mốc tham chiếu: trung bình tổng tiền "
        "của các tháng được chọn | "
        "Nguồn: fact_order trong kho Smart CRM. "
        "Chỉ phản ánh thành tiền ghi nhận, "
        "không đồng nghĩa doanh thu đã xác minh."
    )


# =========================================================
# 10. ORDER TABLE
# =========================================================

st.divider()

st.subheader("Chi tiết đơn hàng")

preferred_columns = [
    "order_business_key",
    "order_id_source",
    "store_id",
    "customer_key",
    "order_date",
    "analysis_month",
    "amount",
    "order_status",
]

table_columns = [
    column
    for column in preferred_columns
    if column in view.columns
]

if not table_columns:

    table_columns = list(view.columns)

render_html_table(
    view[table_columns],
    max_rows=100,
)

csv_data = view[table_columns].to_csv(
    index=False,
    encoding="utf-8-sig",
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Tải dữ liệu đang lọc (CSV)",
    data=csv_data,
    file_name="smartcrm_orders_filtered.csv",
    mime="text/csv",
)


# =========================================================
# 11. CUSTOMER SEGMENTATION QT-12
# =========================================================

st.divider()

st.header("Phân khúc khách hàng QT-12")

st.caption(
    "Phân khúc được tính theo dữ liệu giao dịch ghi nhận "
    "trong kho và kỳ phân tích đã chọn."
)

# Xác định tháng phân tích hợp lệ
valid_selected_months = [
    month
    for month in selected_months
    if isinstance(month, str)
    and len(month) == 7
    and month[4] == "-"
    and pd.notna(
        pd.to_datetime(
            month,
            format="%Y-%m",
            errors="coerce",
        )
    )
]

if not valid_selected_months:

    st.warning(
        "Không có tháng hợp lệ để tính phân khúc khách hàng."
    )

else:

    # Ngày cuối tháng phân tích mới nhất
    latest_month = max(valid_selected_months)

    analysis_end = (
        pd.to_datetime(
            latest_month + "-01",
            format="%Y-%m-%d",
        )
        + pd.offsets.MonthEnd(0)
    )

    # Giao dịch có khách hàng xác định,
    # ngày và số tiền hợp lệ.
    valid_orders = fact[
        fact["customer_key"].ne("UNKNOWN")
        & fact["customer_key"].notna()
        & fact["order_date"].notna()
        & fact["amount"].notna()
        & (fact["amount"] >= 0)
    ].copy()

    # Không lấy giao dịch sau ngày phân tích
    valid_orders = valid_orders[
        valid_orders["order_date"] <= analysis_end
    ].copy()

    # -----------------------------------------------------
    # GIAO DỊCH 12 THÁNG
    # -----------------------------------------------------

    start_12m = (
        analysis_end
        - pd.DateOffset(months=12)
        + pd.Timedelta(days=1)
    )

    orders_12m = valid_orders[
        valid_orders["order_date"] >= start_12m
    ].copy()

    # -----------------------------------------------------
    # GIAO DỊCH 90 NGÀY
    # -----------------------------------------------------

    start_90d = (
        analysis_end
        - pd.Timedelta(days=89)
    )

    orders_90d = valid_orders[
        valid_orders["order_date"] >= start_90d
    ].copy()

    # -----------------------------------------------------
    # TÍNH CHỈ SỐ KHÁCH HÀNG
    # -----------------------------------------------------

    spending = (
        orders_12m.groupby("customer_key")["amount"]
        .sum()
    )

    order_counts = (
        orders_12m.groupby("customer_key")
        .size()
    )

    recent_counts = (
        orders_90d.groupby("customer_key")
        .size()
    )

    # -----------------------------------------------------
    # DANH SÁCH KHÁCH HÀNG
    # -----------------------------------------------------

    segment_df = customers.copy()

    segment_df["customer_key"] = (
        segment_df["customer_key"].astype(str)
    )

    # Không phân khúc UNKNOWN
    segment_df = segment_df[
        segment_df["customer_key"].ne("UNKNOWN")
    ].copy()

    segment_df = segment_df.drop_duplicates(
        subset=["customer_key"]
    )

    # Gắn các chỉ số giao dịch
    segment_df["spending_12m"] = (
        segment_df["customer_key"]
        .map(spending)
        .fillna(0)
    )

    segment_df["orders_12m"] = (
        segment_df["customer_key"]
        .map(order_counts)
        .fillna(0)
        .astype(int)
    )

    segment_df["orders_90d"] = (
        segment_df["customer_key"]
        .map(recent_counts)
        .fillna(0)
        .astype(int)
    )

    # -----------------------------------------------------
    # GÁN PHÂN KHÚC QT-12
    # VIP > THƯỜNG XUYÊN > MỚI > NGỦ ĐÔNG
    # -----------------------------------------------------

    segment_df["customer_segment"] = "Ngủ đông"

    # Khách mới: đúng 1 giao dịch trong 90 ngày
    segment_df.loc[
        segment_df["orders_90d"] == 1,
        "customer_segment",
    ] = "Mới"

    # Khách thường xuyên
    segment_df.loc[
        (
            segment_df["spending_12m"] >= 10_000_000
        )
        | (
            segment_df["orders_12m"] >= 3
        ),
        "customer_segment",
    ] = "Thường xuyên"

    # Khách VIP
    segment_df.loc[
        (
            segment_df["spending_12m"] >= 30_000_000
        )
        | (
            segment_df["orders_12m"] >= 8
        ),
        "customer_segment",
    ] = "VIP"

 
    # -----------------------------------------------------
    # THỐNG KÊ PHÂN KHÚC
    # -----------------------------------------------------

    segment_order = [
        "VIP",
        "Thường xuyên",
        "Mới",
        "Ngủ đông",
    ]

    segment_summary = (
        segment_df["customer_segment"]
        .value_counts()
        .reindex(
            segment_order,
            fill_value=0,
        )
    )

    # KPI
    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "VIP",
        f"{segment_summary['VIP']:,}",
    )

    s2.metric(
        "Thường xuyên",
        f"{segment_summary['Thường xuyên']:,}",
    )

    s3.metric(
        "Mới",
        f"{segment_summary['Mới']:,}",
    )

    s4.metric(
        "Ngủ đông",
        f"{segment_summary['Ngủ đông']:,}",
    )

    # -----------------------------------------------------
    # BIỂU ĐỒ PHÂN KHÚC
    # -----------------------------------------------------

    # Mốc tham chiếu: trung bình khách hàng trên 4 nhóm
    segment_reference = (
        segment_summary.sum() / len(segment_order)
        if segment_order
        else 0
    )

    render_svg_chart(
        segment_order,
        segment_summary.tolist(),
        "Số lượng khách hàng theo phân khúc",
        "Số khách hàng",
        chart_type="bar",
        reference_value=segment_reference,
        reference_label="TB/nhóm",
    )

    st.caption(
        "Mốc tham chiếu: trung bình số khách hàng "
        "trên 4 phân khúc; chỉ dùng để so sánh "
        "quy mô nhóm, không phải mục tiêu phân khúc."
    )

    # -----------------------------------------------------
    # BẢNG CHI TIẾT
    # -----------------------------------------------------

    st.subheader("Chi tiết phân khúc khách hàng")

    segment_columns = [
        "customer_key",
        "spending_12m",
        "orders_12m",
        "orders_90d",
        "customer_segment",
    ]

    segment_columns = [
        column
        for column in segment_columns
        if column in segment_df.columns
    ]

    render_html_table(
        segment_df[segment_columns],
        max_rows=100,
    )

    # -----------------------------------------------------
    # XUẤT CSV
    # -----------------------------------------------------

    segment_csv = segment_df.to_csv(
        index=False,
        encoding="utf-8-sig",
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Tải kết quả phân khúc khách hàng (CSV)",
        data=segment_csv,
        file_name="customer_segments.csv",
        mime="text/csv",
    )

    # -----------------------------------------------------
    # THÔNG TIN KỲ PHÂN TÍCH
    # -----------------------------------------------------

    st.caption(
        f"Kỳ phân tích đến ngày: "
        f"{analysis_end.strftime('%d/%m/%Y')} | "
        f"Tổng khách hàng được phân khúc: "
        f"{len(segment_df):,}"
    )

    st.warning(
        "Lưu ý: QT-12 hiện được tính trên giao dịch ghi nhận "
        "có khóa khách hàng xác định. Do chưa xác minh "
        "trạng thái đơn hoàn tất, kết quả phân khúc là "
        "kết quả phân tích sơ bộ, chưa phải phân khúc chính thức."
    )



# =========================================================
# 12. DATA QUALITY
# =========================================================

st.divider()

st.subheader("Kiểm tra chất lượng dữ liệu")

q1, q2, q3 = st.columns(3)

q1.metric(
    "Hồ sơ khách hàng",
    f"{len(customers):,}",
)

q2.metric(
    "Kỳ phân tích",
    f"{len(periods):,}",
)

q3.metric(
    "Bản ghi cảnh báo",
    f"{len(issues):,}",
)

# Kiểm tra khách hàng UNKNOWN
if "customer_key" in view.columns:

    unresolved = view[
        view["customer_key"].eq("UNKNOWN")
    ]

    if not unresolved.empty:

        st.warning(
            f"Có {len(unresolved):,} bản ghi chưa xác định được "
            "khách hàng. Không tự động gán các bản ghi này "
            "cho một khách hàng cụ thể."
        )

# Kiểm tra trạng thái đơn hàng
if "order_status" in view.columns:

    statuses = (
        view["order_status"]
        .fillna("UNKNOWN")
        .astype(str)
        .value_counts()
    )

    if statuses.index.isin(["UNKNOWN"]).any():

        st.warning(
            "Dữ liệu chưa xác minh trạng thái đơn hàng hoàn tất. "
            "Kết quả phân khúc hiện phản ánh giao dịch ghi nhận, "
            "chưa thể khẳng định hoàn toàn theo đơn hàng đã hoàn tất."
        )


# =========================================================
# 13. FOOTER
# =========================================================

st.caption(
    "Smart CRM | Dashboard phân tích dữ liệu, "
    "tích hợp ETL và tính phân khúc khách hàng QT-12. "
    "Kết quả cần được đối chiếu với chất lượng nguồn dữ liệu."
)