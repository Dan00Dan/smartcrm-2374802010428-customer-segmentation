# Đặc tả yêu cầu dữ liệu – Track DA – L1

Trần Thị Như Quỳnh | MSSV: 2374802010428

Mục tiêu: dùng dữ liệu mua hàng để chia khách thành VIP, Thường xuyên, Mới và Ngủ đông theo QT-12.

## 1. Nguồn dữ liệu

| File mẫu | Số dòng đã đọc | Định dạng |
|---|---:|---|
| customers_raw.csv | 67.037 | CSV |
| orders_2024_2026.csv | 26.000 | CSV |
| order_item | Chưa có file mẫu | — |

## 2. Cột thật và tỷ lệ thiếu

Tính ô rỗng hoặc chỉ có khoảng trắng trên tổng số dòng của từng file.

| File | Cột trong CSV | Số ô thiếu | Tỷ lệ thiếu |
|---|---|---:|---:|
| customers_raw.csv | record_id | 0 | 0,00% |
| customers_raw.csv | ho_ten | 0 | 0,00% |
| customers_raw.csv | so_dien_thoai | 4.133 | 6,17% |
| customers_raw.csv | email | 30.157 | 44,99% |
| customers_raw.csv | dia_chi | 6.023 | 8,98% |
| customers_raw.csv | ngay_tao | 0 | 0,00% |
| orders_2024_2026.csv | order_id | 0 | 0,00% |
| orders_2024_2026.csv | ma_don | 0 | 0,00% |
| orders_2024_2026.csv | ma_cua_hang | 0 | 0,00% |
| orders_2024_2026.csv | ngay | 114 | 0,44% |
| orders_2024_2026.csv | ten_khach | 0 | 0,00% |
| orders_2024_2026.csv | so_dien_thoai | 1.488 | 5,72% |
| orders_2024_2026.csv | thanh_tien | 279 | 1,07% |
| orders_2024_2026.csv | nhan_vien | 1.011 | 3,89% |
| orders_2024_2026.csv | ghi_chu | 12.961 | 49,85% |

| Trường cần cho phân khúc | Cột tìm thấy trong file |
|---|---|
| Mã khách | customers: record_id; orders: không có mã khách chung |
| Mã đơn | orders: có order_id và ma_don; cần xác nhận cột dùng làm mã đơn nghiệp vụ |
| Tên khách | customers: ho_ten; orders: ten_khach |
| Ngày mua | orders: ngay |
| Tổng tiền | orders: thanh_tien |
| Trạng thái đơn | Không có cột trạng thái trong file orders |

## 3. Kiểm tra chất lượng dữ liệu

| Yêu cầu chất lượng | Ngưỡng mục tiêu | Xử lý khi có lỗi |
|---|---|---|
| Đủ các cột bắt buộc để tính | 100% cột cần thiết có mặt | Thiếu cột thì dừng và báo tên cột thiếu |
| Các cột trọng yếu không bị thiếu | Mỗi cột trọng yếu đầy đủ ít nhất 95% trên dữ liệu nguồn | Báo tỷ lệ thiếu; không dùng dòng thiếu để gán nhãn |
| Mã đơn trong dữ liệu dùng tính không trùng | 0 mã đơn trùng | Bản trùng hoàn toàn giữ một; bản khác nhau cùng mã thì tách ra kiểm tra |
| Nối đơn với khách hàng | 100% đơn dùng tính nối được tới khách bằng mã ổn định | CSV chưa có mã khách chung; chưa tính phân khúc đến khi có ánh xạ được xác nhận |
| Ngày mua và tổng tiền hợp lệ | 100% trong dữ liệu dùng tính | Tách dòng sai; ghi lỗi cho khách liên quan |

Cột trọng yếu hiện có: customers.record_id; orders.order_id, ngay và thanh_tien. CSV chưa có mã khách chung trong bảng đơn.

