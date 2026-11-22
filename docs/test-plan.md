# TEST PLAN – SMART CRM

**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 1.5  
**Ngày cập nhật:** 22/11/2026

---

## 1. Mục tiêu kiểm thử

Tài liệu xác định phạm vi, phương pháp và các trường hợp kiểm thử cho hệ thống Smart CRM, tập trung vào các chức năng:

- Tiếp nhận và xử lý dữ liệu khách hàng, đơn hàng.
- Chuẩn hóa dữ liệu đầu vào và nạp dữ liệu vào Data Warehouse.
- Kiểm tra chất lượng dữ liệu (Data Quality).
- Xử lý dữ liệu ngày đơn hàng và các giá trị không hợp lệ.
- Ẩn danh thông tin khách hàng bằng HMAC-SHA256.
- Tính toán và phân khúc khách hàng theo quy tắc QT-12.
- Kiểm thử hồi quy sau khi sửa lỗi.

## 2. Phạm vi kiểm thử

### 2.1. Trong phạm vi

| STT | Chức năng | Nội dung kiểm thử |
|---|---|---|
| 1 | Data Loading | Đọc và nạp dữ liệu khách hàng, đơn hàng |
| 2 | Data Normalization | Chuẩn hóa dữ liệu, kiểu dữ liệu và định dạng |
| 3 | Data Deduplication | Phát hiện và xử lý dữ liệu trùng lặp |
| 4 | Data Quality | Kiểm tra dữ liệu thiếu, sai định dạng và bất thường |
| 5 | Date Processing | Chuẩn hóa ngày đơn hàng với nhiều định dạng |
| 6 | Data Warehouse | Kiểm tra kết quả nạp dữ liệu |
| 7 | Data Pseudonymization | Ẩn danh dữ liệu bằng HMAC-SHA256 |
| 8 | Customer Segmentation | Phân khúc khách hàng theo QT-12 |
| 9 | Regression Testing | Kiểm tra lại các lỗi đã được sửa |

### 2.2. Ngoài phạm vi

- Kiểm thử tải và hiệu năng trên môi trường production.
- Kiểm thử tích hợp với hệ thống bên thứ ba chưa được triển khai.
- Kiểm thử phân quyền người dùng ở môi trường production.
- Kiểm thử bảo mật chuyên sâu bởi đơn vị độc lập.

## 3. Phương pháp kiểm thử

| Phương pháp | Mục đích |
|---|---|
| Functional Testing | Kiểm tra chức năng xử lý dữ liệu |
| Boundary Testing | Kiểm tra các giá trị ở ngưỡng điều kiện |
| Negative Testing | Kiểm tra dữ liệu sai hoặc không hợp lệ |
| Data Quality Testing | Đánh giá chất lượng dữ liệu |
| Regression Testing | Đảm bảo chức năng cũ vẫn hoạt động sau khi sửa lỗi |

## 4. Môi trường kiểm thử

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python 3.13 |
| Xử lý dữ liệu | Pandas, NumPy |
| Kiểm thử tự động | Pytest |
| Giao diện | Streamlit |
| Container | Docker, Docker Compose |
| Hệ điều hành | Windows |
| Quản lý mã nguồn | Git, GitHub |

## 5. Danh sách Test Case

### 5.1. Data Loading và Data Warehouse

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-01 | Đọc dữ liệu khách hàng đầu vào | Dữ liệu được đọc thành công |
| TC-02 | Kiểm tra mã khách hàng bị thiếu hoặc trùng | Phát hiện và xử lý theo quy tắc |
| TC-03 | Đọc dữ liệu đơn hàng | Dữ liệu đơn hàng được tiếp nhận |
| TC-04 | Kiểm tra ngày đơn hàng không hợp lệ | Phát hiện giá trị ngày không hợp lệ |
| TC-05 | Kiểm tra giá trị đơn hàng âm | Dữ liệu không hợp lệ được xử lý |
| TC-06 | Kiểm tra bản ghi trùng lặp | Bản ghi trùng được phát hiện |
| TC-07 | Nạp dữ liệu vào Data Warehouse | Dữ liệu được nạp theo cấu trúc |
| TC-08 | Kiểm tra dữ liệu sau khi nạp | Kết quả được lưu và có thể truy xuất |

### 5.2. Data Normalization

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-09 | Chuẩn hóa định dạng ngày tháng | Ngày tháng được đưa về định dạng thống nhất |
| TC-10 | Chuẩn hóa dữ liệu văn bản | Dữ liệu được xử lý theo quy tắc |
| TC-11 | Xử lý giá trị NULL | Giá trị thiếu được xử lý phù hợp |
| TC-12 | Kiểm tra kiểu dữ liệu | Các cột có kiểu dữ liệu phù hợp |
| TC-13 | Kiểm tra dữ liệu số | Giá trị số được chuyển đổi chính xác |
| TC-14 | Kiểm tra bản ghi trùng sau chuẩn hóa | Không giữ lại bản ghi trùng theo quy tắc |
| TC-15 | Kiểm tra dữ liệu không hợp lệ | Dữ liệu lỗi được phát hiện |
| TC-16 | Kiểm tra tính nhất quán dữ liệu | Dữ liệu sau chuẩn hóa thống nhất |
| TC-17 | Kiểm tra dữ liệu khách hàng | Thông tin khách hàng được xử lý đúng |
| TC-18 | Kiểm tra dữ liệu đơn hàng | Thông tin đơn hàng được xử lý đúng |
| TC-19 | Kiểm tra dữ liệu sau ETL | Dữ liệu đầu ra đáp ứng yêu cầu |
| TC-20 | Kiểm tra kết quả tổng hợp | Kết quả tổng hợp được tạo chính xác |

