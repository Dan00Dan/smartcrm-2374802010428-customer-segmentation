# Hệ thống phân khúc khách hàng theo dữ liệu mua hàng

**Sinh viên:** Trần Thị Như Quỳnh – 2374802010428 – Track Data Analyst  
**Học phần:** Chuyên đề Tốt nghiệp 1, HK1 2026–2027  
**Luồng nghiệp vụ:** L1 – Hồ sơ khách hàng và phân khúc

## 1. Mục tiêu

Xây dựng quy trình xử lý dữ liệu mua hàng, kiểm tra chất lượng, nạp dữ liệu vào kho và cung cấp dashboard để nhân viên Marketing theo dõi dữ liệu theo tháng.

Phân khúc khách hàng dự kiến tuân theo quy tắc QT-12: VIP, Thường xuyên, Mới và Ngủ đông. Kết quả phân khúc chỉ được công bố sau khi xác minh quy tắc liên kết khách hàng, trạng thái đơn hàng hợp lệ và các điều kiện nghiệp vụ liên quan.

## 2. Công nghệ sử dụng

- Python
- Pandas
- Streamlit
- Pytest
- CSV làm định dạng dữ liệu đầu vào và kho dữ liệu trong phạm vi hiện tại.

## 3. Yêu cầu môi trường

- Python tương thích với các thư viện trong `requirements.txt`.
- Git để tải mã nguồn.
- Hai bộ dữ liệu đầu vào theo cấu trúc dự án.

## 4. Cài đặt và chạy dự án

Mở PowerShell tại thư mục gốc của repository.

### Bước 1. Tạo môi trường ảo

```powershell
py -m venv .venv
```

Nếu môi trường `.venv` đã tồn tại thì không cần tạo lại.

### Bước 2. Kích hoạt môi trường ảo

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu môi trường `.venv` đã được kích hoạt thì bỏ qua bước này.

### Bước 3. Cài đặt thư viện

```powershell
python -m pip install -r requirements.txt
```

### Bước 4. Chuẩn bị dữ liệu đầu vào

Dự án sử dụng hai tệp dữ liệu:

- `data/raw/customers_raw.csv`
- `data/raw/orders_2024_2026.csv`

Hai tệp dữ liệu đầu vào không được đưa lên repository do có thể chứa thông tin cá nhân. Khi clone dự án sang máy hoặc thư mục mới, cần tự chuẩn bị dữ liệu được phép sử dụng và đặt đúng tên, đúng vị trí nêu trên.

Nếu chưa có dữ liệu đầu vào, hãy chuẩn bị dữ liệu trước khi chạy pipeline và ETL. Không tự ý tải dữ liệu khách hàng lên repository công khai.

### Bước 5. Chạy pipeline xử lý dữ liệu

```powershell
python -m src.pipeline
```

Pipeline đọc dữ liệu, thống kê chất lượng, chuẩn hóa ngày tháng và số tiền, phân loại dữ liệu hợp lệ hoặc bị từ chối, sau đó lưu kết quả theo cấu hình dự án.

Các kết quả chính:

- `data/processed/orders_normalized.csv`: dữ liệu đơn hàng sau xử lý theo các tiêu chí hiện tại.
- `data/processed/orders_reject.csv`: dữ liệu bị từ chối kèm lý do.
- `docs/bao-cao-chat-luong.md`: báo cáo chất lượng dữ liệu.

### Bước 6. Nạp dữ liệu vào kho

```powershell
python -m src.etl.load_warehouse
```

Các bảng kho được tạo trong `data/warehouse/`:

- `dim_customer.csv`: dữ liệu chiều khách hàng.
- `dim_period.csv`: dữ liệu chiều thời gian.
- `fact_order.csv`: dữ liệu đơn hàng.
- `data_quality_issues.csv`: các vấn đề chất lượng dữ liệu.

Báo cáo nạp kho được lưu tại `docs/bao-cao-nap-kho.md`.

### Bước 7. Chạy dashboard

```powershell
python -m streamlit run app.py
```

Mở địa chỉ sau trên trình duyệt:

`http://localhost:8501`

Dashboard hỗ trợ lọc tháng, xem thống kê tổng quan, theo dõi số đơn và tổng tiền ghi nhận theo tháng, xem chi tiết đơn hàng và cảnh báo chất lượng dữ liệu.

### Bước 8. Chạy kiểm thử

```powershell
python -m pytest -q
```

Kết quả kiểm thử gần nhất trong quá trình phát triển là **16 bài kiểm thử đạt yêu cầu**. Cần chạy lại lệnh trên để xác nhận kết quả tại thời điểm sử dụng.

## 5. Quy trình xử lý dữ liệu

