# Smart CRM – Hồ sơ khách hàng & phân khúc

**Sinh viên:** Trần Thị Như Quỳnh – MSSV: 2374802010428  
**Track:** Data Analyst (DA)  
**Học phần:** Chuyên đề Tốt nghiệp 1 – Trường Đại học Văn Lang  

## 1. Mô tả bài toán

Nhân viên Marketing tra cứu thông tin khách hàng và lịch sử mua hàng, kiểm tra dữ liệu cần thiết, tính tổng chi tiêu và số đơn hàng trong khoảng thời gian quy định, sau đó áp dụng quy tắc để phân khúc khách hàng.

Luồng nghiệp vụ:

Tra cứu khách hàng → kiểm tra lịch sử mua hàng → xử lý dữ liệu → tính tổng chi tiêu và số đơn hàng → phân khúc khách hàng → hiển thị kết quả.

## 2. Phạm vi

### Làm
- Tra cứu thông tin khách hàng.
- Đọc và xử lý dữ liệu lịch sử mua hàng.
- Kiểm tra dữ liệu cần thiết trước khi phân tích.
- Tính tổng chi tiêu của khách hàng.
- Tính số lượng đơn hàng trong khoảng thời gian quy định.
- Áp dụng quy tắc để phân khúc khách hàng.
- Trình bày kết quả phân tích và phân khúc.

### Không làm
- Không xây dựng toàn bộ hệ thống CRM.
- Không xây dựng chức năng quản lý bán hàng.
- Không xây dựng chức năng marketing automation.
- Không phát triển mô hình AI dự đoán hành vi khách hàng.

## 3. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ lập trình | Python |
| Xử lý dữ liệu | Pandas, NumPy |
| Phân tích dữ liệu | Jupyter Notebook |
| Trực quan hóa dữ liệu | Matplotlib |
| Cơ sở dữ liệu | PostgreSQL |
| Kết nối cơ sở dữ liệu | SQLAlchemy, psycopg2-binary |
| Quản lý biến môi trường | python-dotenv |
| Quản lý mã nguồn | Git, GitHub |
| Môi trường phát triển | Visual Studio Code |

## 4. Cấu trúc thư mục

```text
smartcrm-2374802010428-customer-segmentation/
│
├── docs/
│   └── .gitkeep
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
│
├── notebooks/
│   └── .gitkeep
│
├── src/
│   ├── check_env.py
│   └── etl/
│       └── .gitkeep
│
├── dashboard/
│   └── .gitkeep
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md