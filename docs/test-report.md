# TEST REPORT – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Người thực hiện:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Ngày kiểm thử:** 13/11/2026  
**Phiên bản:** 1.3

## 1. Môi trường kiểm thử

| Thành phần | Mô tả |
|---|---|
| Hệ điều hành | Windows |
| Python | 3.13.15 |
| Framework kiểm thử | pytest 9.1.1 |
| Môi trường thực thi | `.venv` |
| Công cụ | VS Code, Git |
| Lệnh kiểm thử | `python -m pytest tests -v` |

## 2. Kết quả kiểm thử tổng thể

| Nội dung | Kết quả |
|---|---:|
| Tổng số Test Case tự động | 30 |
| PASS | 30 |
| FAIL | 0 |
| BLOCKED | 0 |
| Thời gian thực thi | 1.07 giây |

**Kết luận:** Toàn bộ 30 Test Case tự động đạt trạng thái PASS trong lần kiểm thử ngày 13/11/2026.

## 3. Bảng Test Case đại diện

Bảng dưới đây trình bày 12 Test Case đại diện cho các chức năng chính, bao gồm kiểm thử chức năng, kiểm thử dữ liệu không hợp lệ, kiểm thử biên, chất lượng dữ liệu và kiểm thử hồi quy.

| ID | Test Type | Test Objective | Preconditions | Test Data | Test Steps | Expected Result | Actual Result / Status |
|---|---|---|---|---|---|---|---|
| TC-01 | Data Quality | Phát hiện khóa nghiệp vụ trùng | Có dữ liệu đơn hàng | Business key trùng | Nạp dữ liệu | Không nạp bản ghi trùng | Đúng / PASS |
| TC-03 | Negative | Ghi nhận thành tiền không hợp lệ | Có dữ liệu đơn hàng | Amount sai định dạng | Nạp dữ liệu | Ghi nhận lỗi dữ liệu | Đúng / PASS |
| TC-05 | Data Quality | Xử lý khách hàng chưa xác định | Có đơn hàng chưa ánh xạ khách hàng | Customer UNKNOWN | Nạp dữ liệu | Gán UNKNOWN và ghi nhận đơn hàng | Đúng / PASS |
| TC-07 | Negative | Kiểm tra thiếu cột bắt buộc | Có dữ liệu đầu vào | Thiếu required column | Nạp dữ liệu | Báo lỗi thiếu cột | Đúng / PASS |
| TC-08 | Regression | Kiểm tra nạp kho lặp | Kho đã được nạp lần đầu | Cùng bộ dữ liệu | Nạp lần hai | Không tạo bản ghi trùng | Đúng / PASS |
| TC-09 | Functional | Chuẩn hóa nhiều định dạng ngày | Có hàm chuẩn hóa ngày | Ngày có định dạng khác nhau | Gọi hàm chuẩn hóa | Ngày được chuẩn hóa chính xác | Đúng / PASS |
| TC-11 | Negative | Xử lý ngày không hợp lệ | Có hàm chuẩn hóa ngày | Ngày sai định dạng | Gọi hàm chuẩn hóa | Trả về giá trị thiếu | Đúng / PASS |
| TC-14 | Functional | Chuẩn hóa tiền có dấu phân cách | Có hàm chuẩn hóa tiền | Amount có dấu phân cách hàng nghìn | Gọi hàm chuẩn hóa | Chuyển thành số đúng | Đúng / PASS |
| TC-20 | Boundary | Kiểm tra thành tiền bằng 0 | Có hàm chuẩn hóa tiền | Amount = 0 | Gọi hàm chuẩn hóa | Giữ giá trị 0 hợp lệ | Đúng / PASS |
| TC-21 | Functional | Phân loại đơn hợp lệ và bị từ chối | Có dữ liệu đơn hàng | Bộ dữ liệu hợp lệ và lỗi | Chạy xử lý đơn hàng | Phân loại đúng, không mất bản ghi | Đúng / PASS |
| TC-22 | Boundary | Phân khúc VIP theo chi tiêu | Có hàm QT-12 | Chi tiêu đạt ngưỡng VIP | Gọi hàm phân khúc | Gán VIP đúng | Đúng / PASS |
| TC-30 | Regression | Bảo toàn DataFrame đầu vào | Có dữ liệu phân khúc | DataFrame ban đầu | Chạy phân khúc | DataFrame gốc không thay đổi | Đúng / PASS |

## 4. Phân loại kiểm thử

| Test Type | Nội dung kiểm thử |
|---|---|
| Functional | Chuẩn hóa dữ liệu, xử lý đơn hàng và phân khúc khách hàng |
| Boundary | Thành tiền bằng 0 và các ngưỡng phân khúc |
| Negative | Ngày, thành tiền sai định dạng và thiếu cột bắt buộc |
| Data Quality | Khóa nghiệp vụ trùng, khách hàng UNKNOWN và lỗi dữ liệu |
| Regression | Nạp dữ liệu lần hai và bảo toàn DataFrame đầu vào |

## 5. Kết quả kiểm thử phân khúc QT-12

Các trường hợp kiểm thử quy tắc phân khúc khách hàng QT-12 bao gồm:

1. VIP theo ngưỡng chi tiêu.
2. VIP theo số lượng đơn hàng.
3. Thường xuyên theo ngưỡng chi tiêu.
4. Thường xuyên theo số lượng đơn hàng.
5. Khách hàng mới.
6. Khách hàng ngủ đông.
7. Kiểm tra mức ưu tiên VIP cao hơn Thường xuyên.
8. Kiểm tra mức ưu tiên Thường xuyên cao hơn Mới.
9. Kiểm tra hàm phân khúc không làm thay đổi DataFrame đầu vào.

**Kết quả: 9/9 PASS.**

Các trường hợp kiểm thử xác nhận việc phân loại khách hàng theo các điều kiện và thứ tự ưu tiên được quy định trong QT-12.

## 6. Bằng chứng kiểm thử

Các ảnh minh chứng được lưu tại thư mục `docs/screenshots/`.

| Tên ảnh | Nội dung minh chứng |
|---|---|
| `TEST-03-pytest-final.png` | Kết quả chạy toàn bộ Test Suite |
| `TEST-04-QT12-final.png` | Kết quả kiểm thử quy tắc phân khúc QT-12 |

Các ảnh trên ghi nhận kết quả thực thi kiểm thử tại thời điểm lập báo cáo.

## 7. Kết luận

Trong lần kiểm thử ngày 13/11/2026, hệ thống đạt kết quả 30/30 Test Case PASS, không có trường hợp FAIL hoặc BLOCKED. Thời gian thực thi toàn bộ Test Suite là 1.07 giây.

Các nội dung được kiểm thử bao gồm chuẩn hóa dữ liệu đầu vào, nạp dữ liệu vào kho dữ liệu, xử lý và phân loại đơn hàng, kiểm tra chất lượng dữ liệu và phân khúc khách hàng theo quy tắc QT-12.

Kết quả kiểm thử phản ánh trạng thái chương trình tại thời điểm thực hiện và là cơ sở đánh giá các chức năng thuộc phạm vi kiểm thử của dự án Smart CRM trong BT3.