1. Đọc và thống kê dữ liệu đầu vào.
2. Chuẩn hóa ngày tháng và số tiền.
3. Phân loại dữ liệu hợp lệ và dữ liệu bị từ chối.
4. Kiểm tra chất lượng và tính bảo toàn số dòng.
5. Nạp dữ liệu vào các bảng kho dạng CSV.
6. Kiểm tra khóa nghiệp vụ và ghi nhận bản ghi chưa xác định được khách hàng.
7. Hiển thị số liệu tổng hợp và cảnh báo trên dashboard.

## 6. Cấu trúc thư mục chính

- `app.py`: giao diện dashboard Streamlit.
- `data/raw/`: dữ liệu CSV đầu vào.
- `data/processed/`: dữ liệu sau xử lý và dữ liệu bị từ chối.
- `data/warehouse/`: các bảng kho dữ liệu được sinh ra khi chạy ETL.
- `src/extract/`: module đọc dữ liệu.
- `src/transform/`: module chuẩn hóa dữ liệu.
- `src/quality/`: module kiểm tra chất lượng.
- `src/load/`: module lưu dữ liệu và báo cáo.
- `src/etl/load_warehouse.py`: module nạp dữ liệu vào kho.
- `tests/`: các bài kiểm thử tự động.
- `docs/`: đặc tả, sơ đồ, báo cáo và ảnh minh chứng.
- `requirements.txt`: danh sách thư viện.
- `.gitignore`: danh sách file và thư mục không đưa lên GitHub.

## 7. Giới hạn dữ liệu hiện tại

Nguồn dữ liệu hiện tại chưa xác minh đầy đủ khóa liên kết giữa hồ sơ khách hàng và đơn hàng; đồng thời chưa có thông tin đủ tin cậy để xác định chắc chắn trạng thái đơn hàng hoàn tất.

Vì vậy:

- Đơn chưa xác định được khách hàng được gắn khóa kỹ thuật `UNKNOWN`.
- Trạng thái đơn hàng được ghi nhận là `UNKNOWN` khi nguồn chưa cung cấp thông tin xác thực.
- Các biểu đồ chỉ phản ánh bản ghi và số tiền được ghi nhận trong kho; không khẳng định tất cả đơn là đơn hoàn tất hoặc số tiền là doanh thu hợp lệ.
- Kết quả phân khúc khách hàng chưa được công bố cho đến khi các điều kiện dữ liệu và nghiệp vụ được xác minh.

## 8. Trạng thái công việc

### 8.1. Công việc đã hoàn thành

- [x] Xây dựng pipeline xử lý và kiểm tra chất lượng dữ liệu.
- [x] Bổ sung kiểm thử tự động cho pipeline.
- [x] Xây dựng module nạp dữ liệu vào kho CSV.
- [x] Bổ sung kiểm thử cho module nạp kho.
- [x] Xây dựng dashboard có bộ lọc tháng, thống kê tổng quan và biểu đồ.
- [x] Bổ sung cảnh báo về dữ liệu chưa xác định và trạng thái đơn hàng.
- [x] Cố định phiên bản thư viện trong `requirements.txt`.
- [x] Bổ sung hướng dẫn cài đặt, chạy chương trình và kiểm thử trong README.
- [x] Chạy kiểm thử tự động với kết quả gần nhất là 16 bài kiểm thử đạt yêu cầu.

### 8.2. Công việc đang tiếp tục hoàn thiện

- [ ] Xác minh quy tắc liên kết khách hàng giữa các nguồn dữ liệu.
- [ ] Xác minh điều kiện xác định đơn hàng hoàn tất.
- [ ] Hoàn thiện và xác minh kết quả phân khúc khách hàng theo QT-12.
- [ ] Kiểm thử quy trình cài đặt và chạy dự án trên môi trường độc lập.

## 9. Tài liệu liên quan

- `docs/srs.md`: đặc tả yêu cầu phần mềm.
- `docs/data-requirements.md`: yêu cầu dữ liệu.
- `docs/bao-cao-chat-luong.md`: báo cáo chất lượng dữ liệu.
- `docs/bao-cao-nap-kho.md`: báo cáo nạp kho.
- `docs/pipeline-result.png`: ảnh minh chứng chạy pipeline.
- `docs/dashboard-01.png.png` đến `docs/dashboard-04.png.png`: ảnh minh chứng dashboard.

## 10. Chạy pipeline tổng

Sau khi chuẩn bị dữ liệu đầu vào và kích hoạt môi trường ảo, chạy lệnh:

```powershell
python run_pipeline.py
```

Lệnh này lần lượt thực hiện:

1. Xử lý và kiểm tra chất lượng dữ liệu.
2. Nạp dữ liệu vào kho.

Nếu một bước thất bại, chương trình sẽ dừng và trả về mã lỗi của bước đó.

## 11. Bug Log và công khai sử dụng AI

- `docs/bug-log.md`: ghi nhận các vấn đề dữ liệu và cách xử lý.
- `docs/ai-disclosure.md`: khai báo việc sử dụng công cụ AI trong quá trình thực hiện dự án.
- `docs/thay-doi-thiet-ke.md`: ghi nhận các thay đổi thiết kế.