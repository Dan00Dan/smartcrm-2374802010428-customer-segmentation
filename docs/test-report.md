# TEST REPORT – SMART CRM

**Dự án:** Smart CRM – L1 Hồ sơ khách hàng và phân khúc  
**Người thực hiện:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Ngày kiểm thử:** 13/11/2026

## 1. Môi trường kiểm thử

| Thành phần | Mô tả |
|---|---|
| Hệ điều hành | Windows |
| Python | 3.13.15 |
| Framework | pytest 9.1.1 |
| Môi trường | `.venv` |
| Lệnh kiểm thử | `python -m pytest tests -v` |

## 2. Kết quả kiểm thử tổng thể

| Nội dung | Kết quả |
|---|---:|
| Tổng số test case | 30 |
| PASS | 30 |
| FAIL | 0 |
| BLOCKED | 0 |
| Thời gian thực thi | 2.04 giây |

**Kết luận:** Toàn bộ 30 test case đạt PASS tại lần kiểm thử ngày 13/11/2026.

## 3. Bảng test case đại diện

| ID | Test Type | Test Objective | Preconditions | Test Data | Test Steps | Expected Result | Actual Result / Status |
|---|---|---|---|---|---|---|
| TC-01 | Data Quality | Phát hiện khóa nghiệp vụ trùng | Có dữ liệu đơn hàng | Business key trùng | Nạp dữ liệu | Không nạp bản ghi trùng | Đúng / PASS |
| TC-03 | Negative | Ghi nhận thành tiền không hợp lệ | Có dữ liệu đơn hàng | Amount sai định dạng | Nạp dữ liệu | Ghi nhận lỗi dữ liệu | Đúng / PASS |
| TC-05 | Data Quality | Xử lý khách hàng chưa xác định | Có đơn hàng chưa ánh xạ khách hàng | Customer UNKNOWN | Nạp dữ liệu | Gán UNKNOWN, ghi nhận đơn hàng | Đúng / PASS |
| TC-07 | Negative | Kiểm tra thiếu cột bắt buộc | Có dữ liệu đầu vào | Thiếu required column | Nạp dữ liệu | Báo lỗi thiếu cột | Đúng / PASS |
| TC-08 | Regression | Kiểm tra nạp kho lặp | Kho đã được nạp lần đầu | Cùng bộ dữ liệu | Nạp lần hai | Không tạo bản ghi trùng | Đúng / PASS |
| TC-09 | Functional | Chuẩn hóa nhiều định dạng ngày | Có hàm chuẩn hóa ngày | Ngày định dạng khác | Gọi hàm chuẩn hóa | Ngày được chuẩn hóa chính xác | Đúng / PASS |
| TC-11 | Negative | Xử lý ngày không hợp lệ | Có hàm chuẩn hóa ngày | Ngày sai định dạng | Gọi hàm chuẩn hóa | Trả về giá trị thiếu | Đúng / PASS |
| TC-14 | Functional | Chuẩn hóa tiền có dấu phân cách | Có hàm chuẩn hóa tiền | Amount có dấu phân cách hàng nghìn | Gọi hàm chuẩn hóa | Chuyển thành số đúng | Đúng / PASS |
| TC-20 | Boundary | Kiểm tra thành tiền bằng 0 | Có hàm chuẩn hóa tiền | Amount = 0 | Gọi hàm chuẩn hóa | Giữ giá trị 0 hợp lệ | Đúng / PASS |
| TC-21 | Functional | Phân loại đơn hợp lệ và bị từ chối | Có dữ liệu đơn hàng | Bộ dữ liệu hợp lệ và lỗi | Chạy xử lý đơn hàng | Phân loại đúng, không mất bản ghi | Đúng / PASS |
| TC-22 | Boundary | Phân khúc VIP theo chi tiêu | Có hàm QT-12 | Chi tiêu đạt ngưỡng VIP | Gọi hàm phân khúc | Gán VIP đúng | Đúng / PASS |
| TC-30 | Regression | Bảo toàn DataFrame đầu vào | Có dữ liệu phân khúc | DataFrame ban đầu | Chạy phân khúc | DataFrame gốc không thay đổi | Đúng / PASS |

## 4. Phân loại kiểm thử

| Loại | Nội dung |
|---|---|
| Functional | Chuẩn hóa dữ liệu, xử lý đơn hàng và phân khúc |
| Boundary | Thành tiền bằng 0 và ngưỡng phân khúc |
| Negative | Ngày, thành tiền sai và thiếu cột |
| Data Quality | Khóa trùng, khách hàng UNKNOWN |
| Regression | Nạp lại dữ liệu và bảo toàn DataFrame |

## 5. Kiểm thử phân khúc QT-12

Các trường hợp đã kiểm thử:
- VIP theo ngưỡng chi tiêu.
- VIP theo số lượng đơn.
- Thường xuyên theo ngưỡng chi tiêu.
- Thường xuyên theo số lượng đơn.
- Khách hàng mới.
- Khách hàng ngủ đông.
- Ưu tiên VIP cao hơn Thường xuyên.
- Ưu tiên Thường xuyên cao hơn Mới.
- Hàm phân khúc không làm thay đổi DataFrame đầu vào.

**Kết quả: 9/9 PASS.**

## 6. Bằng chứng kiểm thử

- `docs/screenshots/TEST-01-all-tests-pass.png`: kết quả toàn bộ test suite.
- `docs/screenshots/TEST-02-QT12-pass.png`: kết quả test QT-12.

## 7. Kết luận

Lần kiểm thử ngày 13/11/2026 đạt 30/30 PASS, không có FAIL hoặc BLOCKED. Các chức năng được kiểm tra gồm chuẩn hóa dữ liệu, nạp kho, xử lý đơn hàng, chất lượng dữ liệu và phân khúc khách hàng QT-12.

Kết quả phản ánh trạng thái chương trình tại thời điểm thực hiện kiểm thử.
