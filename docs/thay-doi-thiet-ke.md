# GHI NHẬN THAY ĐỔI THIẾT KẾ THEO PHẢN HỒI BT1, BT2 VÀ BT3

**Dự án:** Smart CRM – L1: Hồ sơ khách hàng và phân khúc
**Sinh viên:** Trần Thị Như Quỳnh
**MSSV:** 2374802010428
**Track:** Data Analyst
**Phiên bản tài liệu:** 2.1

Tài liệu ghi nhận các phản hồi của giảng viên qua BT1, BT2 và BT3; các quyết định xử lý, lý do, ảnh hưởng đến thiết kế và những vấn đề được ghi nhận nhưng chưa thực hiện.

Các thay đổi được phân loại thành ba nhóm: **phải sửa hoặc làm rõ**, **nên sửa** và **ghi nhận không sửa**.

---

## 1. Ghi nhận các thay đổi thiết kế

### TD-01 – Điều chỉnh số lượng User Story

- **Phản hồi:** BT1 có 8 User Story, trong khi yêu cầu là 5–7 User Story. Giảng viên đề xuất gộp các yêu cầu phù hợp để giảm số lượng.
- **Quyết định:** PHẢI SỬA.
- **Lý do:** Đưa số lượng User Story về đúng yêu cầu và hạn chế nội dung trùng lặp.
- **Thay đổi:** Điều chỉnh bảng User Story trong `docs/srs.md`.
- **Kết quả:** SRS hiện có 7 User Story.

### TD-02 – Bổ sung thuật ngữ nghiệp vụ

- **Phản hồi:** Phần thuật ngữ chủ yếu là chữ viết tắt; cần giải thích thêm các thuật ngữ nghiệp vụ như chỉ số mua hàng, ngày chốt, đơn hàng hoàn tất và kỳ phân tích.
- **Quyết định:** PHẢI SỬA.
- **Lý do:** Giúp người đọc hiểu thống nhất các khái niệm được sử dụng trong yêu cầu và quy tắc phân khúc khách hàng.
- **Thay đổi:** Bổ sung và chuẩn hóa phần thuật ngữ trong `docs/srs.md`.
- **Kết quả:** Các thuật ngữ nghiệp vụ được giải thích rõ hơn trong tài liệu yêu cầu.

### TD-03 – Làm rõ thông tin lưu trữ lỗi và lần chạy

- **Phản hồi:** Kiến trúc đề cập việc lưu báo cáo lỗi và thông tin lần chạy, nhưng sơ đồ dữ liệu kho chưa có bảng tương ứng.
- **Quyết định:** PHẢI LÀM RÕ.
- **Lý do:** Phân biệt dữ liệu phục vụ phân tích khách hàng với thông tin phục vụ theo dõi vận hành.
- **Thay đổi:** Bổ sung mô tả về nhật ký vận hành trong `docs/srs.md`; xác định các thông tin cần ghi nhận gồm mã lần chạy, kỳ phân tích, thời điểm chạy, trạng thái thực hiện và thông tin lỗi phù hợp. Sơ đồ `docs/architecture.drawio` thể hiện khối lưu trữ kết quả, báo cáo lỗi và thông tin lần chạy.
- **Ảnh hưởng:** Làm rõ yêu cầu và kiến trúc lưu trữ ở mức thiết kế. Nhật ký vận hành được xác định là thành phần riêng, không thuộc lược đồ hình sao phục vụ phân tích.
- **Giới hạn hiện tại:** Chưa triển khai hoặc xác nhận có bảng nhật ký vận hành độc lập trong kho dữ liệu. Nội dung này mới được làm rõ ở mức yêu cầu và thiết kế, không được xem là chức năng đã hoàn thiện.
- **Kết quả:** Đã xử lý phần thiếu rõ ràng trong tài liệu thiết kế; việc triển khai thành phần lưu trữ nhật ký vẫn là nội dung cần xem xét ở giai đoạn tiếp theo.

### TD-04 – Bổ sung tài liệu trong repository

- **Phản hồi:** Tại thời điểm đánh giá BT1, repository còn thiếu một số tài liệu cần thiết như SRS, sơ đồ thiết kế gốc, wireframe, khai báo sử dụng AI và yêu cầu dữ liệu.
- **Quyết định:** PHẢI SỬA.
- **Lý do:** Bảo đảm tài liệu phân tích và thiết kế được lưu trong repository để thuận tiện kiểm tra, theo dõi thay đổi và phát triển tiếp.
- **Thay đổi:** Bổ sung các tài liệu trong thư mục `docs/`, gồm `srs.md`, các sơ đồ `.drawio`, `wireframe.png`, `ai-disclosure.md` và `data-requirements.md`.
- **Kết quả:** Các tài liệu phân tích và thiết kế chính được đưa vào repository.

