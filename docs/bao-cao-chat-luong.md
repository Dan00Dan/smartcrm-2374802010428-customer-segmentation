# Báo cáo chất lượng dữ liệu đơn hàng

## 1. Tổng quan

- Số dòng đầu vào: 26,000
- Số dòng hợp lệ: 25,607
- Số dòng bị từ chối: 393
- Tổng dòng sau phân loại: 26,000

## 2. Kết quả kiểm tra

- Bảo toàn số dòng: True
- Dòng từ chối có lý do: True

## 3. Đánh giá chất lượng theo từng cột

| Cột dữ liệu | Tổng dòng | Không thiếu | Thiếu | Completeness | Validity | Consistency |
|---|---:|---:|---:|---:|---:|---:|
| order_id | 26000 | 26000 | 0 | 100.00% | nan% | nan% |
| ma_don | 26000 | 26000 | 0 | 100.00% | nan% | nan% |
| ma_cua_hang | 26000 | 26000 | 0 | 100.00% | nan% | nan% |
| ngay | 26000 | 25886 | 114 | 99.56% | 100.00% | 98.92% |
| ten_khach | 26000 | 26000 | 0 | 100.00% | nan% | nan% |
| so_dien_thoai | 26000 | 24512 | 1488 | 94.28% | nan% | nan% |
| thanh_tien | 26000 | 25721 | 279 | 98.93% | 100.00% | 99.56% |
| nhan_vien | 26000 | 24989 | 1011 | 96.11% | nan% | nan% |
| ghi_chu | 26000 | 13039 | 12961 | 50.15% | nan% | nan% |

**Giải thích các chỉ số:**

- **Completeness:** Tỷ lệ dữ liệu không bị thiếu trên tổng số dòng.
- **Validity:** Tỷ lệ giá trị đáp ứng quy tắc hợp lệ trên số giá trị không thiếu.
- **Consistency:** Tỷ lệ giá trị đúng định dạng chuẩn trên số giá trị không thiếu.
- **N/A:** Chưa thiết lập quy tắc Validity hoặc Consistency cho cột đó.

## 4. Bảo vệ dữ liệu cá nhân

- Các file CSV đầu ra đã loại bỏ những cột định danh trực tiếp.
- Thông tin khách hàng được sử dụng trong bộ nhớ để đối chiếu.
- Warehouse sử dụng mã khách hàng giả danh HMAC-SHA256.
- Không xuất tên, số điện thoại, email và địa chỉ vào các bảng Warehouse.

## 5. File đầu ra

- Dữ liệu hợp lệ: `data/processed/orders_normalized.csv`
- Dữ liệu bị từ chối: `data/processed/orders_reject.csv`
- Báo cáo chất lượng CSV: `docs/data-quality-by-column.csv`
- Báo cáo tổng hợp: `docs/bao-cao-chat-luong.md`
