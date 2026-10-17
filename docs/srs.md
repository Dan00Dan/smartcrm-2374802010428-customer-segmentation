# SRS – Hệ thống phân khúc khách hàng

**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst (DA)  
**Luồng:** L1 – Hồ sơ khách hàng và phân khúc

## 1. Giới thiệu và phạm vi

Hệ thống hỗ trợ nhân viên Marketing kiểm tra dữ liệu mua hàng, tính chỉ số mua hàng và phân khúc khách hàng theo quy tắc QT-12, phục vụ việc lựa chọn nhóm khách phù hợp cho hoạt động chăm sóc.

Phạm vi gồm kiểm tra chất lượng dữ liệu, chọn kỳ phân tích, tính chỉ số mua hàng, gán phân khúc, lọc danh sách, thống kê, xem căn cứ gán nhãn và xuất CSV.

**Ngoài phạm vi (WON'T):** tạo hoặc gộp hồ sơ khách hàng, quản lý hoạt động bán hàng, tự động gửi khuyến mãi và dự báo bằng Machine Learning.

### 1.1. Bảng thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Khách hàng | Đối tượng được phân khúc, nhận diện bằng mã khách hàng nguồn đã được xác nhận ánh xạ. |
| Đơn hàng | Giao dịch mua hàng được nhận diện bằng mã đơn nghiệp vụ; mỗi đơn hợp lệ chỉ được tính một lần. |
| Đơn hoàn tất | Đơn hàng có trạng thái hoàn tất theo quy ước trạng thái đã được xác nhận trong dữ liệu nguồn. |
| Chỉ số mua hàng | Các chỉ số gồm tổng chi tiêu 12 tháng, số đơn 12 tháng và số đơn 90 ngày. |
| Phân khúc | Nhóm khách hàng gồm VIP, Thường xuyên, Mới hoặc Ngủ đông. |
| Kỳ phân tích | Tháng được chọn để tính toán và xem kết quả phân khúc. |
| Ngày chốt (D) | Thời điểm 00:00 ngày đầu tiên của tháng kế tiếp, theo múi giờ Asia/Ho_Chi_Minh. |
| Cửa sổ thời gian | Khoảng thời gian dùng để tính chỉ số mua hàng, gồm 12 tháng lịch và 90 ngày trước ngày chốt. |
| QT-12 | Quy tắc phân khúc khách hàng theo chi tiêu và số đơn mua hàng. |
| DATA_ERROR | Trạng thái khách hàng có lỗi dữ liệu quan trọng, chưa đủ điều kiện tính chỉ số hoặc gán phân khúc. |
| Lần chạy | Một lượt thực hiện kiểm tra dữ liệu, tính chỉ số và gán phân khúc cho kỳ phân tích. |
| Nhật ký vận hành | Thông tin về lần chạy, trạng thái xử lý và lỗi phát sinh trong quá trình thực hiện. |
| FR / NFR | Yêu cầu chức năng / yêu cầu phi chức năng. |
| GWT | Given: bối cảnh; When: hành động; Then: kết quả mong đợi. |
| MoSCoW | MUST: bắt buộc; SHOULD: nên có; COULD: có thể có; WON'T: ngoài phạm vi. |

## 2. Các bên liên quan và vai trò

| Vai trò | Được thực hiện | Không được thực hiện trong phạm vi hệ thống |
|---|---|---|
| Nhân viên Marketing | Xem kết quả kiểm tra dữ liệu; chọn kỳ; yêu cầu tính phân khúc; xem chỉ số, thống kê và căn cứ; lọc và xuất kết quả. | Sửa dữ liệu nguồn, thay đổi QT-12 hoặc tự sửa nhãn đã tính. |
| Người phân tích dữ liệu | Xem kết quả kiểm tra chất lượng dữ liệu và nguyên nhân lỗi để xác định dữ liệu cần xử lý. | Tự ý gán nhãn hoặc công bố kết quả khi nguồn chưa đủ điều kiện. |

## 3. Yêu cầu chức năng

### 3.1. User Story

| Mã | Nội dung | MoSCoW |
|---|---|---|
| US-01 | Là người phân tích dữ liệu, tôi muốn xem kết quả kiểm tra chất lượng dữ liệu để xác định dữ liệu đủ điều kiện phân khúc và các lỗi cần xử lý. | MUST |
| US-02 | Là nhân viên Marketing, tôi muốn xem chi tiêu và số đơn của từng khách trong các cửa sổ thời gian quy định để đánh giá hoạt động mua hàng. | MUST |
| US-03 | Là nhân viên Marketing, tôi muốn chọn tháng phân tích và yêu cầu gán phân khúc theo QT-12 để xác định nhóm khách cần chăm sóc trong đúng kỳ. | MUST |
| US-04 | Là nhân viên Marketing, tôi muốn lọc theo phân khúc và mã khách để tìm đúng khách cần xem. | SHOULD |
| US-05 | Là nhân viên Marketing, tôi muốn xuất danh sách phân khúc để sử dụng và đối chiếu ngoài hệ thống. | COULD |
| US-06 | Là nhân viên Marketing, tôi muốn xem số lượng và tỷ lệ từng phân khúc để đánh giá quy mô các nhóm khách. | SHOULD |
| US-07 | Là nhân viên Marketing, tôi muốn xem căn cứ gán phân khúc để kiểm tra và giải thích kết quả. | SHOULD |

**Lưu ý:** US-03 gộp nội dung chọn kỳ của US-01 cũ và yêu cầu gán phân khúc của US-04 cũ. Các mã User Story được đánh số lại để bảo đảm có đúng 7 User Story.

### 3.2. Yêu cầu chức năng

| Mã | Yêu cầu |
|---|---|
| FR-01 | Cho phép chọn tháng đã kết thúc; mặc định là tháng hoàn tất gần nhất. Báo lỗi nếu kỳ không hợp lệ. |
| FR-02 | Kiểm tra cột bắt buộc, khóa, ngày, tiền, ánh xạ khách hàng và trạng thái đơn; hiển thị số dòng hợp lệ, lỗi và bản trùng bị loại. Chặn tính phân khúc khi nguồn chưa đủ điều kiện. |
| FR-03 | Tính tổng chi tiêu 12 tháng, số đơn 12 tháng và số đơn 90 ngày cho từng khách từ các đơn hoàn tất hợp lệ. |
| FR-04 | Gán đúng một phân khúc theo QT-12 cho mỗi khách hợp lệ; khách có lỗi quan trọng được ghi DATA_ERROR và để trống phân khúc. |
| FR-05 | Cho phép lọc theo phân khúc, mã khách hoặc kết hợp cả hai trong kỳ đang xem. |
| FR-06 | Xuất đúng danh sách sau lọc ra CSV UTF-8, có tiêu đề cột và thông tin kỳ phân tích. |
| FR-07 | Hiển thị số khách và tỷ lệ từng phân khúc trên tổng khách OK; thống kê khách lỗi riêng. Nếu không có khách OK, tỷ lệ hiển thị là “Không xác định”. |
| FR-08 | Hiển thị chỉ số, căn cứ gán nhãn và phiên bản quy tắc; khách lỗi hiển thị nguyên nhân lỗi. |

### 3.3. Tiêu chí chấp nhận cho các User Story MUST

| Mã | US | Given – Bối cảnh | When – Hành động | Then – Kết quả |
|---|---|---|---|---|
| AC-01 | US-01 | Nguồn đủ cột, đã xác nhận ánh xạ khách và trạng thái đơn. | Kiểm tra dữ liệu. | Hiển thị số dòng hợp lệ, số lỗi và bản trùng bị loại. |
| AC-02 | US-01 | Có bản ghi trùng hoàn toàn. | Kiểm tra dữ liệu. | Giữ một bản, ghi nhận số bản trùng bị loại. |
| AC-03 | US-01 | Thiếu cột bắt buộc hoặc chưa xác nhận ánh xạ khách/trạng thái đơn. | Kiểm tra dữ liệu. | Báo lỗi nguồn và chặn tính phân khúc. |
| AC-04 | US-02 | Khách có hai đơn hoàn tất hợp lệ trị giá 6 triệu và 4 triệu trong 12 tháng. | Tính chỉ số. | Chi tiêu bằng 10 triệu đồng, số đơn 12 tháng bằng 2. |
| AC-05 | US-02 | Một đơn hoàn tất hợp lệ có ba dòng hàng trong dữ liệu kiểm thử. | Tính chỉ số. | Đếm một đơn và chỉ cộng tổng tiền của đơn một lần. |
| AC-06 | US-02 | Đơn thiếu tổng tiền hoặc có ngày mua không hợp lệ, xác định được khách bị ảnh hưởng. | Tính chỉ số. | Ghi nhận DATA_ERROR cho khách, để trống các chỉ số và phân khúc theo BR-05. |
| AC-07 | US-03 | Kỳ phân tích hợp lệ và khách có chi tiêu đúng 30 triệu đồng hoặc đúng 8 đơn trong 12 tháng. | Chọn kỳ và yêu cầu gán phân khúc. | Tính theo kỳ đã chọn và gán VIP. |
| AC-08 | US-03 | Khách hợp lệ đồng thời đạt điều kiện VIP và Thường xuyên. | Gán phân khúc. | Chỉ gán VIP theo thứ tự ưu tiên. |
| AC-09 | US-03 | Khách có lỗi dữ liệu quan trọng. | Yêu cầu gán phân khúc. | Không gán nhãn, để trống phân khúc và hiển thị nguyên nhân lỗi. |

Sơ đồ Use Case: `usecase.drawio`.

UC-03 – Tính và gán phân khúc khách hàng – hỗ trợ US-03, bao gồm chọn kỳ phân tích và yêu cầu tính phân khúc. Hệ thống có 7 User Story và 7 Use Case; quan hệ giữa User Story và Use Case được thể hiện trong bảng truy vết.

## 4. Yêu cầu phi chức năng

| Mã | Yêu cầu | Cách kiểm tra |
|---|---|---|
| NFR-01 | Thời gian tính phân khúc không vượt quá 60 giây với bộ kiểm thử gồm 65.000 khách hàng và 26.000 đơn, trên máy có CPU 4 lõi và RAM 8 GB. | Chạy ba lần trong cùng điều kiện; mỗi lần phải hoàn thành trong tối đa 60 giây. Ghi lại thời gian từng lần và môi trường kiểm thử. |
| NFR-02 | 100% khách hợp lệ có đúng một nhãn; không có dòng trùng khóa khách hàng/kỳ phân tích trong kết quả công bố. | Kiểm tra số lượng nhãn và tính duy nhất của khóa khách hàng/kỳ. |
| NFR-03 | Ba lần chạy với cùng dữ liệu đầu vào, kỳ phân tích và phiên bản quy tắc phải cho chỉ số và nhãn giống nhau 100%. | So sánh kết quả theo mã khách hàng và kỳ phân tích giữa ba lần chạy. |

## 5. Ràng buộc và quy tắc nghiệp vụ

### 5.1. Điều kiện phân khúc theo QT-12

| Phân khúc | Điều kiện |
|---|---|
| VIP | Chi tiêu 12 tháng ≥ 30 triệu đồng HOẶC số đơn 12 tháng ≥ 8. |
| Thường xuyên | Chi tiêu 12 tháng ≥ 10 triệu đồng HOẶC số đơn 12 tháng ≥ 3. |
| Mới | Có đúng một đơn hoàn tất hợp lệ trong 90 ngày gần nhất. |
| Ngủ đông | Khách hợp lệ còn lại sau khi xét các nhóm ưu tiên cao hơn. |

### 5.2. Quy tắc nghiệp vụ

| Mã | Quy tắc |
|---|---|
| BR-01 | Ưu tiên VIP → Thường xuyên → Mới → Ngủ đông. Mỗi khách hợp lệ nhận đúng một nhãn. |
| BR-02 | Tính theo tháng. Ngày chốt D là 00:00 ngày đầu tháng kế tiếp theo múi giờ Asia/Ho_Chi_Minh. Dùng cửa sổ [D − 12 tháng lịch, D) và [D − 90 ngày, D). |
| BR-03 | Chỉ sử dụng đơn hoàn tất hợp lệ. Đếm mã đơn khác nhau; tổng tiền mỗi đơn chỉ cộng một lần. |
| BR-04 | Bản trùng hoàn toàn giữ một bản; các bản mâu thuẫn cùng mã đơn được cách ly để kiểm tra. |
| BR-05 | Khách không có đơn và không có lỗi có chỉ số bằng 0. Khách có lỗi quan trọng được ghi DATA_ERROR và để trống chỉ số, phân khúc. |
| BR-06 | Nếu không xác định được khách bị ảnh hưởng bởi lỗi thì chặn công bố kết quả. Không tự gộp hồ sơ dựa trên tên hoặc số điện thoại. |
| BR-07 | Chỉ thay kết quả cũ khi toàn bộ kết quả mới được lưu thành công. Nếu lưu thất bại, giữ nguyên kết quả trước đó. |
| BR-08 | Thông tin lần chạy và lỗi phát sinh phải được ghi nhận trong nhật ký vận hành, tách biệt với lược đồ hình sao phục vụ phân tích. |

### 5.3. Nguồn dữ liệu và điều kiện thực hiện

CSV hiện có chưa chứa mã khách hàng chung giữa các nguồn và chưa có trạng thái đơn. Trước khi tính phân khúc, phải xác nhận mã đơn nghiệp vụ, ánh xạ đơn–khách hàng và cách nhận diện đơn hoàn tất.

Chi tiết nguồn, chất lượng, điều kiện sử dụng và đầu ra: `data-requirements.md`.

### 5.4. Kiến trúc lưu trữ và nhật ký vận hành

Hệ thống gồm các thành phần xử lý dữ liệu nguồn, kiểm tra chất lượng dữ liệu, tính chỉ số và gán phân khúc, lưu kết quả phân tích, và lưu nhật ký vận hành.

- **Kho dữ liệu phân tích:** lưu kết quả theo khóa khách hàng/kỳ phân tích và các thông tin cần thiết để truy xuất căn cứ gán nhãn.
- **Nhật ký vận hành:** lưu mã lần chạy, kỳ phân tích, thời điểm chạy, trạng thái thực hiện và thông tin lỗi phù hợp.
- **Nguyên tắc lưu kết quả:** chỉ công bố kết quả mới khi toàn bộ kết quả được lưu thành công; nếu thất bại, giữ kết quả đã công bố trước đó.

Nhật ký vận hành có thể được triển khai bằng bảng riêng hoặc tệp nhật ký tùy kiến trúc triển khai. Lược đồ hình sao hiện tại chỉ mô tả dữ liệu phục vụ phân tích, không bắt buộc phải chứa bảng nhật ký vận hành.

## 6. Bảng truy vết yêu cầu

| FR | User Story | Use Case | MoSCoW |
|---|---|---|---|
| FR-01 | US-03 | UC-03 – Tính và gán phân khúc khách hàng | MUST |
| FR-02 | US-01 | UC-01 – Xem kết quả kiểm tra chất lượng dữ liệu | MUST |
| FR-03 | US-02 | UC-02 – Xem chỉ số mua hàng của khách | MUST |
| FR-04 | US-03 | UC-03 – Tính và gán phân khúc khách hàng | MUST |
| FR-05 | US-04 | UC-04 – Lọc danh sách khách theo phân khúc | SHOULD |
| FR-06 | US-05 | UC-05 – Xuất danh sách phân khúc | COULD |
| FR-07 | US-06 | UC-06 – Xem thống kê phân khúc | SHOULD |
| FR-08 | US-07 | UC-07 – Xem căn cứ gán phân khúc | SHOULD |