### TD-05 – Sửa lỗi xử lý ngày trong ETL

- **Vấn đề:** Module nạp dữ liệu vào kho tham chiếu cột `order_date` trước khi cột này được tạo từ dữ liệu nguồn `ngay`.
- **Quyết định:** PHẢI SỬA.
- **Thay đổi:** Chuẩn hóa dữ liệu ngày từ cột nguồn `ngay` bằng `pd.to_datetime`, sử dụng `format="mixed"`, `dayfirst=True` và `errors="coerce"`.
- **Lý do:** Hỗ trợ dữ liệu ngày có nhiều định dạng và chuyển các giá trị không hợp lệ thành giá trị thiếu để quy trình kiểm tra chất lượng xử lý.
- **Ảnh hưởng:** Cập nhật `src/etl/load_warehouse.py`.
- **Kết quả kiểm chứng:** Bộ kiểm thử toàn dự án gần nhất được ghi nhận đạt 37 passed, 0 failed.
- **Commit liên quan:** `289f6e1 – Fix warehouse order date parsing`.

### TD-06 – Bổ sung trạng thái truy vấn Dashboard

- **Phản hồi:** Dashboard chưa có minh chứng đầy đủ cho ba trạng thái: đang truy vấn, bộ lọc rỗng và lỗi kết nối dữ liệu.
- **Quyết định:** NÊN SỬA.
- **Thay đổi:** Bổ sung trạng thái đang truy vấn bằng `st.spinner`, thông báo truy vấn thành công, cảnh báo bộ lọc rỗng và thông báo lỗi khi không tải được dữ liệu kho.
- **Lý do:** Giúp người dùng nhận biết trạng thái xử lý và nguyên nhân không hiển thị dữ liệu.
- **Ảnh hưởng:** Điều chỉnh `app.py`.
- **Kiểm chứng:** Đối chiếu các trạng thái truy vấn và ảnh minh chứng Dashboard.
- **Kết quả:** Đã bổ sung các trạng thái phản hồi trong giao diện.

### TD-07 – Bổ sung mốc tham chiếu biểu đồ

- **Phản hồi:** Dashboard chưa thể hiện mốc tham chiếu cho từng biểu đồ.
- **Quyết định:** NÊN SỬA.
- **Thay đổi:** Bổ sung đường tham chiếu trung bình trên các biểu đồ số đơn hàng theo tháng, tổng tiền ghi nhận theo tháng và số lượng khách hàng theo phân khúc.
- **Lý do:** Hỗ trợ người dùng so sánh quy mô dữ liệu giữa các tháng và các phân khúc.
- **Ảnh hưởng:** Điều chỉnh hàm `render_svg_chart` và các biểu đồ liên quan trong `app.py`.
- **Kiểm chứng:** Đối chiếu đường tham chiếu trên Dashboard.
- **Kết quả:** Đã bổ sung mốc tham chiếu trên các biểu đồ liên quan.

### TD-08 – Làm rõ cơ chế Migration và Seed

- **Phản hồi:** Repository chưa thể hiện rõ cơ chế khởi tạo kho dữ liệu và seed dữ liệu kiểm thử.
- **Quyết định:** NÊN SỬA.
- **Thay đổi:** Bổ sung `docs/migration-seed.md`, mô tả cơ chế khởi tạo kho CSV bằng ETL snapshot và seed dữ liệu kiểm thử bằng `pandas.DataFrame`.
- **Lý do:** Làm rõ cách khởi tạo dữ liệu và tái lập kiểm thử mà không phụ thuộc vào SQL Migration.
- **Kiểm chứng:** Đối chiếu tài liệu với quy trình ETL và bộ kiểm thử.
- **Kết quả:** Đã bổ sung tài liệu mô tả cơ chế Migration và Seed phù hợp với kiến trúc kho CSV hiện tại.

### TD-09 – Bổ sung Bug Log theo phản hồi BT3

