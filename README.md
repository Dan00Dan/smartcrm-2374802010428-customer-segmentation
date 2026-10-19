# Hệ thống phân khúc khách hàng theo dữ liệu mua hàng

**Sinh viên:** Trần Thị Như Quỳnh – 2374802010428 – Track DA  
**Học phần:** Chuyên đề Tốt nghiệp 1, HK1 2026–2027  
**Luồng nghiệp vụ:** L1 – Hồ sơ khách hàng & phân khúc

## 1. Mục tiêu

Hỗ trợ nhân viên Marketing phân khúc khách hàng thành VIP, Thường xuyên, Mới và Ngủ đông theo quy tắc QT-12.

Người phân tích dữ liệu kiểm tra chất lượng dữ liệu đầu vào. Hệ thống định hướng tính toán chỉ số mua hàng, hiển thị phân khúc, hỗ trợ lọc, thống kê và xuất kết quả.

## 2. Yêu cầu môi trường

- Python 3.11 trở lên.
- Sử dụng môi trường ảo `.venv`.
- Thư viện xử lý dữ liệu: Pandas; các thư viện khác xem trong `requirements.txt`.
- Cơ sở dữ liệu dự kiến: PostgreSQL.
- Biến môi trường: tham khảo `.env.example`.
- Mở các sơ đồ `.drawio` bằng diagrams.net.

## 3. Hướng dẫn chạy

Mở PowerShell tại thư mục gốc của repository và kích hoạt môi trường ảo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài đặt thư viện nếu môi trường chưa có đủ:

```powershell
pip install -r requirements.txt
```

Chạy pipeline xử lý dữ liệu:

```powershell
python -m src.pipeline
```

Pipeline thực hiện các bước:

1. Đọc hai file `customers_raw.csv` và `orders_2024_2026.csv` trong thư mục `data/raw/`.
2. In số dòng, số cột và tỷ lệ ô trống của từng cột.
3. Chuẩn hóa ngày tháng trong dữ liệu đơn hàng về định dạng `YYYY-MM-DD`.
4. Chuẩn hóa số tiền, bao gồm số nguyên và định dạng tiền Việt Nam có dấu chấm phân cách hàng nghìn, ví dụ `34.980.500đ`.
5. Phân loại các dòng có ngày và số tiền hợp lệ; từ chối các dòng thiếu ngày hoặc thiếu số tiền và ghi rõ lý do.
6. Kiểm tra tính bảo toàn số dòng và xác nhận các dòng bị từ chối có lý do.
7. Lưu dữ liệu hợp lệ, dữ liệu bị từ chối và báo cáo chất lượng.

Kết quả được lưu tại:

- `data/processed/orders_normalized.csv`: các dòng đơn hàng có ngày và số tiền hợp lệ.
- `data/processed/orders_reject.csv`: các dòng bị từ chối, kèm lý do.
- `docs/bao-cao-chat-luong.md`: báo cáo kết quả kiểm tra chất lượng.
- `docs/pipeline-result.png`: ảnh minh chứng kết quả chạy pipeline.

**Lưu ý:** Pipeline hiện mới thực hiện thống kê dữ liệu, chuẩn hóa ngày tháng và số tiền, phân loại dữ liệu theo hai tiêu chí này và kiểm tra chất lượng cơ bản. Chưa thực hiện ghép hồ sơ khách hàng với đơn hàng hoặc tính phân khúc khách hàng theo QT-12.

## 4. Cấu trúc thư mục

- `docs/`: SRS, đặc tả dữ liệu, sơ đồ thiết kế, wireframe, khai báo sử dụng AI, báo cáo chất lượng và ảnh minh chứng.
- `data/raw/`: Dữ liệu CSV đầu vào.
- `data/processed/`: Dữ liệu sau xử lý và các dòng bị từ chối.
- `notebooks/`: Notebook khảo sát và phân tích dữ liệu.
- `src/extract/`: Module đọc dữ liệu đầu vào.
- `src/transform/`: Module chuẩn hóa và chuyển đổi dữ liệu.
- `src/quality/`: Module kiểm tra chất lượng dữ liệu.
- `src/load/`: Module lưu dữ liệu đầu ra và báo cáo chất lượng.
- `src/pipeline.py`: Điểm chạy chính của pipeline.
- `src/check_env.py`: Kiểm tra môi trường thực thi.
- `tests/`: Các unit test cho chuẩn hóa dữ liệu và xử lý đơn hàng.
- `dashboard/`: Thư mục dự kiến dành cho giao diện hiển thị kết quả phân tích.
- `requirements.txt`: Danh sách thư viện Python.
- `.env.example`: Mẫu cấu hình môi trường.
- `.gitignore`: Danh sách file và thư mục không đưa lên GitHub.

