# Ghi nhận thay đổi thiết kế theo phản hồi BT1

**Dự án:** Smart CRM – L1: Tính và gán phân khúc khách hàng  
**Track:** Data Analyst

Tài liệu ghi nhận phản hồi của giảng viên sau BT1, quyết định xử lý, lý do và ảnh hưởng đến thiết kế dự án.

## TD-01 – Số lượng User Story

- **Phản hồi:** BT1 có 8 User Story, trong khi yêu cầu là 5–7 User Story. Giảng viên đề xuất gộp các yêu cầu phù hợp để giảm số lượng.
- **Quyết định:** SỬA.
- **Lý do:** Đưa số lượng User Story về đúng yêu cầu và hạn chế nội dung trùng lặp.
- **Ảnh hưởng:** Điều chỉnh bảng User Story trong `docs/srs.md` và kiểm tra tính nhất quán với các Use Case liên quan. SRS hiện có 7 User Story.

## TD-02 – Bổ sung thuật ngữ nghiệp vụ

- **Phản hồi:** Phần thuật ngữ chủ yếu là chữ viết tắt; cần giải thích thêm các thuật ngữ nghiệp vụ như chỉ số mua hàng, ngày chốt, đơn hàng hoàn tất và kỳ phân tích.
- **Quyết định:** SỬA.
- **Lý do:** Giúp người đọc hiểu thống nhất các khái niệm được sử dụng trong yêu cầu và quy tắc phân khúc khách hàng.
- **Ảnh hưởng:** Bổ sung và chuẩn hóa phần thuật ngữ trong `docs/srs.md`.

## TD-03 – Thông tin lưu trữ lỗi và lần chạy

- **Phản hồi:** Kiến trúc đề cập việc lưu báo cáo lỗi và thông tin lần chạy, nhưng sơ đồ dữ liệu kho chưa có bảng tương ứng.
- **Quyết định:** SỬA.
- **Lý do:** Làm rõ sự khác biệt giữa dữ liệu phục vụ phân tích khách hàng và thông tin phục vụ theo dõi vận hành.
- **Ảnh hưởng:** Làm rõ cách lưu thông tin lỗi và lần chạy trong `docs/srs.md`; đối chiếu với `docs/architecture.drawio` để bảo đảm hai tài liệu thống nhất.

## TD-04 – Tài liệu trong repository

- **Phản hồi:** Tại thời điểm đánh giá BT1, repository còn thiếu một số tài liệu cần thiết như SRS, sơ đồ thiết kế gốc, wireframe, khai báo sử dụng AI và yêu cầu dữ liệu.
- **Quyết định:** SỬA.
- **Lý do:** Bảo đảm tài liệu phân tích và thiết kế được lưu trong repository để thuận tiện kiểm tra, theo dõi thay đổi và phát triển tiếp.
- **Ảnh hưởng:** Các tài liệu đã được bổ sung trong thư mục `docs/`, gồm `srs.md`, các sơ đồ `.drawio`, `wireframe.png`, `ai-disclosure.md` và `data-requirements.md`. Tiếp tục kiểm tra tính đầy đủ và nhất quán của các tài liệu.

## TD-05 – Sửa xử lý ngày trong ETL

- **Vấn đề:** Module nạp dữ liệu vào kho tham chiếu cột `order_date` trước khi cột này được tạo từ dữ liệu nguồn `ngay`.
- **Quyết định:** SỬA.
- **Thay đổi:** Chuẩn hóa dữ liệu ngày từ cột nguồn `ngay` bằng `pd.to_datetime`, sử dụng `format="mixed"`, `dayfirst=True` và `errors="coerce"`.
- **Lý do:** Hỗ trợ dữ liệu ngày có nhiều định dạng và chuyển các giá trị không hợp lệ thành giá trị thiếu để quy trình kiểm tra chất lượng xử lý.
- **Ảnh hưởng:** Cập nhật `src/etl/load_warehouse.py` để xử lý ngày trước khi sử dụng cột `order_date`. Tiếp tục theo dõi các bản ghi bị từ chối và kiểm tra kết quả của pipeline.
- **Kết quả kiểm chứng:** Bộ kiểm thử gần nhất đạt 20/20 bài kiểm thử.
- **Commit liên quan:** `289f6e1 – Fix warehouse order date parsing`.

## Trạng thái thực hiện

- Đã ghi nhận 4 nhóm phản hồi thiết kế từ BT1.
- Đã bổ sung TD-05 để ghi nhận việc sửa lỗi xử lý ngày trong ETL.
- Các quyết định, lý do và ảnh hưởng được ghi lại để phục vụ theo dõi thay đổi.
- Cần tiếp tục đối chiếu SRS, sơ đồ kiến trúc, wireframe và kết quả thực thi để xác nhận tính nhất quán của toàn bộ dự án.