### 5.3. Xử lý đơn hàng và ngày tháng

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-21 | Xử lý đơn hàng có ngày tháng hỗn hợp | Các định dạng ngày được xử lý đúng |
| TC-22 | Xử lý ngày tháng không thể chuyển đổi | Giá trị lỗi được phát hiện, không làm sai dữ liệu hợp lệ |

### 5.4. Data Quality và bảo mật dữ liệu

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-23 | Kiểm tra tỷ lệ dữ liệu thiếu | Thống kê được giá trị thiếu |
| TC-24 | Kiểm tra chất lượng theo từng cột | Kết quả đánh giá được tổng hợp |
| TC-25 | Kiểm tra dữ liệu bất thường | Các giá trị bất thường được nhận diện |
| TC-26 | Kiểm tra ẩn danh thông tin khách hàng | Thông tin định danh được thay thế bằng mã giả danh |
| TC-27 | Kiểm tra tính ổn định của HMAC | Cùng đầu vào và secret cho cùng kết quả |
| TC-28 | Kiểm tra secret không hợp lệ hoặc bị thiếu | Hệ thống từ chối tiếp tục xử lý khi thiếu điều kiện bảo mật |

### 5.5. Customer Segmentation – QT-12

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-29 | Khách hàng đạt điều kiện VIP theo doanh thu | Được phân khúc VIP |
| TC-30 | Khách hàng đạt điều kiện VIP theo số đơn | Được phân khúc VIP |
| TC-31 | Khách hàng đạt điều kiện Thường xuyên | Được phân khúc Thường xuyên |
| TC-32 | Khách hàng có đúng một đơn hợp lệ trong 90 ngày | Được phân khúc Mới nếu không thuộc nhóm ưu tiên cao hơn |
| TC-33 | Khách hàng không đạt các điều kiện phía trên | Được phân khúc Ngủ đông |
| TC-34 | Khách hàng đồng thời thỏa nhiều điều kiện | Áp dụng thứ tự ưu tiên VIP → Thường xuyên → Mới → Ngủ đông |
| TC-35 | Kiểm tra ranh giới doanh thu và số đơn | Phân khúc đúng tại ngưỡng QT-12 |
| TC-36 | Kiểm tra thời gian tính toán phân khúc | Sử dụng khoảng thời gian và quy tắc ngày đã quy định |

### 5.6. Regression Testing

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-37 | Kiểm tra hồi quy sau khi sửa lỗi xử lý ngày hỗn hợp | Dữ liệu ngày hợp lệ vẫn được xử lý chính xác |

## 6. Thực thi kiểm thử

Sử dụng Pytest để chạy kiểm thử tự động.

**Chạy toàn bộ kiểm thử:**

```bash
python -m pytest tests -v
```

**Chạy kiểm thử và hiển thị kết quả ngắn gọn:**

```bash
python -m pytest -q
```

**Kiểm tra danh sách test được thu thập:**

```bash
python -m pytest tests --collect-only -q
```

## 7. Tiêu chí đánh giá

| Trạng thái | Ý nghĩa |
|---|---|
| PASS | Kết quả thực tế đáp ứng kết quả mong đợi |
| FAIL | Kết quả thực tế không đáp ứng yêu cầu |
| BLOCKED | Không thể thực hiện do thiếu điều kiện hoặc môi trường |

Một Test Case chỉ được đánh dấu PASS khi đã có kết quả thực thi hoặc bằng chứng kiểm thử phù hợp.

## 8. Kết quả kiểm thử

Theo lần chạy kiểm thử tự động gần nhất được ghi nhận:

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số test tự động | 37 |
| PASS | 37 |
| FAIL | 0 |
| Thời gian chạy gần nhất được ghi nhận | 1.40 giây |

**Lưu ý:** 37 là số lượng bài kiểm thử tự động được Pytest thu thập và thực thi, không phải số lượng Test Case nghiệp vụ ban đầu. Danh sách Test Case trong tài liệu mô tả phạm vi và mục tiêu kiểm thử; trạng thái thực tế cần đối chiếu với kết quả chạy và báo cáo kiểm thử.

Kết quả chi tiết được trình bày trong `docs/test-report.md`.

## 9. Tài liệu liên quan

- `docs/test-report.md`: Báo cáo kết quả kiểm thử.
- `docs/bug-log.md`: Nhật ký lỗi và quá trình khắc phục.
- `docs/bao-cao-chat-luong.md`: Báo cáo chất lượng dữ liệu.
- `docs/bao-cao-nap-kho.md`: Báo cáo nạp dữ liệu vào Data Warehouse.
- `docs/SECURITY-CHECKLIST.md`: Danh sách kiểm tra bảo mật.
- `tests/`: Mã nguồn kiểm thử tự động.