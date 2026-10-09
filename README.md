# Hệ thống phân khúc khách hàng theo dữ liệu mua hàng

**Sinh viên:** Trần Thị Như Quỳnh – 2374802010428 – Track DA  
**Học phần:** Chuyên đề Tốt nghiệp 1, HK1 2026–2027  
**Luồng nghiệp vụ:** L1 – Hồ sơ khách hàng & phân khúc

## 1. Mục tiêu

Hỗ trợ nhân viên Marketing phân khúc khách hàng thành VIP,
Thường xuyên, Mới và Ngủ đông theo quy tắc QT-12.
Người phân tích dữ liệu kiểm tra chất lượng dữ liệu đầu vào.
Hệ thống tính chỉ số mua hàng, hiển thị phân khúc, hỗ trợ lọc,
thống kê và xuất kết quả.

## 2. Yêu cầu môi trường

- Python 3.11 trở lên; sử dụng môi trường ảo `.venv`.
- Thư viện: Pandas, NumPy, Jupyter, Matplotlib, SQLAlchemy,
  psycopg2-binary và python-dotenv; xem `requirements.txt`.
- Cơ sở dữ liệu dự kiến: PostgreSQL.
- Biến môi trường: xem `.env.example`.
- Mở sơ đồ `.drawio` bằng diagrams.net.

## 3. Hướng dẫn chạy

BT1 đang ở giai đoạn phân tích và thiết kế.
Hướng dẫn chạy chương trình sẽ được bổ sung khi triển khai BT2.

Tài liệu nằm trong thư mục `docs/`.
Mở file `.drawio` bằng https://app.diagrams.net.
Xem thiết kế dashboard tại `docs/wireframe.png`.

## 4. Cấu trúc thư mục

- `docs/`: SRS, đặc tả dữ liệu, sơ đồ thiết kế, wireframe
  và khai báo sử dụng AI.
- `data/`: Dữ liệu đầu vào và dữ liệu sau xử lý.
- `notebooks/`: Notebook khảo sát và phân tích dữ liệu.
- `src/`: Mã nguồn xử lý dữ liệu và phân khúc khách hàng.
- `dashboard/`: Giao diện hiển thị kết quả phân tích.
- `tests/`: Mã kiểm thử, bổ sung khi triển khai.
- `requirements.txt`: Danh sách thư viện Python.
- `.env.example`: Mẫu cấu hình môi trường.
- `.gitignore`: Danh sách file và thư mục không đưa lên GitHub.

## 5. Kiểm thử

Chưa có kết quả kiểm thử chức năng và hiệu năng.
Sẽ bổ sung lệnh chạy kiểm thử và số lượng test PASS khi triển khai BT2.

## 6. Trạng thái hiện tại

- [x] Khởi tạo repository và môi trường ảo.
- [x] Soạn nội dung phân tích và thiết kế BT1.
- [x] Đưa các sơ đồ, wireframe và khai báo AI lên nhánh `dev`.
- [x] Đồng bộ SRS và đặc tả dữ liệu trên repo với báo cáo BT1.
- [ ] Triển khai kiểm tra và xử lý dữ liệu.
- [ ] Triển khai tính chỉ số và phân khúc theo QT-12.
- [ ] Xây dựng dashboard.
- [ ] Kiểm thử chức năng và hiệu năng.