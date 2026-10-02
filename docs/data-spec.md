# Đặc tả yêu cầu dữ liệu – Track DA – L1

Trần Thị Như Quỳnh | MSSV: 2374802010428

Mục tiêu: dùng dữ liệu mua hàng để chia khách thành VIP, Thường xuyên, Mới và Ngủ đông theo QT-12.

## 1. Nguồn dữ liệu

| Dữ liệu | Nguồn dự kiến | Định dạng | Cập nhật / xử lý | Khối lượng |
|---|---|---|---|---|
| Khách hàng | customers_raw.csv của case study | CSV | Kiểm tra mỗi lần nhận file; lịch cập nhật nguồn chưa xác nhận | Khoảng 65.000 hồ sơ theo case study; chưa đếm file |
| Đơn hàng | orders_2024_2026.csv của case study | CSV | Tính phân khúc hằng tháng; lịch cập nhật nguồn chưa xác nhận | Chưa đếm file |
| Chi tiết đơn hàng | order_item, dùng đối chiếu nếu có nguồn | CSV hoặc bảng | Kiểm tra cùng dữ liệu đơn hàng | Chưa xác nhận nguồn và số dòng |

## 2. Các thông tin cần có

| Dữ liệu | Tên cột dự kiến | Ý nghĩa | Kiểu dữ liệu | Điều kiện hợp lệ | Tỷ lệ thiếu trên mẫu |
|---|---|---|---|---|---|
| Khách hàng | customer_id | Mã khách hàng | Chuỗi | Có giá trị, không trùng | Chưa đo |
| Khách hàng | full_name | Tên khách hàng | Chuỗi | Dùng khi tra cứu theo tên | Chưa đo |
| Đơn hàng | order_id | Mã đơn hàng | Chuỗi | Có giá trị, không trùng sau xử lý | Chưa đo |
| Đơn hàng | customer_id | Mã khách của đơn | Chuỗi | Có trong danh sách khách hàng | Chưa đo |
| Đơn hàng | order_date | Ngày mua hàng | Ngày/giờ | Đọc được ngày, thuộc kỳ khi tính | Chưa đo |
| Đơn hàng | total_amount | Tổng tiền sau giảm giá | Số | Không âm, đơn vị đồng | Chưa đo |
| Đơn hàng | status | Trạng thái đơn | Chuỗi | Phân biệt hoàn tất, hủy, trả lại theo dữ liệu nguồn | Chưa đo |
| Chi tiết đơn | order_id | Mã đơn liên quan | Chuỗi | Có trong danh sách đơn hàng | Chưa đo |
| Chi tiết đơn | line_id | Mã dòng hàng | Chuỗi | Không trùng trong cùng đơn | Chưa đo |
| Chi tiết đơn | quantity | Số lượng sản phẩm | Số nguyên | Lớn hơn 0 | Chưa đo |
| Chi tiết đơn | unit_price | Đơn giá | Số | Không âm, đơn vị đồng | Chưa đo |

Tỷ lệ thiếu = số dòng thiếu thông tin ở cột / tổng số dòng × 100%.

## 3. Kiểm tra chất lượng dữ liệu

| Yêu cầu chất lượng | Ngưỡng mục tiêu | Xử lý khi có lỗi |
|---|---|---|
| Đủ các cột bắt buộc để tính | 100% cột cần thiết có mặt | Thiếu cột thì dừng và báo tên cột thiếu |
| Các cột trọng yếu không bị thiếu | Mỗi cột trọng yếu đầy đủ ít nhất 95% trên dữ liệu nguồn | Báo tỷ lệ thiếu; không dùng dòng thiếu để gán nhãn |
| Mã đơn trong dữ liệu dùng tính không trùng | 0 mã đơn trùng | Bản trùng hoàn toàn giữ một; bản khác nhau cùng mã thì tách ra kiểm tra |
| Mã khách của đơn tồn tại | 100% trong dữ liệu dùng tính | Tách đơn không tìm được khách; nếu không xác định khách bị ảnh hưởng thì chưa công bố kết quả |
| Ngày mua và tổng tiền hợp lệ | 100% trong dữ liệu dùng tính | Tách dòng sai; ghi lỗi cho khách liên quan |

Cột trọng yếu: mã khách ở bảng khách; mã đơn, mã khách, ngày mua và tổng tiền ở bảng đơn.

Khách có lỗi dữ liệu quan trọng được ghi “Lỗi dữ liệu” (DATA_ERROR), chưa gán phân khúc. Khách không có đơn và không có lỗi thì chỉ số bằng 0. Không gộp các mã khách khác nhau vì việc gộp hồ sơ nằm ngoài phạm vi.

## 4. Cách tính và quy tắc phân khúc

- Chỉ tính đơn hoàn tất hợp lệ; cách xử lý đơn hủy/trả lại cần đối chiếu trạng thái nguồn.
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

