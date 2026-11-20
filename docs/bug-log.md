# BUG LOG – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 2.0

## 1. Danh sách lỗi đã xử lý

| Bug ID | Mô tả lỗi | Severity | Nguyên nhân | Cách xử lý | Trạng thái | Commit liên kết |
|---|---|---|---|---|---|---|
| BUG-01 | Hồ sơ khách hàng thiếu hoặc trùng `record_id` vẫn có thể được đưa vào kho dữ liệu | Major | Phiên bản ETL trước chưa kiểm tra ID rỗng và ID trùng trước khi tạo dimension khách hàng | Bổ sung kiểm tra `record_id` rỗng và trùng; dừng nạp dữ liệu khi phát hiện vi phạm | Đã sửa; có kiểm thử hồi quy | `e7def4a` |
| BUG-02 | Đơn hàng có ngày không hợp lệ không được ghi nhận đầy đủ trong báo cáo chất lượng dữ liệu | Major | Giá trị ngày không hợp lệ được chuyển thành `NaT`, nhưng chưa được ghi thành một issue riêng | Bổ sung kiểm tra ngày và ghi nhận mã lỗi `INVALID_ORDER_DATE` vào bảng `data_quality_issues.csv` | Đã sửa; có kiểm thử hồi quy | `e7def4a` |
| BUG-03 | Đơn hàng có thành tiền không hợp lệ chưa được chuẩn hóa và truy vết đầy đủ | Major | Giá trị thành tiền từ nguồn chưa được chuyển đổi và kiểm tra kiểu số trước khi đưa vào kho | Sử dụng `pd.to_numeric(errors="coerce")`; ghi nhận `INVALID_ORDER_AMOUNT` khi giá trị không hợp lệ | Đã sửa; có kiểm thử hồi quy | `e7def4a` |
| BUG-04 | Một số định dạng ngày tháng không được phân tích chính xác khi nạp dữ liệu vào kho | Major | Chuyển đổi ngày chưa chỉ định chế độ xử lý nhiều định dạng và thứ tự ngày/tháng | Bổ sung `format="mixed"`, `dayfirst=True` và `errors="coerce"` trong `pd.to_datetime()` | Đã sửa; có commit khắc phục | `289f6e1` |

## 2. Kiểm thử xác nhận

Các trường hợp được kiểm thử trong `tests/test_load_warehouse.py`:

- `test_missing_customer_record_id_is_rejected`: xác nhận từ chối hồ sơ thiếu mã.
- `test_duplicate_customer_record_id_is_rejected`: xác nhận từ chối mã hồ sơ trùng.
- `test_invalid_order_date_is_recorded_as_issue`: xác nhận ghi nhận ngày không hợp lệ.
- `test_invalid_order_amount_is_recorded_as_issue`: xác nhận ghi nhận thành tiền không hợp lệ.

Kiểm thử toàn bộ dự án được thực hiện bằng lệnh:

```bash
python -m pytest tests -v
```

Kết quả lần chạy gần nhất: **30 passed, 0 failed**.

## 3. Các hạn chế dữ liệu nguồn chưa được khắc phục hoàn toàn

| Vấn đề | Nguyên nhân | Biện pháp hiện tại |
|---|---|---|
| Không xác định được khách hàng của một số đơn hàng | Số điện thoại không khớp hoặc không đủ điều kiện ánh xạ duy nhất | Gán `UNKNOWN`, ghi nhận vấn đề chất lượng dữ liệu |
| Chưa xác minh được trạng thái hoàn tất của đơn hàng | Dữ liệu nguồn chưa cung cấp trạng thái đáng tin cậy | Đặt trạng thái `UNKNOWN`, chặn công bố phân khúc |

Hai vấn đề trên là hạn chế của dữ liệu nguồn, chưa thể xem là lỗi đã khắc phục hoàn toàn. Hệ thống tiếp tục ghi nhận và kiểm soát để tránh đưa dữ liệu chưa xác minh vào kết quả phân khúc.

## 4. Kết luận

Các lỗi liên quan đến kiểm tra khóa khách hàng, ghi nhận dữ liệu ngày/thành tiền không hợp lệ và phân tích định dạng ngày đã được xử lý bằng các thay đổi mã nguồn có commit liên kết và kiểm thử xác nhận.

Các hạn chế phụ thuộc vào dữ liệu nguồn được ghi nhận riêng, không tự động giả định hoặc tự sửa dữ liệu khi chưa có căn cứ.
