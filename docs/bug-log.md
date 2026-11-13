
# BUG LOG – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 1.3  
**Ngày cập nhật:** 13/11/2026

## 1. Danh sách lỗi

| Bug ID | Mô tả lỗi | Severity | Nguyên nhân | Cách xử lý | Trạng thái | Commit liên kết |
|---|---|---|---|---|---|---|
| BUG-01 | Không xác định được khách hàng cho một số đơn hàng | Major | Dữ liệu nguồn chưa đủ thông tin để ánh xạ chính xác đơn hàng với hồ sơ khách hàng | Gán khóa khách hàng `UNKNOWN`, ghi nhận vấn đề chất lượng dữ liệu; không tự ghép theo tên | Đã xử lý an toàn; chờ xác minh dữ liệu nguồn | N/A – Vấn đề dữ liệu nguồn |
| BUG-02 | Chưa xác minh được trạng thái hoàn thành của đơn hàng | Major | Dữ liệu nguồn chưa có thông tin trạng thái đơn hàng đáng tin cậy | Đánh dấu nguồn chưa đủ điều kiện và chặn công bố phân khúc | Đang chờ bổ sung hoặc xác minh dữ liệu | N/A – Vấn đề dữ liệu nguồn |
| BUG-03 | Một số đơn hàng có dữ liệu ngày hoặc thành tiền không hợp lệ | Minor | Giá trị nguồn bị thiếu hoặc không đúng định dạng yêu cầu | Tách đơn hàng không hợp lệ sang danh sách bị từ chối và ghi rõ lý do | Đã xử lý trong pipeline | N/A – Xử lý bằng pipeline |
| BUG-04 | Lỗi xử lý cột ngày khi nạp dữ liệu vào kho | Major | Module nạp kho tham chiếu `order_date` trước khi chuẩn hóa dữ liệu ngày từ cột nguồn `ngay` | Chuẩn hóa dữ liệu ngày bằng `pd.to_datetime()`, sử dụng `format="mixed"`, `dayfirst=True` và `errors="coerce"` | Đã sửa; bộ kiểm thử hiện tại đạt 30/30 PASS | `289f6e1` – Fix warehouse order date parsing |

## 2. Quy ước Severity

| Severity | Ý nghĩa |
|---|---|
| Critical | Lỗi nghiêm trọng khiến hệ thống không thể sử dụng hoặc gây mất dữ liệu nghiêm trọng |
| Major | Lỗi ảnh hưởng đáng kể đến quy trình hoặc kết quả nghiệp vụ |
| Minor | Lỗi phạm vi nhỏ, có cơ chế xử lý an toàn hoặc ít ảnh hưởng đến kết quả |

## 3. Ghi chú

- Các vấn đề dữ liệu chưa xác minh không được xem là đã khắc phục hoàn toàn chỉ vì pipeline xử lý an toàn.
- BUG-01 và BUG-02 vẫn cần bổ sung hoặc xác minh dữ liệu nguồn.
- BUG-03 được xử lý bằng cơ chế kiểm tra và phân loại dữ liệu không hợp lệ.
- BUG-04 đã được sửa và kiểm tra lại bằng bộ kiểm thử tự động.
- Commit liên kết được ghi nhận khi xác định được commit trực tiếp xử lý lỗi.
- Các vấn đề dữ liệu nguồn không có commit sửa dữ liệu được ghi là `N/A`.
