# Phụ lục – Khai báo sử dụng công cụ AI

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
|---|---|---|---|
| ChatGPT/Codex | Hỗ trợ soạn thảo và rà soát yêu cầu, bảng truy vết, đặc tả và sơ đồ Use Case. | Thành phần 1 – SRS; thành phần 2 – Use Case. | Đối chiếu yêu cầu đề bài; rà soát tính nhất quán giữa 7 User Story, 8 FR và 7 Use Case. |
| ChatGPT/Codex | Hỗ trợ đề xuất kiến trúc, mô hình dữ liệu, sơ đồ và wireframe. | Thành phần 3 – Kiến trúc; thành phần 4 – Mô hình dữ liệu; thành phần 5 – Wireframe. | Rà soát vai trò ba lớp, grain, khóa liên kết và trường hiển thị; đối chiếu nguồn dữ liệu và Use Case tương ứng. Số liệu trên wireframe chỉ mang tính minh họa, chưa phải kết quả kiểm thử hệ thống thực tế. |
| ChatGPT/Codex | Hỗ trợ phân tích lỗi ETL, đề xuất cách xử lý dữ liệu ngày và rà soát tài liệu kỹ thuật. | Thành phần triển khai BT2 – `src/etl/load_warehouse.py`, `docs/bug-log.md`, `docs/thay-doi-thiet-ke.md`. | Đối chiếu thay đổi mã nguồn, ghi nhận lỗi trong Bug Log và kiểm tra kết quả chạy pipeline, bộ kiểm thử tự động. |
| Python và pytest | Thực thi pipeline xử lý dữ liệu và kiểm thử tự động. | Mã nguồn trong `src/`, bộ kiểm thử trong `tests/` và `run_pipeline.py`. | Chạy chương trình, kiểm tra kết quả đầu ra và đối chiếu kết quả kiểm thử thực tế. |

## Cam kết

Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Tôi đã sử dụng các công cụ nêu trên để hỗ trợ quá trình thực hiện dự án và chịu trách nhiệm kiểm tra, đánh giá tính phù hợp của nội dung trước khi sử dụng.

- **Họ tên:** Trần Thị Như Quỳnh
- **MSSV:** 2374802010428
- **Ngày:** 09/10/2026