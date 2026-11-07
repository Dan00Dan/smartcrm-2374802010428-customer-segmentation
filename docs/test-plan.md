# TEST PLAN – SMART CRM

**Dự án:** Smart CRM – L1: Tính và gán phân khúc khách hàng  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 1.0

## 1. Mục tiêu kiểm thử

Kiểm tra tính đúng đắn, độ tin cậy và khả năng tái lập của quy trình xử lý dữ liệu khách hàng, đơn hàng, chuẩn hóa dữ liệu, nạp dữ liệu vào kho và kiểm tra chất lượng dữ liệu.

## 2. Phạm vi kiểm thử

- Chuẩn hóa ngày tháng và thành tiền.
- Kiểm tra dữ liệu đầu vào hợp lệ, thiếu và sai định dạng.
- Kiểm tra dữ liệu trùng lặp và khóa nghiệp vụ.
- Kiểm tra xử lý đơn hàng hợp lệ và không hợp lệ.
- Kiểm tra khách hàng chưa xác định.
- Kiểm tra khả năng nạp dữ liệu nhiều lần.
- Kiểm tra tính nhất quán của dữ liệu kho.
- Kiểm tra các trường hợp biên và khả năng chạy lại kiểm thử.

## 3. Môi trường kiểm thử

| Thành phần | Môi trường |
|---|---|
| Hệ điều hành | Windows |
| Ngôn ngữ | Python 3.13.15 |
| Framework | pytest 9.1.1 |
| Công cụ | VS Code, Git |
| Dữ liệu | Bộ dữ liệu kiểm thử độc lập |
| Phương pháp | Kiểm thử tự động và kiểm thử thủ công |

## 4. Danh sách test case hiện có

| ID | Nội dung kiểm thử | Kết quả mong đợi |
|---|---|---|
| TC-01 | Ngày hợp lệ dạng dd/mm/yyyy | Chuẩn hóa đúng |
| TC-02 | Ngày hợp lệ dạng yyyy-mm-dd | Giữ đúng ngày |
| TC-03 | Ngày rỗng | Trả về giá trị thiếu |
| TC-04 | Ngày sai định dạng | Trả về giá trị thiếu |
| TC-05 | Thành tiền hợp lệ | Chuyển thành số đúng |
| TC-06 | Thành tiền có khoảng trắng | Chuẩn hóa đúng |
| TC-07 | Thành tiền dạng tiền Việt | Chuyển thành số đúng |
| TC-08 | Thành tiền có dấu phân cách hàng nghìn | Chuyển thành số đúng |
| TC-09 | Thành tiền rỗng | Trả về giá trị thiếu |
| TC-10 | Thành tiền không hợp lệ | Trả về giá trị thiếu |
| TC-11 | Thành tiền âm | Trả về giá trị thiếu |
| TC-12 | Tách đơn hợp lệ và bị từ chối | Phân loại đúng, không mất bản ghi |
| TC-13 | Nạp đơn và khách hàng chưa xác định | Đơn vẫn được ghi nhận, khách được đánh dấu UNKNOWN |
| TC-14 | Nạp kho lần hai | Không phát sinh bản ghi trùng |
| TC-15 | Khóa nghiệp vụ trùng | Từ chối nạp dữ liệu |
| TC-16 | Thiếu cột bắt buộc | Từ chối nạp dữ liệu |
| TC-17 | Thiếu mã khách hàng | Từ chối nạp dữ liệu |
| TC-18 | Mã khách hàng trùng | Từ chối nạp dữ liệu |
| TC-19 | Ngày đơn hàng sai | Ghi nhận vào bảng lỗi dữ liệu |
| TC-20 | Thành tiền đơn hàng sai | Ghi nhận vào bảng lỗi dữ liệu |

## 5. Phân loại kiểm thử

| Nhóm kiểm thử | Test case |
|---|---|
| Luồng đúng | TC-01, TC-02, TC-05, TC-06, TC-07, TC-08, TC-12 |
| Kiểm thử biên | Cần bổ sung |
| Dữ liệu sai | TC-03, TC-04, TC-09, TC-10, TC-11, TC-16 |
| Bảo mật / chất lượng dữ liệu | TC-13, TC-15, TC-17, TC-18, TC-19, TC-20 |
| Tái lập | TC-14 và kiểm thử chạy lại toàn bộ |

## 6. Phương pháp thực thi

Chạy toàn bộ test bằng lệnh:

```powershell
python -m pytest tests -v
```

Ghi nhận kết quả thực tế, số test PASS, FAIL và lưu ảnh chụp kết quả tại `docs/screenshots/`.

## 7. Tiêu chí đánh giá

- PASS: Kết quả thực tế đúng với kết quả mong đợi.
- FAIL: Kết quả thực tế khác kết quả mong đợi.
- BLOCKED: Không thể thực hiện do thiếu điều kiện hoặc môi trường.
- Không ghi nhận PASS nếu chưa thực hiện kiểm thử thực tế.
- Sau khi sửa lỗi, phải chạy lại toàn bộ test để kiểm tra hồi quy.
- Mỗi test case phải có kết quả và minh chứng tương ứng.
