# TEST PLAN – SMART CRM

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Phiên bản:** 1.3  
**Ngày cập nhật:** 13/11/2026

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

## 4. Danh sách Test Case

### 4.1. Kiểm thử nạp kho dữ liệu

| ID | Test Case | Kết quả mong đợi |
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

| ID | Test Case | Kết quả mong đợi |
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

| ID | Test Case | Kết quả mong đợi |
|---|---|---|
| TC-21 | Tách đơn hàng hợp lệ và bị từ chối | Phân loại đúng, không mất bản ghi |

### 4.4. Kiểm thử phân khúc khách hàng QT-12

| ID | Test Case | Kết quả mong đợi |
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

| Nhóm kiểm thử | Nội dung | Test Case tiêu biểu |
|---|---|---|
| Functional | Kiểm tra luồng xử lý dữ liệu hợp lệ, nạp dữ liệu và phân khúc | TC-05, TC-12, TC-18, TC-22 |
| Boundary | Kiểm tra giá trị biên và ngưỡng phân khúc | TC-17, TC-20, TC-22, TC-23 |
| Negative | Kiểm tra dữ liệu sai định dạng, thiếu dữ liệu và dữ liệu không hợp lệ | TC-03, TC-04, TC-07, TC-11, TC-16 |
| Data Quality | Kiểm tra khóa trùng, khách hàng chưa xác định và dữ liệu thiếu | TC-01, TC-02, TC-05, TC-06 |
| Regression | Kiểm tra khả năng nạp lại dữ liệu và bảo toàn dữ liệu đầu vào | TC-08, TC-30 |

## 6. Phương pháp thực thi

### 6.1. Chạy toàn bộ Test Suite

```powershell
python -m pytest tests -v
```

### 6.2. Kiểm tra danh sách Test Case

```powershell
python -m pytest tests --collect-only -q
```

### 6.3. Ghi nhận kết quả

- Ghi nhận kết quả thực tế của từng Test Case.
- Đối chiếu kết quả thực tế với kết quả mong đợi.
- Tổng hợp số lượng PASS, FAIL và BLOCKED.
- Lưu ảnh chụp kết quả kiểm thử tại `docs/screenshots/`.
- Chi tiết kết quả thực thi được trình bày trong `docs/test-report.md`.

## 7. Tiêu chí đánh giá

| Trạng thái | Điều kiện |
|---|---|
| PASS | Kết quả thực tế đúng với kết quả mong đợi |
| FAIL | Kết quả thực tế khác kết quả mong đợi |
| BLOCKED | Không thể thực hiện do thiếu điều kiện hoặc môi trường |

## 8. Kết quả kiểm thử hiện tại

- Tổng số Test Case tự động: 30.
- Kết quả kiểm thử gần nhất: 30/30 PASS.
- Số Test Case FAIL: 0.
- Số Test Case BLOCKED: 0.
- Chi tiết kết quả và minh chứng được ghi nhận trong `docs/test-report.md`.
