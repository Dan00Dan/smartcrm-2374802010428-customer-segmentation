# TEST REPORT – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Người thực hiện:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Ngày kiểm thử gần nhất:** 22/11/2026  
**Phiên bản:** 1.5

## 1. Môi trường kiểm thử

| Thành phần | Mô tả |
|---|---|
| Hệ điều hành | Windows |
| Python | 3.13.15 |
| Framework kiểm thử | pytest 9.1.1 |
| Môi trường thực thi | `.venv` |
| Công cụ | VS Code, Git |
| Lệnh kiểm thử | `python -m pytest -q` |

## 2. Kết quả kiểm thử tổng thể

| Nội dung | Kết quả |
|---|---:|
| Tổng số kiểm thử tự động | 37 |
| PASS | 37 |
| FAIL | 0 |
| BLOCKED | 0 |
| Thời gian thực thi gần nhất | 1.39 giây |

**Kết luận:** Toàn bộ 37 kiểm thử tự động đạt trạng thái PASS trong lần chạy gần nhất ngày 22/11/2026.

## 3. Phạm vi và kết quả kiểm thử

Bảng dưới đây tổng hợp các nhóm chức năng đã được kiểm tra trong quá trình phát triển BT3.

| STT | Nhóm kiểm thử | Nội dung kiểm tra | Kết quả ghi nhận |
|---|---|---|---|
| 1 | Data Loading | Đọc và tiếp nhận dữ liệu khách hàng, đơn hàng | PASS |
| 2 | Data Normalization | Chuẩn hóa dữ liệu và định dạng đầu vào | PASS |
| 3 | Data Deduplication | Phát hiện và xử lý bản ghi trùng | PASS |
| 4 | Data Quality | Kiểm tra dữ liệu thiếu, sai định dạng và bất thường | PASS |
| 5 | Date Processing | Xử lý nhiều định dạng ngày và ngày không hợp lệ | PASS |
| 6 | Data Warehouse | Kiểm tra quá trình nạp và kết quả lưu trữ | PASS |
| 7 | Data Pseudonymization | Kiểm tra cơ chế ẩn danh dữ liệu khách hàng | PASS |
| 8 | Customer Segmentation | Kiểm tra phân khúc khách hàng theo QT-12 | PASS |
| 9 | Regression Testing | Kiểm tra lại các lỗi đã được khắc phục | PASS |

**Lưu ý:** Bảng này tổng hợp phạm vi và kết quả theo nhóm chức năng, không phải bảng ánh xạ từng hàm kiểm thử với từng Test Case. Tổng số 37 là số lượng test tự động do pytest thu thập và thực thi.

## 4. Phân loại kiểm thử

| Test Type | Nội dung kiểm thử |
|---|---|
| Functional Testing | Kiểm tra chức năng chuẩn hóa dữ liệu, xử lý đơn hàng và phân khúc khách hàng |
| Boundary Testing | Kiểm tra các giá trị tại ngưỡng điều kiện và ranh giới phân khúc |
| Negative Testing | Kiểm tra dữ liệu sai định dạng, thiếu cột và giá trị không hợp lệ |
| Data Quality Testing | Kiểm tra dữ liệu trùng, dữ liệu thiếu và dữ liệu bất thường |
| Regression Testing | Kiểm tra lại chức năng sau khi sửa lỗi |

## 5. Kết quả kiểm thử phân khúc QT-12

Các nội dung kiểm thử quy tắc phân khúc khách hàng QT-12 bao gồm:

1. VIP theo ngưỡng chi tiêu.
2. VIP theo số lượng đơn hàng.
3. Thường xuyên theo ngưỡng chi tiêu.
4. Thường xuyên theo số lượng đơn hàng.
5. Khách hàng mới.
6. Khách hàng ngủ đông.
7. Kiểm tra mức ưu tiên VIP cao hơn Thường xuyên.
8. Kiểm tra mức ưu tiên Thường xuyên cao hơn Mới.
9. Kiểm tra hàm phân khúc không làm thay đổi DataFrame đầu vào.

**Kết quả ghi nhận: 9/9 PASS.**

Các trường hợp kiểm thử xác nhận việc phân loại khách hàng theo điều kiện và thứ tự ưu tiên được quy định trong QT-12.

## 6. Kiểm thử hồi quy và xử lý lỗi

Trong quá trình phát triển, hệ thống đã được kiểm tra và khắc phục một số vấn đề liên quan đến dữ liệu:

| Nội dung | Kết quả xử lý |
|---|---|
| Khóa nghiệp vụ trùng lặp | Đã bổ sung xử lý |
| Ngày đơn hàng không hợp lệ | Đã bổ sung xử lý |
| Thành tiền không hợp lệ | Đã bổ sung xử lý |
| Nhiều định dạng ngày trong cùng dữ liệu | Đã bổ sung kiểm thử hồi quy |
| Dữ liệu đầu vào bị thay đổi ngoài ý muốn | Đã kiểm tra bảo toàn DataFrame |

Chi tiết lỗi, nguyên nhân, cách khắc phục và commit liên quan được ghi trong `docs/bug-log.md`.

## 7. Bằng chứng kiểm thử

Các ảnh minh chứng được lưu tại thư mục `docs/screenshots/`.

| Tên ảnh | Nội dung minh chứng |
|---|---|
| `TEST-03-pytest-final.png` | Kết quả chạy toàn bộ Test Suite |
| `TEST-04-QT12-final.png` | Kết quả kiểm thử quy tắc phân khúc QT-12 |
| `TEST-01-all-tests-pass.png` | Minh chứng kết quả kiểm thử tự động |
| `TEST-02-QT12-pass.png` | Minh chứng kiểm thử QT-12 |

Các ảnh minh chứng cần được đối chiếu với kết quả thực thi thực tế và giữ đúng nội dung đã chụp.

## 8. Kết luận

Trong lần kiểm thử gần nhất ngày 22/11/2026, hệ thống Smart CRM đạt kết quả 37/37 kiểm thử tự động PASS, không có trường hợp FAIL hoặc BLOCKED. Thời gian thực thi được ghi nhận là 1.39 giây.

Các nội dung kiểm thử tập trung vào quá trình tiếp nhận và chuẩn hóa dữ liệu, kiểm tra chất lượng dữ liệu, xử lý đơn hàng, nạp dữ liệu vào Data Warehouse, bảo vệ thông tin khách hàng, phân khúc khách hàng theo QT-12 và kiểm thử hồi quy.

Kết quả này phản ánh trạng thái của bộ kiểm thử tự động tại thời điểm thực thi, không đồng nghĩa với việc toàn bộ chức năng hoặc các yêu cầu bảo mật của hệ thống đã được kiểm chứng trong môi trường production.