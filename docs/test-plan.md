# TEST PLAN – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 1.1

## 1. Mục tiêu kiểm thử

Kiểm tra tính đúng đắn, độ tin cậy và khả năng tái lập của quy trình xử lý dữ liệu khách hàng, đơn hàng, chuẩn hóa dữ liệu, nạp dữ liệu vào kho và phân khúc khách hàng theo QT-12.

## 2. Phạm vi kiểm thử

- Chuẩn hóa ngày tháng và thành tiền.
- Kiểm tra dữ liệu đầu vào hợp lệ, thiếu và sai định dạng.
- Kiểm tra dữ liệu trùng lặp và khóa nghiệp vụ.
- Kiểm tra xử lý đơn hàng hợp lệ và không hợp lệ.
- Kiểm tra khách hàng chưa xác định.
- Kiểm tra khả năng nạp dữ liệu nhiều lần.
- Kiểm tra tính nhất quán dữ liệu kho.
- Kiểm tra logic phân khúc khách hàng theo QT-12.
- Kiểm tra thứ tự ưu tiên phân khúc và tính toàn vẹn dữ liệu đầu vào.

## 3. Môi trường kiểm thử

| Thành phần | Mô tả |
|---|---|
| Hệ điều hành | Windows |
| Ngôn ngữ | Python 3.13.15 |
| Framework | pytest 9.1.1 |
| Công cụ | VS Code, Git |
| Môi trường | `.venv` |
| Dữ liệu | Bộ dữ liệu kiểm thử độc lập |
| Phương pháp | Kiểm thử tự động |

## 4. Danh sách test case

### 4.1. Kiểm thử nạp kho dữ liệu

| ID | Test case | Kết quả mong đợi |
|---|---|---|
| TC-01 | Từ chối khóa nghiệp vụ trùng | Không nạp bản ghi trùng |
| TC-02 | Từ chối mã bản ghi khách hàng trùng | Không tạo khách hàng trùng |
| TC-03 | Ghi nhận đơn hàng có thành tiền không hợp lệ | Ghi nhận lỗi dữ liệu |
| TC-04 | Ghi nhận đơn hàng có ngày không hợp lệ | Ghi nhận lỗi dữ liệu |
| TC-05 | Nạp đơn hàng và đánh dấu khách hàng chưa xác định | Đơn hàng được ghi nhận, khách hàng UNKNOWN |
| TC-06 | Từ chối thiếu mã bản ghi khách hàng | Không nạp dữ liệu không đủ điều kiện |
| TC-07 | Từ chối thiếu cột bắt buộc | Báo lỗi thiếu cột |
| TC-08 | Nạp kho lần hai | Không phát sinh bản ghi trùng |

### 4.2. Kiểm thử chuẩn hóa dữ liệu

| ID | Test case | Kết quả mong đợi |
|---|---|---|
| TC-09 | Chuẩn hóa ngày theo định dạng khác | Chuẩn hóa ngày chính xác |
| TC-10 | Ngày rỗng | Trả về giá trị thiếu |
| TC-11 | Ngày không hợp lệ | Trả về giá trị thiếu |
| TC-12 | Ngày hợp lệ | Chuẩn hóa đúng ngày |
| TC-13 | Thành tiền có khoảng trắng | Chuẩn hóa thành số đúng |
| TC-14 | Thành tiền có dấu phân cách hàng nghìn | Chuyển thành số đúng |
| TC-15 | Thành tiền rỗng | Trả về giá trị thiếu |
| TC-16 | Thành tiền không hợp lệ | Trả về giá trị thiếu |
| TC-17 | Thành tiền âm | Trả về giá trị thiếu |
| TC-18 | Thành tiền hợp lệ | Chuyển thành số đúng |
| TC-19 | Thành tiền dạng tiền Việt | Chuyển thành số đúng |
| TC-20 | Thành tiền bằng 0 | Giữ giá trị 0 hợp lệ |

### 4.3. Kiểm thử xử lý đơn hàng

| ID | Test case | Kết quả mong đợi |
|---|---|---|
| TC-21 | Tách đơn hàng hợp lệ và bị từ chối | Phân loại đúng, không mất bản ghi |

### 4.4. Kiểm thử phân khúc khách hàng QT-12

| ID | Test case | Kết quả mong đợi |
|---|---|---|
| TC-22 | VIP theo ngưỡng chi tiêu | Gán VIP đúng |
| TC-23 | VIP theo số lượng đơn | Gán VIP đúng |
| TC-24 | Thường xuyên theo ngưỡng chi tiêu | Gán Thường xuyên đúng |
| TC-25 | Thường xuyên theo số lượng đơn | Gán Thường xuyên đúng |
| TC-26 | Khách hàng mới | Gán Mới đúng |
| TC-27 | Khách hàng ngủ đông | Gán Ngủ đông đúng |
| TC-28 | VIP ưu tiên cao hơn Thường xuyên | Gán VIP đúng |
| TC-29 | Thường xuyên ưu tiên cao hơn Mới | Gán Thường xuyên đúng |
| TC-30 | Hàm phân khúc không thay đổi DataFrame đầu vào | Dữ liệu ban đầu không bị thay đổi |

## 5. Phân loại kiểm thử

| Nhóm kiểm thử | Nội dung |
|---|---|
| Luồng đúng | Chuẩn hóa dữ liệu hợp lệ, nạp dữ liệu, xử lý đơn hàng và phân khúc hợp lệ |
| Kiểm thử biên | Thành tiền bằng 0; ngưỡng chi tiêu và số lượng đơn theo QT-12 |
| Dữ liệu sai | Ngày không hợp lệ, thành tiền không hợp lệ, thiếu cột bắt buộc |
| Bảo mật / chất lượng dữ liệu | Khóa trùng, mã khách hàng chưa xác định, dữ liệu thiếu và giao dịch lỗi |
| Tái lập | Nạp dữ liệu nhiều lần không tạo bản ghi trùng; kiểm tra tính toàn vẹn DataFrame đầu vào |

## 6. Phương pháp thực thi

Chạy toàn bộ test bằng lệnh:

```powershell
python -m pytest tests -v
```

Kiểm tra danh sách test:

```powershell
python -m pytest tests --collect-only -q
```

Ghi nhận kết quả thực tế, số test PASS, FAIL và lưu ảnh chụp kết quả tại `docs/screenshots/`.

## 7. Tiêu chí đánh giá

- **PASS:** Kết quả thực tế đúng với kết quả mong đợi.
- **FAIL:** Kết quả thực tế khác kết quả mong đợi.
- **BLOCKED:** Không thể thực hiện do thiếu điều kiện hoặc môi trường.

## 8. Kết quả kiểm thử hiện tại

- Tổng số test case: 30.
- Kết quả kiểm thử gần nhất: 30/30 PASS.
- Chi tiết kết quả và minh chứng được ghi nhận trong `docs/test-report.md`.

