# SRS – L1: Tính và gán phân khúc khách hàng

Trần Thị Như Quỳnh | MSSV: 2374802010428 | Track DA

## 1. Giới thiệu

Công cụ giúp nhân viên Marketing phân khúc khách hàng theo dữ liệu mua hàng và QT-12 để lựa chọn nhóm khách phù hợp cho hoạt động chăm sóc.

| Thuật ngữ | Ý nghĩa |
|---|---|
| customer | Khách hàng |
| order | Đơn hàng |
| order_item | Dòng hàng trong đơn |
| customer_segment | Kết quả phân khúc |
| FR / NFR | Yêu cầu chức năng / yêu cầu phi chức năng |
| GWT | Given – bối cảnh; When – hành động; Then – kết quả cần đạt |

## 2. Phạm vi và quy tắc

- Người sử dụng: nhân viên Marketing.
- Thực hiện: kiểm tra dữ liệu, tính chỉ số mua hàng, gán phân khúc, lọc, thống kê và xem căn cứ phân khúc; xuất CSV ở mức COULD.
- Không thực hiện: tạo/gộp hồ sơ khách hàng, gửi khuyến mãi hoặc dự báo bằng ML.

| Phân khúc | Điều kiện theo QT-12 |
|---|---|
| VIP | Chi tiêu 12 tháng ≥30 triệu đồng HOẶC số đơn 12 tháng ≥8 |
| Thường xuyên | Chi tiêu 12 tháng ≥10 triệu đồng HOẶC số đơn 12 tháng ≥3 |
| Mới | Có đúng 1 đơn trong 90 ngày gần nhất |
| Ngủ đông | Các khách hợp lệ còn lại |

Quy ước của bài:

- Ưu tiên VIP → Thường xuyên → Mới → Ngủ đông; mỗi khách hợp lệ chỉ nhận một nhãn.
- Tính lại hàng tháng. Ngày chốt là ngày đầu tháng kế tiếp; lấy 12 tháng lịch và 90 ngày trước ngày chốt, không tính giao dịch từ ngày chốt trở đi.
- Chỉ dùng đơn hoàn tất hợp lệ; mỗi mã đơn được đếm và cộng tiền một lần. Trạng thái đơn cần đối chiếu dữ liệu nguồn.
- Không có đơn và không có lỗi: chỉ số bằng 0. Khách thiếu dữ liệu quan trọng: ghi DATA_ERROR, chưa gán phân khúc.

## 3. User Story và yêu cầu chức năng

### 3.1. User Story

| Mã | Nội dung | MoSCoW |
|---|---|---|
| US-01 | Là nhân viên Marketing, tôi muốn chọn tháng phân tích để xem kết quả đúng kỳ cần đánh giá. | SHOULD |
| US-02 | Là nhân viên Marketing, tôi muốn xem kết quả kiểm tra chất lượng dữ liệu để nhận biết dữ liệu chưa đủ tin cậy cho việc phân khúc. | MUST |
| US-03 | Là nhân viên Marketing, tôi muốn xem tổng chi tiêu và số đơn của từng khách trong 12 tháng để đánh giá giá trị mua hàng của khách. | MUST |
| US-04 | Là nhân viên Marketing, tôi muốn gán phân khúc theo QT-12 để xác định nhóm khách cần chăm sóc. | MUST |
| US-05 | Là nhân viên Marketing, tôi muốn lọc danh sách theo phân khúc và mã khách để tìm đúng khách cần xem. | SHOULD |
| US-06 | Là nhân viên Marketing, tôi muốn xuất danh sách phân khúc để sử dụng và đối chiếu kết quả ngoài công cụ. | COULD |
| US-07 | Là nhân viên Marketing, tôi muốn xem số lượng và tỷ lệ từng phân khúc để đánh giá quy mô các nhóm khách. | SHOULD |
| US-08 | Là nhân viên Marketing, tôi muốn xem căn cứ gán phân khúc của từng khách để kiểm tra và giải thích kết quả. | SHOULD |

### 3.2. Tiêu chí chấp nhận GWT cho MUST

| Mã | US | Given – Bối cảnh | When – Hành động | Then – Kết quả |
|---|---|---|---|---|
| AC-01 | US-02 | Dữ liệu đủ cột bắt buộc, khóa và giá trị hợp lệ | Kiểm tra dữ liệu | Hiện số dòng hợp lệ và số dòng lỗi |
| AC-02 | US-02 | Có bản ghi đơn hàng trùng hoàn toàn | Kiểm tra dữ liệu | Chỉ giữ một bản, ghi số bản trùng bị loại |
| AC-03 – ngoại lệ | US-02 | Thiếu cột bắt buộc | Kiểm tra dữ liệu | Báo tên cột thiếu và chặn tính phân khúc |
| AC-04 | US-03 | Khách có hai đơn hợp lệ 6 triệu và 4 triệu trong cửa sổ 12 tháng | Tính chỉ số | Chi tiêu bằng 10 triệu, số đơn bằng 2 |
| AC-05 | US-03 | Một đơn có ba dòng hàng | Tính chỉ số | Đếm một đơn, tổng tiền đơn chỉ cộng một lần |
| AC-06 – ngoại lệ | US-03 | Đơn thiếu tổng tiền hoặc ngày mua không hợp lệ | Tính chỉ số | Ghi khách DATA_ERROR, không công bố chỉ số của khách đó |
| AC-07 | US-04 | Khách chi tiêu đúng 30 triệu hoặc có đúng 8 đơn trong 12 tháng | Gán phân khúc | Khách thuộc VIP |
| AC-08 | US-04 | Khách đồng thời đạt VIP và Thường xuyên | Gán phân khúc | Chỉ gán VIP theo thứ tự ưu tiên |
| AC-09 – ngoại lệ | US-04 | Khách có lỗi dữ liệu quan trọng | Gán phân khúc | Phân khúc để trống, hiển thị lý do lỗi |

