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

## 4. Quy tắc tính toán và cửa sổ thời gian

Chỉ sử dụng các đơn hoàn tất hợp lệ để tính chỉ số mua hàng. Nguồn dữ liệu hiện có chưa có mã khách hàng chung giữa các nguồn và chưa có trạng thái đơn hàng. Vì vậy, trước khi tính phân khúc, phải xác nhận mã đơn nghiệp vụ, ánh xạ đơn hàng–khách hàng và quy tắc nhận diện đơn hoàn tất. Nếu chưa xác nhận được các thông tin này, hệ thống phải chặn tính phân khúc.

Ngày chốt D là thời điểm 00:00 ngày đầu tiên của tháng kế tiếp theo múi giờ `Asia/Ho_Chi_Minh`.

- **Cửa sổ 12 tháng:** `[D − 12 tháng lịch, D)`, dùng để tính tổng chi tiêu và số đơn hoàn tất hợp lệ trong 12 tháng.
- **Cửa sổ 90 ngày:** `[D − 90 ngày, D)`, dùng để tính số đơn hoàn tất hợp lệ trong 90 ngày gần nhất.
- **Nguyên tắc đếm đơn:** Mỗi mã đơn nghiệp vụ chỉ được tính một lần. Nếu dữ liệu có nhiều dòng hàng thuộc cùng một đơn, tổng tiền của đơn chỉ được cộng một lần.
- **Nguyên tắc thời gian:** Chỉ tính các giao dịch nằm trong cửa sổ tương ứng; thời điểm D không thuộc cửa sổ tính toán.
---

## 5. Kiểm tra tính toàn vẹn và chất lượng dữ liệu

- **Tính duy nhất:** Mỗi `customer_id` trong danh mục khách hàng chuẩn phải xác định duy nhất một hồ sơ khách hàng đã được xác nhận. Không tự gộp hồ sơ chỉ dựa trên tên hoặc số điện thoại.
- **Tính hợp lệ của định danh:** Các trường định danh bắt buộc như `customer_id` và `order_id` không được rỗng đối với bản ghi tham gia tính toán.
- **Toàn vẹn tham chiếu:** Mỗi đơn hàng hợp lệ được sử dụng để tính toán phải ánh xạ được đến một `customer_id` đã xác nhận.
- **Kiểm tra dữ liệu giao dịch:** Ngày mua hàng phải hợp lệ; tổng tiền phải có định dạng hợp lệ và không âm. Bản ghi lỗi được ghi nhận để đối soát, không âm thầm đưa vào phép tính.
- **Xử lý lỗi chặn:** Nếu không xác định được khách hàng bị ảnh hưởng bởi lỗi quan trọng, hệ thống phải chặn công bố kết quả mới. Nếu xác định được khách hàng bị ảnh hưởng, ghi nhận `DATA_ERROR` cho khách đó và không gán phân khúc.
- **Bảo toàn kết quả:** Chỉ thay thế kết quả đã công bố khi toàn bộ kết quả mới được lưu thành công. Nếu lưu thất bại, giữ nguyên kết quả trước đó.
---

## 6. Mô hình Lưu trữ và Liên kết Kho Dữ liệu

### 6.1. Các bảng lưu trữ chính

- `dim_customer`: Lưu danh mục khách hàng chuẩn, gồm `customer_key`, `customer_id` và `full_name`. Mỗi `customer_id` phải xác định duy nhất một hồ sơ khách hàng đã được xác nhận.
- `dim_period`: Lưu kỳ phân tích, gồm `period_key`, tháng phân tích, ngày chốt `D`, thời điểm bắt đầu và kết thúc của các cửa sổ tính toán.
- `fact_customer_segment`: Lưu kết quả phân khúc theo từng khách hàng và kỳ phân tích, gồm `customer_key`, `period_key`, tổng chi tiêu 12 tháng, số đơn 12 tháng, số đơn 90 ngày, phân khúc, trạng thái xử lý, nguyên nhân và phiên bản quy tắc áp dụng.

### 6.2. Khóa và quan hệ giữa các bảng

- Khóa chính của `dim_customer` là `customer_key`; `customer_id` là mã nghiệp vụ duy nhất đã được xác nhận.
- Khóa chính của `dim_period` là `period_key`.
- Khóa chính của `fact_customer_segment` là tổ hợp `(customer_key, period_key)`, bảo đảm mỗi khách hàng có tối đa một kết quả trong mỗi kỳ phân tích.
- `fact_customer_segment.customer_key` tham chiếu đến `dim_customer.customer_key`.
- `fact_customer_segment.period_key` tham chiếu đến `dim_period.period_key`.

### 6.3. Lưu trữ nhật ký chạy và lỗi

Thông tin vận hành được lưu riêng với các bảng kho dữ liệu phân tích, trong bảng hoặc tệp nhật ký chạy (`ops_log`). Nhật ký gồm mã lần chạy, kỳ phân tích, thời điểm bắt đầu/kết thúc, trạng thái chạy và thông tin lỗi nếu có.

Các bản ghi có lỗi dữ liệu cần được ghi nhận để đối soát. Nếu xác định được khách hàng bị ảnh hưởng, ghi nhận trạng thái `DATA_ERROR` và không gán phân khúc cho khách đó. Nếu không xác định được khách hàng bị ảnh hưởng bởi lỗi quan trọng, hệ thống phải chặn công bố toàn bộ kết quả mới.

### 6.4. Nguyên tắc công bố và truy xuất kết quả

- Chỉ công bố kết quả mới khi toàn bộ kết quả của kỳ phân tích được lưu thành công.
- Nếu lưu kết quả mới thất bại, giữ nguyên kết quả đã công bố trước đó.
- Khi xuất CSV, lấy mã khách hàng từ `dim_customer`, kỳ phân tích từ `dim_period` và các chỉ số, phân khúc, trạng thái cùng nguyên nhân từ `fact_customer_segment`.
- Mỗi kết quả phải gắn với kỳ phân tích và phiên bản quy tắc để hỗ trợ kiểm tra, đối chiếu và tái lập kết quả.
