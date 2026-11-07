# TEST REPORT – SMART CRM

**Dự án:** Smart CRM – L1 Hồ sơ khách hàng và phân khúc  
**Người thực hiện:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Ngày kiểm thử:** 07/11/2026

## 1. Môi trường kiểm thử

- Hệ điều hành: Windows
- Python: 3.13.15
- Framework: pytest 9.1.1
- Môi trường: `.venv`
- Lệnh kiểm thử: `python -m pytest tests -v`

## 2. Kết quả kiểm thử

| Nội dung | Kết quả |
|---|---:|
| Tổng số test case đã chạy | 30 |
| PASS | 30 |
| FAIL | 0 |
| BLOCKED | 0 |

**Kết luận:** Toàn bộ 30 test case đã chạy thành công tại thời điểm kiểm thử.

## 3. Phân loại kiểm thử

| Loại kiểm thử | Nội dung |
|---|---|
| Luồng đúng | Chuẩn hóa dữ liệu, nạp dữ liệu, phân khúc hợp lệ |
| Kiểm thử biên | Số tiền bằng 0; ngưỡng VIP 30 triệu, 8 đơn; ngưỡng Thường xuyên 10 triệu, 3 đơn |
| Dữ liệu sai | Ngày không hợp lệ, số tiền không hợp lệ, thiếu cột, thiếu mã khách hàng |
| Chất lượng dữ liệu | Trùng khóa, mã khách hàng không xác định, giao dịch lỗi |
| Tái lập | Nạp dữ liệu nhiều lần không tạo bản ghi trùng; chạy lại toàn bộ test suite |

## 4. Kiểm thử phân khúc QT-12

Đã kiểm thử các trường hợp:

- VIP theo ngưỡng chi tiêu.
- VIP theo số lượng đơn.
- Thường xuyên theo ngưỡng chi tiêu.
- Thường xuyên theo số lượng đơn.
- Khách mới.
- Khách ngủ đông.
- Ưu tiên VIP cao hơn Thường xuyên.
- Ưu tiên Thường xuyên cao hơn Mới.
- Hàm phân khúc không làm thay đổi DataFrame đầu vào.

Kết quả: **9/9 PASS**.

## 5. Bằng chứng kiểm thử

- [TEST-01-all-tests-pass.png](screenshots/TEST-01-all-tests-pass.png): Kết quả toàn bộ 30 test PASS.
- [TEST-02-QT12-pass.png](screenshots/TEST-02-QT12-pass.png): Kết quả 9 test QT-12 PASS.

## 6. Kết luận

Bộ kiểm thử hiện tại đạt 30/30 PASS. Các chức năng được kiểm thử gồm chuẩn hóa dữ liệu, nạp dữ liệu kho, xử lý đơn hàng và phân khúc khách hàng QT-12.

Kết quả phản ánh trạng thái chương trình tại thời điểm thực hiện kiểm thử ngày 07/11/2026.