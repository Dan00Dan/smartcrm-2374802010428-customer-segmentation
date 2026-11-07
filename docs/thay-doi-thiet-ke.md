# Ghi nhận thay đổi thiết kế theo phản hồi BT1 và BT2

**Dự án:** Smart CRM – L1: Tính và gán phân khúc khách hàng  
**Track:** Data Analyst

Tài liệu ghi nhận phản hồi của giảng viên sau BT1 và BT2, quyết định xử lý, lý do và ảnh hưởng đến thiết kế dự án.

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

## TD-06 – Trạng thái truy vấn Dashboard

- **Phản hồi:** Dashboard chưa có minh chứng đầy đủ cho ba trạng thái: đang truy vấn, bộ lọc rỗng và lỗi kết nối dữ liệu.
- **Quyết định:** SỬA.
- **Thay đổi:** Bổ sung trạng thái đang truy vấn bằng `st.spinner`, thông báo truy vấn thành công, cảnh báo bộ lọc rỗng và thông báo lỗi khi không tải được dữ liệu kho.
- **Lý do:** Giúp người dùng nhận biết trạng thái xử lý và nguyên nhân không hiển thị dữ liệu.
- **Ảnh hưởng:** Điều chỉnh `app.py`, bổ sung trạng thái trực quan trên Dashboard.
- **Kiểm chứng:** Đối chiếu ba trạng thái truy vấn và chụp ảnh minh chứng phục vụ tiêu chí D4.

## TD-07 – Bổ sung mốc tham chiếu biểu đồ

- **Phản hồi:** Dashboard chưa thể hiện mốc tham chiếu cho từng biểu đồ.
- **Quyết định:** SỬA.
- **Thay đổi:** Bổ sung đường tham chiếu trung bình trên các biểu đồ số đơn hàng theo tháng, tổng tiền ghi nhận theo tháng và số lượng khách hàng theo phân khúc.
- **Lý do:** Hỗ trợ người dùng so sánh quy mô dữ liệu giữa các tháng và các phân khúc.
- **Ảnh hưởng:** Điều chỉnh hàm `render_svg_chart` và các biểu đồ liên quan trong `app.py`.
- **Kiểm chứng:** Đối chiếu đường tham chiếu trên Dashboard và chụp ảnh minh chứng.

## TD-08 – Làm rõ cơ chế Migration và Seed

- **Phản hồi:** Repository chưa thể hiện rõ cơ chế khởi tạo kho dữ liệu và seed dữ liệu kiểm thử.
- **Quyết định:** SỬA.
- **Thay đổi:** Bổ sung `docs/migration-seed.md`, mô tả cơ chế khởi tạo kho CSV bằng ETL snapshot và seed dữ liệu kiểm thử bằng `pandas.DataFrame`.
- **Lý do:** Làm rõ cách khởi tạo dữ liệu và tái lập kiểm thử mà không phụ thuộc vào SQL Migration.
- **Ảnh hưởng:** Bổ sung tài liệu quy trình khởi tạo kho và kiểm thử.
- **Kiểm chứng:** Chạy `python -m pytest tests -q`, kết quả hiện tại 20/20 test PASS.

## Trạng thái thực hiện

- Đã ghi nhận TD-01 đến TD-05 từ phản hồi BT1.
- Đã bổ sung TD-06 đến TD-08 từ phản hồi BT2.
- Đã điều chỉnh Dashboard để thể hiện trạng thái truy vấn, bộ lọc rỗng và mốc tham chiếu biểu đồ.
- Đã bổ sung tài liệu `docs/migration-seed.md`.
- Bộ kiểm thử hiện tại đạt 20/20 bài kiểm thử.
- Tiếp tục hoàn thiện minh chứng D4 và kiểm tra tính nhất quán của repository trước khi chuyển sang BT3.