### 3.3. Yêu cầu chức năng

| Mã | Yêu cầu |
|---|---|
| FR-01 | Cho chọn kỳ phân tích; dùng kỳ mặc định nếu chưa chọn. |
| FR-02 | Kiểm tra dữ liệu, báo số dòng hợp lệ/lỗi và lý do lỗi. |
| FR-03 | Tính tổng chi tiêu, số đơn 12 tháng và số đơn 90 ngày của từng khách. |
| FR-04 | Gán một phân khúc theo QT-12 cho khách hợp lệ. |
| FR-05 | Lọc kết quả theo phân khúc hoặc mã khách. |
| FR-06 | Xuất danh sách đã lọc ra CSV theo Data spec. |
| FR-07 | Thống kê số lượng và tỷ lệ từng phân khúc; báo khách lỗi riêng. |
| FR-08 | Hiển thị chỉ số và lý do gán nhãn của từng khách. |

## 4. Use Case

Actor: nhân viên Marketing. Sơ đồ: `docs/use-case.drawio`.

| Mã | Use Case |
|---|---|
| UC-01 | Xem kết quả kiểm tra chất lượng dữ liệu |
| UC-02 | Xem chỉ số mua hàng của khách |
| UC-03 | Tính và gán phân khúc khách hàng |
| UC-04 | Lọc danh sách khách theo phân khúc |
| UC-05 | Xuất danh sách phân khúc |
| UC-06 | Xem thống kê phân khúc |
| UC-07 | Xem căn cứ gán phân khúc |

### Đặc tả UC-03

- Mục tiêu: tạo kết quả phân khúc theo QT-12.
- Actor: nhân viên Marketing.
- Bắt đầu: Marketing yêu cầu tính phân khúc.
- Điều kiện trước: có kỳ phân tích và nguồn dữ liệu truy cập được; Marketing có quyền đọc dữ liệu.
- Điều kiện sau thành công: có chỉ số, phân khúc và lý do theo khách/kỳ; khách lỗi được tách riêng.
- Điều kiện sau thất bại: không công bố kết quả dở dang, giữ kết quả trước đó.

Luồng chính:

1. Marketing xác nhận kỳ phân tích.
2. Hệ thống kiểm tra kỳ và dữ liệu đầu vào.
3. Hệ thống tính chi tiêu và số đơn hợp lệ.
4. Hệ thống áp dụng QT-12 theo thứ tự ưu tiên.
5. Hệ thống tạo kết quả, báo số khách hợp lệ và khách lỗi.
6. Marketing xem kết quả.

Luồng ngoại lệ:

- **2a:** Kỳ sai hoặc chưa kết thúc → báo lỗi, trở về bước 1.
- **2b:** Thiếu cột bắt buộc hoặc không đọc được nguồn → dừng, báo lỗi.
- **3a:** Dòng dữ liệu lỗi → ghi DATA_ERROR cho khách bị ảnh hưởng; nếu không xác định được khách bị ảnh hưởng thì chưa công bố kết quả.
- **5a:** Tạo/lưu kết quả thất bại → báo lỗi, giữ kết quả trước đó.

## 5. Yêu cầu phi chức năng

| Mã | Yêu cầu | Cách kiểm tra |
|---|---|---|
| NFR-01 | Tính phân khúc ≤60 giây với dữ liệu kiểm thử 65.000 khách và 26.000 đơn trên máy 4 lõi CPU, RAM 8 GB | Đo 3 lần, mỗi lần ≤60 giây |
| NFR-02 | 100% khách hợp lệ có một nhãn; 0 dòng trùng mã khách/kỳ | Kiểm tra nhãn và khóa kết quả |
| NFR-03 | Chạy lại 3 lần với cùng dữ liệu, kỳ và phiên bản quy tắc cho chỉ số/nhãn giống nhau 100% | So sánh kết quả theo mã khách/kỳ |

## 6. Dữ liệu và bảng truy vết

Đầu vào: dữ liệu khách hàng, đơn hàng; dòng hàng dùng đối chiếu nếu có nguồn. Đầu ra: kết quả phân khúc và báo cáo lỗi. Chi tiết: `docs/data-spec.md`.

| FR | US | Use Case | MoSCoW |
|---|---|---|---|
| FR-01 | US-01 | UC-03 | SHOULD |
| FR-02 | US-02 | UC-01 | MUST |
| FR-03 | US-03 | UC-02 | MUST |
| FR-04 | US-04 | UC-03 | MUST |
| FR-05 | US-05 | UC-04 | SHOULD |
| FR-06 | US-06 | UC-05 | COULD |
| FR-07 | US-07 | UC-06 | SHOULD |
| FR-08 | US-08 | UC-07 | SHOULD |
