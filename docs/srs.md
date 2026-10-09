# SRS – Hệ thống phân khúc khách hàng

Trần Thị Như Quỳnh | MSSV: 2374802010428 | Track DA  
Luồng L1 – Hồ sơ khách hàng & phân khúc

## 1. Giới thiệu và phạm vi

Hệ thống hỗ trợ nhân viên Marketing phân khúc khách hàng theo
dữ liệu mua hàng và quy tắc QT-12 để lựa chọn nhóm khách phù hợp
cho hoạt động chăm sóc.

Phạm vi gồm kiểm tra dữ liệu, chọn kỳ, tính chỉ số mua hàng,
gán phân khúc, lọc danh sách, thống kê, xem căn cứ gán nhãn
và xuất CSV.

Ngoài phạm vi (WON'T): tạo hoặc gộp hồ sơ khách hàng,
quản lý bán hàng, tự động gửi khuyến mãi và dự báo bằng ML.

### Bảng thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Khách hàng | Đối tượng được phân khúc, nhận diện bằng mã khách nguồn |
| Đơn hàng | Giao dịch mua hàng; mỗi mã đơn hợp lệ được tính một lần |
| Phân khúc | Nhóm VIP, Thường xuyên, Mới hoặc Ngủ đông |
| Kỳ phân tích | Tháng được chọn để tính và xem kết quả |
| QT-12 | Quy tắc phân khúc theo chi tiêu và số đơn mua hàng |
| DATA_ERROR | Trạng thái khách có lỗi dữ liệu quan trọng, chưa được gán nhãn |
| FR / NFR | Yêu cầu chức năng / yêu cầu phi chức năng |
| GWT | Given: bối cảnh; When: hành động; Then: kết quả |
| MoSCoW | MUST: bắt buộc; SHOULD: nên có; COULD: có thể có; WON'T: ngoài phạm vi |

## 2. Các bên liên quan và vai trò

| Vai trò | Được thực hiện | Không được thực hiện trong phạm vi hệ thống |
|---|---|---|
| Nhân viên Marketing | Xem kết quả kiểm tra dữ liệu; chọn kỳ; yêu cầu tính phân khúc; xem chỉ số, thống kê, căn cứ; lọc và xuất kết quả | Sửa dữ liệu nguồn, thay đổi QT-12 hoặc tự sửa nhãn đã tính |
| Người phân tích dữ liệu | Xem kết quả kiểm tra chất lượng dữ liệu và nguyên nhân lỗi để xác định dữ liệu cần xử lý | Tự gán nhãn khách hoặc công bố kết quả khi nguồn chưa đủ điều kiện |

## 3. Yêu cầu chức năng

### 3.1. User Story

| Mã | Nội dung | MoSCoW |
|---|---|---|
| US-01 | Là nhân viên Marketing, tôi muốn chọn tháng phân tích để xem kết quả đúng kỳ cần đánh giá. | SHOULD |
| US-02 | Là người phân tích dữ liệu, tôi muốn xem kết quả kiểm tra chất lượng dữ liệu để xác định dữ liệu đủ điều kiện phân khúc và các lỗi cần xử lý. | MUST |
| US-03 | Là nhân viên Marketing, tôi muốn xem chi tiêu và số đơn của từng khách trong các cửa sổ quy định để đánh giá hoạt động mua hàng. | MUST |
| US-04 | Là nhân viên Marketing, tôi muốn yêu cầu gán phân khúc theo QT-12 để xác định nhóm khách cần chăm sóc. | MUST |
| US-05 | Là nhân viên Marketing, tôi muốn lọc theo phân khúc và mã khách để tìm đúng khách cần xem. | SHOULD |
| US-06 | Là nhân viên Marketing, tôi muốn xuất danh sách phân khúc để sử dụng và đối chiếu ngoài hệ thống. | COULD |
| US-07 | Là nhân viên Marketing, tôi muốn xem số lượng và tỷ lệ từng phân khúc để đánh giá quy mô các nhóm khách. | SHOULD |
| US-08 | Là nhân viên Marketing, tôi muốn xem căn cứ gán phân khúc để kiểm tra và giải thích kết quả. | SHOULD |

### 3.2. Yêu cầu chức năng

| Mã | Yêu cầu |
|---|---|
| FR-01 | Cho chọn tháng đã kết thúc; mặc định là tháng hoàn tất gần nhất. Báo lỗi nếu kỳ không hợp lệ. |
| FR-02 | Kiểm tra cột bắt buộc, khóa, ngày, tiền, ánh xạ khách và trạng thái đơn; hiển thị số dòng hợp lệ, lỗi, trùng bị loại. Chặn tính khi nguồn chưa đủ điều kiện. |
| FR-03 | Tính tổng chi tiêu 12 tháng, số đơn 12 tháng và số đơn 90 ngày cho từng khách từ các đơn hoàn tất hợp lệ. |
| FR-04 | Gán đúng một phân khúc theo QT-12 cho khách hợp lệ; khách lỗi được ghi DATA_ERROR và để trống phân khúc. |
| FR-05 | Cho lọc theo phân khúc, mã khách hoặc kết hợp cả hai trong kỳ đang xem. |
| FR-06 | Xuất đúng danh sách sau lọc ra CSV UTF-8, có tiêu đề cột và kỳ phân tích. |
| FR-07 | Hiển thị số khách và tỷ lệ từng phân khúc trên tổng khách OK; thống kê khách lỗi riêng. Nếu không có khách OK, tỷ lệ là “Không xác định”. |
| FR-08 | Hiển thị chỉ số, căn cứ gán nhãn và phiên bản quy tắc; khách lỗi hiển thị nguyên nhân lỗi. |

### 3.3. Tiêu chí chấp nhận cho các User Story MUST

| Mã | US | Given – Bối cảnh | When – Hành động | Then – Kết quả |
|---|---|---|---|---|
| AC-01 | US-02 | Nguồn đủ cột, đã xác nhận ánh xạ khách và trạng thái đơn | Kiểm tra dữ liệu | Hiển thị số dòng hợp lệ và lỗi |
| AC-02 | US-02 | Có bản ghi đơn hàng trùng hoàn toàn | Kiểm tra dữ liệu | Giữ một bản, ghi số bản trùng bị loại |
| AC-03 – ngoại lệ | US-02 | Thiếu cột hoặc chưa xác nhận ánh xạ khách/trạng thái đơn | Kiểm tra dữ liệu | Báo lỗi nguồn và chặn tính phân khúc |
| AC-04 | US-03 | Khách có hai đơn hoàn tất hợp lệ 6 triệu và 4 triệu trong 12 tháng | Tính chỉ số | Chi tiêu bằng 10 triệu, số đơn 12 tháng bằng 2 |
| AC-05 | US-03 | Một đơn hoàn tất hợp lệ có ba dòng hàng trong dữ liệu kiểm thử | Tính chỉ số | Đếm một đơn và cộng tổng tiền đơn một lần |
| AC-06 – ngoại lệ | US-03 | Đơn thiếu tổng tiền hoặc sai ngày mua, xác định được khách | Tính chỉ số | Ghi khách DATA_ERROR, để trống các chỉ số |
| AC-07 | US-04 | Khách hợp lệ có chi tiêu đúng 30 triệu hoặc đúng 8 đơn trong 12 tháng | Gán phân khúc | Gán VIP |
| AC-08 | US-04 | Khách hợp lệ đồng thời đạt VIP và Thường xuyên | Gán phân khúc | Chỉ gán VIP |
| AC-09 – ngoại lệ | US-04 | Khách có lỗi dữ liệu quan trọng | Gán phân khúc | Để trống phân khúc, hiển thị nguyên nhân lỗi |

Sơ đồ Use Case: [usecase.drawio](usecase.drawio).
UC-03 phục vụ cả US-01 và US-04 nên tám User Story liên kết
với bảy Use Case.

## 4. Yêu cầu phi chức năng

| Mã | Yêu cầu | Cách kiểm tra |
|---|---|---|
| NFR-01 | Tính phân khúc ≤60 giây với bộ kiểm thử 65.000 khách và 26.000 đơn trên máy 4 lõi CPU, RAM 8 GB | Đo ba lần; mỗi lần ≤60 giây |
| NFR-02 | 100% khách hợp lệ có đúng một nhãn; 0 dòng trùng mã khách/kỳ | Kiểm tra nhãn và khóa kết quả |
| NFR-03 | Ba lần chạy cùng dữ liệu, kỳ và phiên bản quy tắc cho chỉ số và nhãn giống nhau 100% | So sánh kết quả theo mã khách/kỳ |

## 5. Ràng buộc và quy tắc nghiệp vụ

### 5.1. Điều kiện phân khúc theo QT-12

| Phân khúc | Điều kiện |
|---|---|
| VIP | Chi tiêu 12 tháng ≥30 triệu đồng HOẶC số đơn 12 tháng ≥8 |
| Thường xuyên | Chi tiêu 12 tháng ≥10 triệu đồng HOẶC số đơn 12 tháng ≥3 |
| Mới | Có đúng một đơn trong 90 ngày gần nhất |
| Ngủ đông | Các khách hợp lệ còn lại |

### 5.2. Quy tắc xử lý

| Mã | Quy tắc |
|---|---|
| BR-01 | Ưu tiên VIP → Thường xuyên → Mới → Ngủ đông; mỗi khách hợp lệ nhận đúng một nhãn. |
| BR-02 | Tính theo tháng. Ngày chốt D là 00:00 ngày đầu tháng kế tiếp, múi giờ Asia/Ho_Chi_Minh. Dùng cửa sổ [D−12 tháng lịch, D) và [D−90 ngày, D). |
| BR-03 | Chỉ dùng đơn hoàn tất hợp lệ. Đếm mã đơn khác nhau; tổng tiền mỗi đơn chỉ cộng một lần. |
| BR-04 | Bản trùng hoàn toàn giữ một; các bản mâu thuẫn cùng mã đơn được cách ly để kiểm tra. |
| BR-05 | Khách không có đơn và không lỗi có chỉ số bằng 0. Khách có lỗi quan trọng được ghi DATA_ERROR, để trống chỉ số và phân khúc. |
| BR-06 | Nếu không xác định được khách bị ảnh hưởng bởi lỗi thì chặn công bố kết quả. Không tự gộp hồ sơ dựa trên tên hoặc số điện thoại. |
| BR-07 | Chỉ thay kết quả cũ khi toàn bộ kết quả mới được lưu thành công; nếu thất bại thì giữ kết quả trước đó. |

CSV hiện có chưa chứa mã khách chung giữa hai nguồn và chưa có
trạng thái đơn. Phải xác nhận mã đơn nghiệp vụ, ánh xạ đơn–khách
và cách nhận diện đơn hoàn tất trước khi tính phân khúc.

Chi tiết nguồn, chất lượng và đầu ra:
[data-requirements.md](data-requirements.md).

## 6. Bảng truy vết yêu cầu

| FR | User Story | Use Case | MoSCoW |
|---|---|---|---|
| FR-01 | US-01 | UC-03 – Tính và gán phân khúc khách hàng | SHOULD |
| FR-02 | US-02 | UC-01 – Xem kết quả kiểm tra chất lượng dữ liệu | MUST |
| FR-03 | US-03 | UC-02 – Xem chỉ số mua hàng của khách | MUST |
| FR-04 | US-04 | UC-03 – Tính và gán phân khúc khách hàng | MUST |
| FR-05 | US-05 | UC-04 – Lọc danh sách khách theo phân khúc | SHOULD |
| FR-06 | US-06 | UC-05 – Xuất danh sách phân khúc | COULD |
| FR-07 | US-07 | UC-06 – Xem thống kê phân khúc | SHOULD |
| FR-08 | US-08 | UC-07 – Xem căn cứ gán phân khúc | SHOULD |