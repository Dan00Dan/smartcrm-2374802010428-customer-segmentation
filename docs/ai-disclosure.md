# PHỤ LỤC – KHAI BÁO SỬ DỤNG CÔNG CỤ AI

## 1. Danh sách công cụ và phạm vi sử dụng

| Công cụ | Mục đích sử dụng | Phạm vi áp dụng | Cách kiểm chứng |
|---|---|---|---|
| ChatGPT | Hỗ trợ phân tích yêu cầu, soạn thảo và rà soát User Story, đặc tả chức năng, bảng truy vết yêu cầu và sơ đồ Use Case. | BT1 – SRS, Use Case và bảng truy vết yêu cầu. | Đối chiếu với đề bài, kiểm tra tính nhất quán giữa User Story, Functional Requirements (FR) và Use Case. |
| ChatGPT | Hỗ trợ đề xuất kiến trúc hệ thống, mô hình dữ liệu, sơ đồ thiết kế và wireframe. | BT1 – Kiến trúc hệ thống, mô hình dữ liệu, ERD và Wireframe. | Đối chiếu vai trò các thành phần, mức chi tiết dữ liệu (grain), khóa liên kết và nội dung hiển thị với yêu cầu hệ thống. Số liệu trên wireframe chỉ mang tính minh họa. |
| ChatGPT | Hỗ trợ phân tích lỗi trong quy trình ETL, đề xuất phương án xử lý dữ liệu và rà soát mã nguồn. | BT2 – Quy trình ETL, `src/etl/load_warehouse.py`, Bug Log và tài liệu thay đổi thiết kế. | Kiểm tra lại mã nguồn sau chỉnh sửa, thực thi pipeline, đối chiếu kết quả xử lý dữ liệu và kiểm thử các trường hợp liên quan. |
| ChatGPT | Hỗ trợ xây dựng, chỉnh sửa và rà soát tài liệu kiểm thử, triển khai, bảo mật và tài liệu kỹ thuật. | BT3 – Test Plan, Test Report, Bug Log, Deployment Guide, Security Checklist và Technical Document. | Đối chiếu nội dung tài liệu với mã nguồn, yêu cầu bài tập, kết quả kiểm thử thực tế và các ảnh minh chứng đã thu thập. |

## 2. Công cụ kỹ thuật hỗ trợ thực hiện dự án

Các công cụ dưới đây được sử dụng để phát triển, thực thi và kiểm chứng hệ thống; không phải công cụ AI.

| Công cụ | Mục đích sử dụng | Phạm vi áp dụng | Cách kiểm chứng |
|---|---|---|---|
| Python | Thực thi quy trình ETL, xử lý, chuẩn hóa, kiểm tra và nạp dữ liệu vào Data Warehouse. | Mã nguồn trong thư mục `src/`. | Chạy chương trình, kiểm tra dữ liệu đầu ra, báo cáo chất lượng dữ liệu và kết quả nạp kho. |
| pytest | Thực thi kiểm thử tự động và kiểm thử hồi quy cho các chức năng của hệ thống. | Bộ kiểm thử trong thư mục `tests/`. | Chạy bộ kiểm thử và ghi nhận kết quả PASS/FAIL thực tế. |

## 3. Cam kết và trách nhiệm

Tôi xác nhận đã đọc, hiểu và chịu trách nhiệm về toàn bộ nội dung của dự án trước khi nộp.

Trong quá trình thực hiện, tôi sử dụng ChatGPT để hỗ trợ phân tích yêu cầu, đề xuất phương án, soạn thảo và rà soát tài liệu, cũng như hỗ trợ tìm hiểu và xử lý các vấn đề kỹ thuật. Các nội dung do AI đề xuất đều được xem xét, điều chỉnh và đối chiếu với yêu cầu thực tế của dự án trước khi sử dụng.

Tôi không sử dụng nội dung do AI tạo ra để thay thế cho việc thực thi, kiểm thử và kiểm chứng kết quả. Các kết quả kiểm thử, trạng thái chương trình, dữ liệu đầu ra và thông tin triển khai được ghi nhận dựa trên quá trình thực hiện và kiểm tra thực tế.

Tôi chịu trách nhiệm về tính chính xác, phù hợp, nhất quán và trung thực của toàn bộ nội dung được sử dụng trong sản phẩm bàn giao.

- **Họ và tên:** Trần Thị Như Quỳnh
- **MSSV:** 2374802010428
- **Ngày khai báo:** 22/11/2026