- **Phản hồi:** Bug Log trước đây chỉ có phần tổng quan và kết luận, chưa có danh sách lỗi đã sửa, mức độ nghiêm trọng và commit liên quan.
- **Quyết định:** PHẢI SỬA.
- **Thay đổi:** Bổ sung `docs/bug-log.md` với 4 lỗi Major, gồm lỗi mã hồ sơ khách hàng, ngày đơn hàng, thành tiền và phân tích nhiều định dạng ngày.
- **Lý do:** Bảo đảm có thể truy vết lỗi, cách xử lý và thay đổi mã nguồn.
- **Kiểm chứng:** Bổ sung kiểm thử hồi quy và liên kết commit `e7def4a`, `289f6e1`.
- **Kết quả:** Đã ghi nhận các lỗi chính, phương án xử lý và thông tin commit liên quan.

### TD-10 – Bổ sung Deployment Guide

- **Phản hồi:** Repository chưa có `docs/deployment-guide.md`; hướng dẫn triển khai chỉ xuất hiện trong báo cáo.
- **Quyết định:** PHẢI SỬA.
- **Thay đổi:** Bổ sung `docs/deployment-guide.md`, hướng dẫn chuẩn bị môi trường, cấu hình biến môi trường, triển khai Docker Compose, kiểm tra Dashboard và xử lý lỗi thường gặp.
- **Lý do:** Giúp người khác có thể triển khai và kiểm tra hệ thống từ repository.
- **Kiểm chứng:** Kiểm tra cấu hình bằng `docker compose config --quiet`; Docker đã được chạy và Dashboard truy cập tại `http://localhost:8501` trong môi trường ban đầu.
- **Kết quả:** Đã bổ sung hướng dẫn triển khai và kiểm tra hệ thống bằng Docker.

### TD-11 – Bổ sung đo lường chất lượng dữ liệu D3

- **Phản hồi:** Cần thể hiện rõ việc đo chất lượng dữ liệu theo ba chiều và theo từng cột.
- **Quyết định:** PHẢI SỬA.
- **Thay đổi:** Bổ sung mã kiểm tra chất lượng, kiểm thử và báo cáo chất lượng dữ liệu theo cột trong các tài liệu và mã nguồn liên quan.
- **Lý do:** Giúp phát hiện, thống kê và truy vết các vấn đề chất lượng dữ liệu thay vì chỉ đưa ra nhận xét tổng quan.
- **Tài liệu và mã nguồn liên quan:** `src/quality/check_quality.py`, `tests/test_quality.py`, `docs/bao-cao-chat-luong.md`, `docs/data-quality-by-column.csv`.
- **Kết quả:** Đã bổ sung thành phần kiểm tra chất lượng dữ liệu và tài liệu báo cáo kết quả.

### TD-12 – Giả danh hóa dữ liệu cá nhân D4

- **Phản hồi:** Cần thể hiện rõ cơ chế giả danh hóa dữ liệu cá nhân.
- **Quyết định:** PHẢI SỬA.
- **Thay đổi:** Bổ sung cơ chế giả danh hóa bằng HMAC-SHA256, sử dụng biến môi trường `CRM_PSEUDONYM_SECRET`; loại bỏ thông tin định danh trực tiếp khỏi dữ liệu CSV đã xử lý.
- **Lý do:** Hạn chế việc lộ thông tin cá nhân trong dữ liệu phục vụ phân tích.
- **Tài liệu và mã nguồn liên quan:** `src/etl/load_warehouse.py`, `src/load/save_results.py`, `src/pipeline.py`.
- **Lưu ý:** Không đưa khóa bí mật hoặc tệp `.env` lên GitHub.
- **Kết quả:** Đã bổ sung cơ chế giả danh hóa trong quy trình xử lý dữ liệu. Đây không phải là thay thế cho cơ chế xác thực và phân quyền người dùng.

---

## 2. Phân loại theo yêu cầu bài giảng buổi 18

### 2.1. Phải sửa hoặc làm rõ

Các vấn đề ảnh hưởng trực tiếp đến tính đúng đắn nghiệp vụ, chất lượng dữ liệu, bảo vệ dữ liệu cá nhân và khả năng triển khai hệ thống.

| Mã | Nội dung | Lý do | Kết quả |
|---|---|---|---|
| TD-01 | Số lượng User Story | Phải đáp ứng phạm vi yêu cầu | Đã sửa |
| TD-02 | Thuật ngữ nghiệp vụ | Tránh hiểu sai yêu cầu | Đã bổ sung |
| TD-03 | Thông tin lưu trữ lỗi và lần chạy | Bảo đảm thiết kế rõ ràng | Đã làm rõ ở mức tài liệu; chưa triển khai bảng nhật ký độc lập |
| TD-04 | Tài liệu repository | Bảo đảm khả năng kiểm tra | Đã bổ sung |
| TD-05 | Xử lý ngày ETL | Tránh sai lệch dữ liệu | Đã sửa |
| TD-09 | Bug Log | Bảo đảm truy vết lỗi và commit | Đã bổ sung |
| TD-10 | Deployment Guide | Bảo đảm khả năng triển khai | Đã bổ sung |
| TD-11 | Chất lượng dữ liệu D3 | Đánh giá chất lượng theo cột | Đã bổ sung |
| TD-12 | Giả danh hóa D4 | Bảo vệ thông tin cá nhân | Đã bổ sung |