## 5. Kiểm thử

Chạy pipeline bằng lệnh:

```powershell
python -m src.pipeline
```

### Kết quả xử lý dữ liệu đơn hàng

Kết quả chạy pipeline gần nhất:

- Số dòng ban đầu: **26.000**.
- Số dòng hợp lệ: **25.607**.
- Số dòng bị từ chối: **393**.
- Tổng số dòng sau phân loại: **26.000**.

Trong 393 dòng bị từ chối:

- 279 dòng thiếu số tiền.
- 114 dòng thiếu ngày.

Các dòng bị từ chối được lưu riêng tại `data/processed/orders_reject.csv`, kèm lý do từ chối. Dữ liệu hợp lệ được lưu tại `data/processed/orders_normalized.csv`.

Tổng số dòng hợp lệ và bị từ chối bằng số dòng ban đầu, bảo đảm không thất thoát dòng trong quá trình phân loại.

Kết quả kiểm tra chất lượng của lần chạy gần nhất:

- Bảo toàn số dòng: `True`.
- Dòng bị từ chối có lý do: `True`.

### Kết quả unit test

Chạy kiểm thử bằng lệnh:

```powershell
python -m pytest -q
```

**Kết quả kiểm thử gần nhất: 12/12 unit test đạt yêu cầu**, bao gồm các trường hợp chuẩn hóa ngày tháng, chuẩn hóa số tiền, dữ liệu trống, dữ liệu không hợp lệ và kiểm thử nghiệp vụ xử lý đơn hàng.

Ảnh minh chứng kết quả chạy pipeline được lưu tại `docs/pipeline-result.png`. Báo cáo chất lượng dữ liệu được lưu tại `docs/bao-cao-chat-luong.md`.

Chưa kiểm thử đầy đủ chức năng và hiệu năng của toàn hệ thống.

## 6. Trạng thái hiện tại

- [x] Khởi tạo repository và môi trường ảo.
- [x] Hoàn thành phân tích và thiết kế BT1.
- [x] Đưa các sơ đồ, wireframe và khai báo sử dụng AI lên repository.
- [x] Đồng bộ SRS và đặc tả dữ liệu với báo cáo BT1.
- [x] Tạo cấu trúc module ETL ban đầu cho Track DA.
- [x] Đọc dữ liệu CSV bằng Pandas.
- [x] In số dòng, số cột và tỷ lệ ô trống theo từng cột.
- [x] Chuẩn hóa ngày tháng của dữ liệu đơn hàng.
- [x] Chuẩn hóa số tiền theo định dạng dữ liệu đầu vào.
- [x] Ghi dữ liệu hợp lệ và dữ liệu bị từ chối vào các file riêng.
- [x] Ghi lý do từ chối dữ liệu.
- [x] Hoàn thiện module kiểm tra chất lượng dữ liệu cơ bản.
- [x] Lưu báo cáo chất lượng dữ liệu.
- [x] Bổ sung và chạy 12 unit test, gồm kiểm thử chuẩn hóa dữ liệu và xử lý đơn hàng.
- [x] Lưu ảnh minh chứng kết quả chạy pipeline.
- [ ] Xác nhận cách ghép hồ sơ khách hàng với đơn hàng và quy tắc xác định đơn hàng hợp lệ.
- [ ] Triển khai tính chỉ số và phân khúc theo QT-12.
- [ ] Xây dựng dashboard.
- [ ] Kiểm thử chức năng và hiệu năng toàn hệ thống.

## 7. Tài liệu tham khảo trong repository

- `docs/srs.md`: Đặc tả yêu cầu phần mềm.
- `docs/data-requirements.md`: Yêu cầu dữ liệu.
- `docs/architecture.drawio`: Sơ đồ kiến trúc.
- `docs/erd.drawio`: Sơ đồ thực thể – liên kết.
- `docs/usecase.drawio`: Sơ đồ Use Case.
- `docs/wireframe.png`: Hình ảnh thiết kế giao diện.
- `docs/ai-disclosure.md`: Khai báo sử dụng công cụ AI.
- `docs/pipeline-result.png`: Ảnh minh chứng chạy pipeline.
- `docs/bao-cao-chat-luong.md`: Báo cáo kiểm tra chất lượng dữ liệu.