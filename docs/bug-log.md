# BUG LOG – SMART CRM

| ID | Vấn đề | Nguyên nhân/Phân tích | Cách xử lý | Trạng thái |
|---|---|---|---|---|
| BUG-01 | Không xác định được khách hàng cho một số đơn hàng | Dữ liệu nguồn chưa đủ thông tin để ánh xạ chính xác đơn hàng với hồ sơ khách hàng | Gán khóa khách hàng UNKNOWN, ghi nhận vấn đề chất lượng dữ liệu; không tự ghép theo tên | Đã xử lý an toàn, chờ xác minh dữ liệu |
| BUG-02 | Chưa xác minh được trạng thái hoàn thành của đơn hàng | Dữ liệu nguồn chưa có thông tin trạng thái đơn hàng đáng tin cậy | Đánh dấu nguồn chưa đủ điều kiện và chặn công bố phân khúc | Đang chờ bổ sung dữ liệu |
| BUG-03 | Một số đơn hàng có dữ liệu ngày hoặc thành tiền không hợp lệ | Giá trị nguồn thiếu hoặc không đúng định dạng yêu cầu | Tách đơn hàng không hợp lệ sang danh sách bị từ chối và ghi rõ lý do | Đã xử lý trong pipeline |