### 2.2. Nên sửa

Các cải tiến giúp tăng khả năng sử dụng, theo dõi và bảo trì hệ thống nhưng không làm thay đổi trực tiếp quy tắc phân khúc cốt lõi.

| Mã | Nội dung | Lý do | Kết quả |
|---|---|---|---|
| TD-06 | Trạng thái truy vấn Dashboard | Cải thiện trải nghiệm người dùng | Đã thực hiện |
| TD-07 | Mốc tham chiếu biểu đồ | Hỗ trợ phân tích và so sánh | Đã thực hiện |
| TD-08 | Migration và Seed | Hỗ trợ tái lập kiểm thử | Đã bổ sung |

### 2.3. Ghi nhận không sửa

Các vấn đề được ghi nhận nhưng chưa thực hiện do giới hạn dữ liệu nguồn hoặc chưa thuộc phạm vi hiện tại.

| Vấn đề | Quyết định | Lý do | Biện pháp kiểm soát |
|---|---|---|---|
| Không xác định được khách hàng của một số đơn hàng | Không tự động sửa | Dữ liệu nguồn không đủ căn cứ để ánh xạ duy nhất | Gán `UNKNOWN`, ghi nhận vấn đề chất lượng dữ liệu |
| Không xác minh được trạng thái hoàn tất của một số đơn hàng | Không tự suy đoán | Dữ liệu nguồn chưa cung cấp trạng thái đáng tin cậy | Đặt trạng thái `UNKNOWN`, chặn công bố phân khúc |
| Chuyển kho CSV sang hệ quản trị cơ sở dữ liệu quan hệ | Chưa thực hiện | Chưa có yêu cầu bắt buộc thay đổi kiến trúc lưu trữ hiện tại | Tiếp tục sử dụng kho CSV và ghi nhận giới hạn kiến trúc |

---

## 3. Trạng thái kiểm chứng hiện tại

Bảng dưới đây tổng hợp các kết quả đã được ghi nhận trong quá trình thực hiện dự án.

| Nội dung | Kết quả ghi nhận |
|---|---|
| User Story | 7 User Story |
| Bug Log | 4 lỗi Major có commit liên quan |
| Kiểm thử toàn dự án | Lần chạy gần nhất được ghi nhận: 37 passed, 0 failed |
| Kiểm thử nạp dữ liệu kho | Kết quả được ghi nhận: 9 passed, 0 failed |
| Data Quality D3 | Có mã kiểm tra, báo cáo và dữ liệu kết quả theo cột |
| Pseudonymization D4 | Có cơ chế HMAC-SHA256 |
| Deployment Guide | Có trong `docs/deployment-guide.md` |
| Docker | Đã chạy container ở trạng thái `healthy` |
| GitHub | Các thay đổi đã được commit và push |

**Lưu ý:** Kết quả kiểm thử là số liệu đã ghi nhận tại thời điểm thực hiện, không thay thế cho việc chạy lại bộ kiểm thử khi có thay đổi mã nguồn mới.

---

## 4. Kết luận

Qua các phản hồi BT1, BT2 và BT3, dự án đã được điều chỉnh theo hướng hoàn thiện yêu cầu nghiệp vụ, xử lý lỗi ETL, nâng cao chất lượng dữ liệu, giả danh hóa thông tin cá nhân và bổ sung tài liệu triển khai.

Các vấn đề bắt buộc đã được ưu tiên xử lý. Những cải tiến về Dashboard và khả năng tái lập kiểm thử đã được triển khai. Riêng nội dung nhật ký vận hành tại TD-03 đã được làm rõ ở mức tài liệu thiết kế nhưng chưa triển khai thành bảng lưu trữ độc lập.

Các hạn chế do dữ liệu nguồn hoặc phạm vi kiến trúc được ghi nhận và có biện pháp kiểm soát thay vì tự ý suy đoán hoặc sửa dữ liệu.

Tài liệu này được sử dụng để theo dõi lịch sử thay đổi thiết kế, giải trình quyết định kỹ thuật và đối chiếu tiến độ hoàn thiện Smart CRM.
