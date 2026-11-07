
# Khởi tạo kho dữ liệu và Seed – Smart CRM

## 1. Kiến trúc lưu trữ

Smart CRM sử dụng kho dữ liệu dạng CSV, không sử dụng hệ quản trị cơ sở dữ liệu SQL.

Vì vậy, dự án không sử dụng SQL Migration hoặc SQL Seed. Việc khởi tạo kho được thực hiện thông qua pipeline ETL.

## 2. Cấu trúc dữ liệu

Thư mục dữ liệu:

- `data/raw/`: dữ liệu nguồn ban đầu.
- `data/processed/`: dữ liệu đã xử lý.
- `data/warehouse/`: dữ liệu kho phục vụ Dashboard.

Các file kho dữ liệu:

- `dim_customer.csv`: chiều khách hàng.
- `dim_period.csv`: chiều thời gian.
- `fact_order.csv`: bảng dữ liệu đơn hàng.
- `data_quality_issues.csv`: các vấn đề chất lượng dữ liệu.
- `customer_duplicate_candidates.csv`: các hồ sơ khách hàng nghi trùng.

## 3. Khởi tạo kho dữ liệu

Tại thư mục gốc dự án, thực hiện:

```powershell
python src/etl/load_warehouse.py
```

Pipeline thực hiện:

1. Đọc dữ liệu nguồn.
2. Chuẩn hóa và kiểm tra dữ liệu.
3. Xác định khách hàng và đơn hàng.
4. Tạo các bảng dữ liệu kho.
5. Ghi dữ liệu vào `data/warehouse/`.
6. Sinh báo cáo nạp kho tại `docs/bao-cao-nap-kho.md`.

## 4. Cơ chế cập nhật kho

Pipeline sử dụng cơ chế ghi snapshot.

Khi chạy lại ETL, dữ liệu kho được tạo lại từ dữ liệu nguồn hiện có, không cộng dồn vào snapshot trước đó.

## 5. Seed dữ liệu kiểm thử

Dự án sử dụng dữ liệu seed được khởi tạo trực tiếp trong các test bằng `pandas.DataFrame`, không sử dụng seed SQL.

### 5.1. Dữ liệu seed

Trong `tests/test_load_warehouse.py`, phương thức `setUp()` tạo dữ liệu mẫu gồm:

- 2 khách hàng có mã hồ sơ hợp lệ.
- 2 đơn hàng có ngày và giá trị hợp lệ.
- 1 đơn hàng có số điện thoại chưa tồn tại trong danh sách khách hàng để kiểm tra trường hợp `UNKNOWN`.

Dữ liệu được ghi vào thư mục tạm thời của từng test, không ảnh hưởng dữ liệu kho thật.

### 5.2. Kiểm thử seed và nạp kho

Các trường hợp kiểm thử:

- Nạp dữ liệu đơn hàng và xác định khách hàng chưa liên kết.
- Nạp kho nhiều lần không tạo bản ghi trùng.
- Từ chối đơn hàng trùng khóa nghiệp vụ.
- Từ chối dữ liệu thiếu cột bắt buộc.
- Từ chối khách hàng thiếu mã hồ sơ.
- Từ chối khách hàng trùng mã hồ sơ.
- Ghi nhận đơn hàng có ngày không hợp lệ.
- Ghi nhận đơn hàng có giá trị không hợp lệ.

### 5.3. Kiểm tra kết quả

Chạy toàn bộ kiểm thử:

```powershell
python -m pytest tests -q
```

Kết quả mong đợi: toàn bộ test PASS.

### 5.4. Kết luận

Seed dữ liệu được thực hiện bằng dữ liệu mẫu trong test, phục vụ kiểm chứng pipeline ETL và chất lượng dữ liệu. Kho dữ liệu thực tế được khởi tạo bằng pipeline `src/etl/load_warehouse.py` theo cơ chế snapshot, không sử dụng SQL Migration.
## 6. Kiểm tra sau khởi tạo

Sau khi chạy ETL:

- Kiểm tra các file kho dữ liệu được tạo.
- Kiểm tra báo cáo nạp kho.
- Kiểm tra số lượng bản ghi và vấn đề chất lượng dữ liệu.
- Chạy kiểm thử tự động:

```powershell
python -m pytest tests -q
```

## 7. Giới hạn dữ liệu

Dữ liệu nguồn chưa xác minh trạng thái đơn hoàn tất và chưa có mã khách hàng thống nhất.

Vì vậy, kết quả phân khúc QT-12 hiện chỉ mang tính phân tích sơ bộ, chưa được công bố là phân khúc chính thức.
