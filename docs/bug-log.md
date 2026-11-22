# BUG LOG – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 2.2  
**Ngày cập nhật:** 22/11/2026

## 1. Danh sách lỗi đã xử lý

| Bug ID | Mô tả lỗi | Severity | Nguyên nhân | Cách xử lý | Test Case liên kết | Commit liên kết | Trạng thái |
|---|---|---|---|---|---|---|---|
| BUG-01 | Hồ sơ khách hàng thiếu hoặc trùng `record_id` vẫn có thể được đưa vào kho dữ liệu | Major | ETL trước đó chưa kiểm tra ID rỗng và ID trùng trước khi tạo dimension khách hàng | Bổ sung kiểm tra `record_id` rỗng và trùng; dừng nạp dữ liệu khi phát hiện vi phạm | TC-02 | `e7def4a` | Đã sửa, có kiểm thử hồi quy |
| BUG-02 | Đơn hàng có ngày không hợp lệ không được ghi nhận đầy đủ trong báo cáo chất lượng dữ liệu | Major | Giá trị ngày không hợp lệ được chuyển thành `NaT`, nhưng chưa được ghi thành issue riêng | Bổ sung kiểm tra ngày và ghi nhận mã lỗi `INVALID_ORDER_DATE` vào `data_quality_issues.csv` | TC-04 | `e7def4a` | Đã sửa, có kiểm thử hồi quy |
| BUG-03 | Đơn hàng có thành tiền không hợp lệ chưa được chuẩn hóa và truy vết đầy đủ | Major | Giá trị thành tiền chưa được chuyển đổi và kiểm tra kiểu số trước khi đưa vào kho | Sử dụng `pd.to_numeric(errors="coerce")`; ghi nhận `INVALID_ORDER_AMOUNT` khi giá trị không hợp lệ | TC-05 | `e7def4a` | Đã sửa, có kiểm thử hồi quy |
| BUG-04 | Một số định dạng ngày tháng không được phân tích chính xác khi nạp dữ liệu vào kho | Major | Chuyển đổi ngày chưa xử lý tốt nhiều định dạng và thứ tự ngày/tháng | Bổ sung `format="mixed"`, `dayfirst=True` và `errors="coerce"` trong `pd.to_datetime()` | TC-21 | `289f6e1` | Đã sửa, có kiểm thử hồi quy |

## 2. Kiểm thử xác nhận

Các trường hợp kiểm thử hồi quy được thực hiện trong `tests/test_load_warehouse.py`:

| Bug liên quan | Hàm kiểm thử | Nội dung xác nhận |
|---|---|---|
| BUG-01 | `test_missing_customer_record_id_is_rejected` | Từ chối hồ sơ thiếu mã |
| BUG-01 | `test_duplicate_customer_record_id_is_rejected` | Từ chối mã hồ sơ trùng |
| BUG-02 | `test_invalid_order_date_is_recorded_as_issue` | Ghi nhận ngày không hợp lệ |
| BUG-03 | `test_invalid_order_amount_is_recorded_as_issue` | Ghi nhận thành tiền không hợp lệ |
| BUG-04 | `test_mixed_order_date_formats_are_parsed_correctly` | Phân tích chính xác các định dạng ngày khác nhau |

**Lệnh kiểm thử toàn bộ dự án:**

```bash
python -m pytest tests -v
```

**Kết quả lần chạy gần nhất:**

- Tổng số kiểm thử: 37
- PASS: 37
- FAIL: 0
- Thời gian: 1.34 giây

Riêng nhóm kiểm thử nạp dữ liệu vào kho có kết quả được ghi nhận là 9 passed, 0 failed.

## 3. Các hạn chế dữ liệu nguồn chưa được khắc phục hoàn toàn

| Vấn đề | Nguyên nhân | Biện pháp hiện tại |
|---|---|---|
| Không xác định được khách hàng của một số đơn hàng | Số điện thoại không khớp hoặc không đủ điều kiện ánh xạ duy nhất | Gán `UNKNOWN`, ghi nhận vấn đề chất lượng dữ liệu |
| Chưa xác minh được trạng thái hoàn tất của đơn hàng | Dữ liệu nguồn chưa cung cấp trạng thái đáng tin cậy | Đặt trạng thái `UNKNOWN`, chặn công bố phân khúc |

Hai vấn đề trên là hạn chế của dữ liệu nguồn, chưa thể xem là lỗi đã khắc phục hoàn toàn. Hệ thống tiếp tục ghi nhận và kiểm soát để tránh đưa dữ liệu chưa xác minh vào kết quả phân khúc.

## 4. Kết luận

Bốn lỗi chính liên quan đến kiểm tra khóa khách hàng, ghi nhận ngày không hợp lệ, xử lý thành tiền và phân tích nhiều định dạng ngày đã được xử lý.

Mỗi lỗi có thông tin về nguyên nhân, cách khắc phục, Test Case xác nhận và commit liên kết nhằm bảo đảm khả năng truy vết trong quá trình phát triển.

Kết quả kiểm thử tự động gần nhất đạt 37/37 PASS, không có trường hợp FAIL.

Các hạn chế phụ thuộc vào dữ liệu nguồn được ghi nhận riêng, không tự động giả định hoặc tự sửa dữ liệu khi chưa có căn cứ.