Khách có lỗi dữ liệu quan trọng được ghi “Lỗi dữ liệu” (DATA_ERROR), chưa gán phân khúc. Khách không có đơn và không có lỗi thì chỉ số bằng 0. Không gộp các mã khách khác nhau vì việc gộp hồ sơ nằm ngoài phạm vi.

## 4. Cách tính và quy tắc phân khúc

- File đơn chưa có cột trạng thái; chưa xác định được đơn hoàn tất, hủy hoặc trả lại từ CSV hiện có.
- Tổng chi tiêu: cộng tổng tiền của các đơn trong 12 tháng gần nhất.
- Số đơn 12 tháng và số đơn 90 ngày: đếm mã đơn khác nhau trong từng khoảng thời gian.
- Một đơn có nhiều sản phẩm vẫn chỉ tính là một đơn; không cộng tổng tiền đơn nhiều lần.
- Ngày chốt là ngày đầu tháng kế tiếp; không tính giao dịch từ ngày chốt trở đi. Ví dụ kỳ 09/2026 dùng 12 tháng từ 01/10/2025 đến hết 30/09/2026.

| Phân khúc | Điều kiện theo QT-12 |
|---|---|
| VIP | Chi tiêu 12 tháng ≥30 triệu đồng HOẶC số đơn 12 tháng ≥8 |
| Thường xuyên | Chi tiêu 12 tháng ≥10 triệu đồng HOẶC số đơn 12 tháng ≥3 |
| Mới | Có đúng 1 đơn trong 90 ngày gần nhất |
| Ngủ đông | Các khách hợp lệ còn lại |

Ưu tiên lựa chọn: VIP → Thường xuyên → Mới → Ngủ đông. Mỗi khách hợp lệ chỉ có một nhãn.

## 5. Câu hỏi phân tích và mức chi tiết

| Mã | Cần trả lời câu hỏi nào? | Chi tiết theo | User Story |
|---|---|---|---|
| Q1 | Có bao nhiêu dữ liệu thiếu, sai hoặc trùng? Khách nào bị ảnh hưởng? | Nguồn dữ liệu và dòng lỗi | US-02 |
| Q2 | Mỗi khách chi tiêu bao nhiêu và mua bao nhiêu đơn? | Từng khách, từng kỳ | US-03 |
| Q3 | Khách thuộc nhóm nào? Những khách nào thuộc nhóm cần tìm? | Từng khách, từng kỳ, từng phân khúc | US-04, US-05 |
| Q4 | Mỗi phân khúc có bao nhiêu khách và chiếm tỷ lệ bao nhiêu? | Từng phân khúc, từng kỳ | US-07 |
| Q5 | Vì sao khách được xếp vào nhóm đó? | Từng khách, từng kỳ | US-08 |

Kỳ phân tích liên quan US-01; xuất danh sách liên quan US-06. Tỷ lệ phân khúc tính trên khách không lỗi; khách lỗi được thống kê riêng. Khi không có khách hợp lệ, tỷ lệ ghi “Không xác định”.

## 6. Kết quả đầu ra

| Tên cột | Thông tin hiển thị |
|---|---|
| customer_id | Mã khách |
| period | Tháng phân tích |
| spending_12m | Tổng chi tiêu 12 tháng, đơn vị đồng |
| order_count_12m | Số đơn 12 tháng |
| order_count_90d | Số đơn 90 ngày |
| segment | Phân khúc; để trống khi khách lỗi dữ liệu |
| data_status | Hợp lệ (OK) hoặc Lỗi dữ liệu (DATA_ERROR) |
| reason | Lý do gán phân khúc hoặc lỗi dữ liệu |
| rule_version | Phiên bản quy tắc đã sử dụng |

Mỗi khách có một dòng trong một kỳ. Các chỉ số của khách lỗi để trống, không thay bằng 0. Có thể lọc theo mã khách/phân khúc và xuất danh sách ra CSV. Không xuất số điện thoại, email hoặc địa chỉ mặc định.

Để chạy lại cho cùng kết quả, ghi rõ dữ liệu nguồn, kỳ và phiên bản quy tắc đã dùng.

