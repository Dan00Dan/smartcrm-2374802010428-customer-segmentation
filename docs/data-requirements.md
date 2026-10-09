# Tài liệu Đặc tả Dữ liệu (Data Requirements Specification)

## 1. Giới thiệu & Phạm vi dữ liệu
Tài liệu này đặc tả cấu trúc, kiểu dữ liệu chuẩn, hiện trạng chất lượng dữ liệu nguồn và các quy tắc kiểm tra tính toàn vẹn phục vụ bài toán phân khúc khách hàng (BT1).

---

## 2. Nguồn dữ liệu hiện có và Đặc tả Kiểu dữ liệu

### 2.1. Đánh giá nguồn dữ liệu thô
- Nguồn bảng `customers`: Chứa định danh và thông tin khách hàng (`record_id`, `ho_ten`, ...).
- Nguồn bảng `orders`: Chứa nhật ký giao dịch (`order_id`, `ma_don`, `ngay`, `thanh_tien`, ...).

### 2.2. Kiểu dữ liệu chuẩn dùng xử lý

| Trường chuẩn | Kiểu dữ liệu | Nguồn / cách xác định |
|---|---|---|
| customer_id | VARCHAR(100) | Giữ mã customers.record_id sau khi kiểm tra tính duy nhất; mã khách của đơn lấy từ ánh xạ đã xác nhận |
| full_name | VARCHAR(255) | customers.ho_ten |
| order_id | VARCHAR(100) | Chọn orders.order_id hoặc ma_don sau khi xác nhận mã đơn nghiệp vụ |
| order_date | TIMESTAMP | Chuyển từ orders.ngay, thống nhất giờ Việt Nam |
| total_amount | DECIMAL(18,0) | Chuyển từ orders.thanh_tien; VND, không âm |
| status | VARCHAR(20) | Cần nguồn bổ sung hoặc quy tắc nhận diện được xác nhận; không tự coi mọi đơn là hoàn tất |

> **Lưu ý:** Tỷ lệ thiếu phản ánh ô rỗng, không phản ánh đầy đủ lỗi định dạng, khóa trùng hoặc tính đúng đắn của ánh xạ.

---

## 3. Tiêu chuẩn Làm sạch và Xử lý Dữ liệu
- **Chuẩn hóa chuỗi ký tự:** Loại bỏ khoảng trắng thừa đầu/cuối, chuẩn hóa mã hóa UTF-8 đối với các trường tên và địa chỉ.
- **Xử lý giá trị rỗng/lỗi:**
  - Không cho phép null ở các trường định danh (`customer_id`, `order_id`).
  - Giao dịch có `total_amount` âm hoặc không hợp lệ sẽ bị cô lập để đối soát.
- **Xử lý thời gian:** Thống nhất toàn bộ mốc thời gian về múi giờ Việt Nam (`Asia/Ho_Chi_Minh`).

---

## 4. Quy tắc Tính toán và Cửa sổ Thời gian

Chỉ tính từ các đơn hoàn tất hợp lệ. Nguồn hiện có chưa có mã khách chung và trạng thái đơn; phải xác nhận ánh xạ đơn–khách, mã đơn nghiệp vụ và cách nhận diện đơn hoàn tất trước khi tính. Nếu chưa xác nhận được thì chặn tính phân khúc.

Ngày chốt D là 00:00 ngày đầu tháng kế tiếp theo múi giờ Asia/Ho_Chi_Minh. Cửa sổ 12 tháng là [D−12 tháng lịch, D); cửa sổ 90 ngày là [D−90 ngày, D).

- **Định nghĩa các cửa sổ dữ liệu:**
  - $D$: Thời điểm mốc tính toán (00:00:00 ngày mùng 1 tháng $M+1$).
  - Cửa sổ 12 tháng: $[D - 12\text{ tháng}, D)$ phục vụ tính tổng chi tiêu ($M$) và tần suất ($F$).
  - Cửa sổ 90 ngày: $[D - 90\text{ ngày}, D)$ phục vụ tính tính năng động/gần đây ($R$).

---

## 5. Kiểm tra Tính toàn vẹn và Chất lượng Dữ liệu
- **Tính duy nhất:** `customer_id` phải là duy nhất trên toàn tập khách hàng hợp lệ.
- **Toàn vẹn tham chiếu:** Mọi đơn hàng hợp lệ tham gia tính toán bắt buộc phải ánh xạ được tới một `customer_id` xác định.
- **Xử lý lỗi chặn:** Trường hợp phát hiện bất thường nghiêm trọng trong dữ liệu đầu vào hoặc không xác định được danh sách khách hàng bị ảnh hưởng, toàn bộ luồng công bố phải được đưa vào trạng thái chặn (circuit breaker).

---

## 6. Mô hình Lưu trữ và Liên kết Kho Dữ liệu

### Liên kết với kho dữ liệu

- `dim_customer`: lưu mã khách và tên khách.
- `dim_period`: lưu kỳ phân tích và các mốc cửa sổ thời gian.
- `fact_customer_segment`: lưu chỉ số, phân khúc, trạng thái, nguyên nhân, phiên bản quy tắc và thời điểm xử lý.
- Khóa chính của bảng fact là `(customer_key, period_key)`.
- Khi xuất CSV, lấy `customer_id` từ `dim_customer`, `period` từ `dim_period` và các chỉ số từ bảng fact.
- Nếu không xác định được khách bị ảnh hưởng bởi lỗi, chặn công bố toàn bộ kết quả mới.