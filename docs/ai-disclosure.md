# Phụ lục – Khai báo sử dụng công cụ AI

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
|---|---|---|---|
| ChatGPT | Hỗ trợ soạn thảo, rà soát yêu cầu, bảng truy vết, đặc tả và sơ đồ Use Case. | BT1 – SRS; Use Case; bảng truy vết yêu cầu. | Đối chiếu yêu cầu đề bài; rà soát tính nhất quán giữa User Story, FR và Use Case. |
| ChatGPT | Hỗ trợ đề xuất kiến trúc, mô hình dữ liệu, sơ đồ và wireframe. | BT1 – Kiến trúc; mô hình dữ liệu; Wireframe. | Đối chiếu vai trò các lớp, grain, khóa liên kết và trường hiển thị với yêu cầu hệ thống. Số liệu trên wireframe chỉ mang tính minh họa. |
| ChatGPT | Hỗ trợ phân tích lỗi ETL, đề xuất cách xử lý dữ liệu và rà soát mã nguồn. | BT2 – ETL; `src/etl/load_warehouse.py`; Bug Log; tài liệu thay đổi thiết kế. | Đối chiếu thay đổi mã nguồn, thực thi pipeline và kiểm tra kết quả thực tế. |
| ChatGPT | Hỗ trợ xây dựng, chỉnh sửa và rà soát Test Plan, Test Report, Bug Log, Deployment Guide, Security Checklist và Technical Document. | BT3 – Tài liệu kiểm thử, triển khai, bảo mật và kỹ thuật. | Đối chiếu tài liệu với mã nguồn, yêu cầu BT3, kết quả kiểm thử thực tế và minh chứng đã thu thập. |
| Python và pytest | Thực thi pipeline xử lý dữ liệu và kiểm thử tự động. | Mã nguồn trong `src/`, bộ kiểm thử trong `tests/`. | Trực tiếp chạy chương trình, kiểm tra đầu ra và ghi nhận kết quả PASS/FAIL thực tế. |

## Cam kết

Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung nộp. Tôi sử dụng ChatGPT để hỗ trợ quá trình phân tích, soạn thảo và rà soát tài liệu; không sử dụng kết quả do AI đề xuất thay thế cho việc thực thi và kiểm chứng thực tế.

Các kết quả kiểm thử, trạng thái chương trình, ảnh minh chứng và thông tin triển khai được ghi nhận dựa trên quá trình thực hiện và kiểm tra thực tế của tôi.

Tôi chịu trách nhiệm đánh giá tính chính xác, phù hợp và trung thực của toàn bộ nội dung trước khi sử dụng và nộp.

- **Họ tên:** Trần Thị Như Quỳnh
- **MSSV:** 2374802010428
- **Ngày:** 13/11/2026