
from pathlib import Path
from html import escape
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
WAREHOUSE = ROOT / "data" / "warehouse"

st.set_page_config(
    page_title="Smart CRM - Dashboard dữ liệu",
    page_icon="📊",
    layout="wide",
)

st.title("Smart CRM — Dashboard dữ liệu khách hàng")
st.caption("Chuyên đề Tốt nghiệp 1 | Track DA | L1: Tính và gán phân khúc khách hàng")

st.warning(
    "CHƯA ĐƯỢC CÔNG BỐ PHÂN KHÚC: "
    "Nguồn dữ liệu chưa xác minh đầy đủ khách hàng và trạng thái đơn hoàn tất. "
    "Các thống kê bên dưới chỉ phản ánh dữ liệu ghi nhận trong kho, "
    "không phải kết quả phân khúc chính thức."
)


@st.cache_data
def load_data():
    files = {
        "fact": WAREHOUSE / "fact_order.csv",
        "customers": WAREHOUSE / "dim_customer.csv",
        "periods": WAREHOUSE / "dim_period.csv",
        "issues": WAREHOUSE / "data_quality_issues.csv",
    }

    missing = [str(path) for path in files.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Chưa có đủ dữ liệu kho. Hãy chạy lệnh "
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

    fact["order_date"] = pd.to_datetime(
        fact["order_date"], errors="coerce"
    )
    fact["amount"] = pd.to_numeric(
        fact["amount"], errors="coerce"
    )
    fact["analysis_month"] = (
        fact["analysis_month"].fillna("Không rõ").astype(str)
    )
    fact["customer_key"] = (
        fact["customer_key"].fillna("UNKNOWN").astype(str)
    )

    return fact, customers, periods, issues


def render_svg_chart(labels, values, title, y_label, chart_type="bar"):
    """Ve bieu do SVG, khong su dung pyarrow hay matplotlib."""

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
    max_value = max(values, default=0) or 1
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

    # Truc va cac vach luoi
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

    for i, (label, value) in enumerate(zip(labels, values)):
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

    if chart_type == "line" and points:
        coords = " ".join(
            f"{x:.1f},{y:.1f}" for x, y in points
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

    parts.append("</svg>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_html_table(dataframe, max_rows=100):
    """Hien thi bang HTML, khong dung st.dataframe."""

    if dataframe.empty:
        st.info("Không có dữ liệu phù hợp với điều kiện lọc.")
        return

    display_df = dataframe.head(max_rows)
    columns = list(display_df.columns)

    html = [
        '<div style="overflow-x:auto;max-height:500px;">',
        '<table style="border-collapse:collapse;width:100%;'
        'font-size:13px;">',
        "<thead><tr>",
    ]

    for column in columns:
        html.append(
            '<th style="position:sticky;top:0;background:#eaf0f6;'
            'padding:9px;border:1px solid #d5dbe3;text-align:left;">'
            + escape(str(column))
            + "</th>"
        )

    html.append("</tr></thead><tbody>")

    for row in display_df.itertuples(index=False, name=None):
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
    st.markdown("".join(html), unsafe_allow_html=True)

    if len(dataframe) > max_rows:
        st.caption(
            f"Đang hiển thị {max_rows} dòng đầu tiên "
            f"trên tổng số {len(dataframe):,} dòng."
        )


# Nut nap lai du lieu sau khi ETL chay lai
if st.button("🔄 Làm mới dữ liệu"):
    st.cache_data.clear()
    st.rerun()

try:
    fact, customers, periods, issues = load_data()
except FileNotFoundError as exc:
    st.error(str(exc))
    st.info(
        "Sau khi tạo kho dữ liệu thành công, hãy bấm "
        "'Làm mới dữ liệu' hoặc chạy lại ứng dụng."
    )
    st.stop()
except Exception as exc:
    st.error(f"Không thể tải dữ liệu: {exc}")
    st.stop()

if fact.empty:
    st.info("Kho dữ liệu hiện chưa có đơn hàng để hiển thị.")
    st.stop()

# Bo loc thang
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
    st.info("Em hãy chọn ít nhất một tháng để xem báo cáo.")
    st.stop()

view = fact[
    fact["analysis_month"].isin(selected_months)
].copy()

if view.empty:
    st.info("Không có đơn hàng trong khoảng tháng đã chọn.")
    st.stop()

# Chi so tong quan
total_orders = len(view)
unknown_orders = int(
    view["customer_key"].eq("UNKNOWN").sum()
)
known_orders = total_orders - unknown_orders
total_amount = view["amount"].sum(min_count=1)

st.subheader("Tổng quan dữ liệu")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Số dòng đơn hàng", f"{total_orders:,}")
c2.metric("Đơn chưa xác định khách", f"{unknown_orders:,}")
c3.metric("Đơn có khóa khách hàng", f"{known_orders:,}")
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

# Du lieu so sanh theo thang
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
    .rename(columns={"amount": "Tổng tiền ghi nhận (VND)"})
    .sort_values("analysis_month")
)

chart1, chart2 = st.columns(2)

with chart1:
    render_svg_chart(
        monthly_orders["analysis_month"].tolist(),
        monthly_orders["Số đơn"].tolist(),
        "Số đơn hàng theo tháng",
        "Số bản ghi",
        chart_type="bar",
    )

with chart2:
    render_svg_chart(
        monthly_amount["analysis_month"].tolist(),
        monthly_amount["Tổng tiền ghi nhận (VND)"].tolist(),
        "Tổng tiền ghi nhận theo tháng",
        "VND",
        chart_type="line",
    )

# Bang don hang
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
    column for column in preferred_columns
    if column in view.columns
]

if not table_columns:
    table_columns = list(view.columns)

render_html_table(view[table_columns], max_rows=100)

# Tai CSV
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

# Kiem tra chat luong du lieu
st.divider()
st.subheader("Kiểm tra chất lượng dữ liệu")

q1, q2, q3 = st.columns(3)
q1.metric("Hồ sơ khách hàng", f"{len(customers):,}")
q2.metric("Kỳ phân tích", f"{len(periods):,}")
q3.metric("Bản ghi cảnh báo", f"{len(issues):,}")

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
            "Không dùng các thống kê này để công bố phân khúc."
        )

st.caption(
    "Smart CRM | Dashboard phục vụ kiểm tra dữ liệu và tích hợp ETL. "
    "Kết quả phân khúc chỉ được công bố sau khi xác minh "
    "khóa liên kết khách hàng và trạng thái đơn hàng."
)
