
# BÁO CÁO TỐI ƯU HIỆU NĂNG

**Dự án:** Smart CRM – Hệ thống phân khúc khách hàng  
**Sinh viên:** Trần Thị Như Quỳnh  
**MSSV:** 2374802010428  
**Track:** Data Analyst  
**Ngày thực hiện:** 22/11/2026

## 1. Mục tiêu tối ưu

Tối ưu quy trình đọc và xử lý dữ liệu đơn hàng trong pipeline ETL, hạn chế thao tác đọc cùng một file CSV nhiều lần trong một lần chạy.

## 2. Vấn đề trước khi tối ưu

Trong phiên bản ban đầu:

- `pipeline.py` đọc file `orders_2024_2026.csv` bằng `read_csv_data()`.
- Sau đó, `process_orders()` tiếp tục đọc lại chính file CSV này.
- DataFrame đơn hàng đã đọc ở bước đầu chưa được tái sử dụng cho bước xử lý.

Điều này tạo ra thao tác đọc dữ liệu trùng lặp, làm tăng thời gian thực thi và sử dụng tài nguyên không cần thiết.

## 3. Giải pháp tối ưu

Thực hiện các thay đổi:

1. Cập nhật `read_csv_data()` để hỗ trợ truyền thêm tham số đọc CSV như `dtype` và `keep_default_na`.
2. Cập nhật `process_orders()` để nhận DataFrame từ bên ngoài. Nếu đã nhận dữ liệu thì sử dụng lại, không đọc file lần thứ hai.
3. Cập nhật `pipeline.py` để truyền DataFrame `orders` vào `process_orders(orders)`.

Giải pháp giữ nguyên logic chuẩn hóa ngày, số tiền, phân loại dữ liệu hợp lệ và dữ liệu bị từ chối.

## 4. Kết quả đo trước và sau tối ưu

Thực hiện đo 3 lần cho mỗi phiên bản. Phạm vi đo gồm đọc dữ liệu khách hàng, đọc dữ liệu đơn hàng, thống kê dữ liệu và xử lý đơn hàng.

| Lần đo | Trước tối ưu (giây) | Sau tối ưu (giây) |
|---|---:|---:|
| Lần 1 | 3.6993 | 3.0662 |
| Lần 2 | 3.0727 | 2.9642 |
| Lần 3 | 3.1156 | 2.9964 |
| **Trung vị** | **3.1156** | **2.9964** |

### Các chỉ số đánh giá

- Thời gian trước tối ưu: 3.1156 giây.
- Thời gian sau tối ưu: 2.9964 giây.
- Thời gian giảm: 0.1192 giây.
- Tỷ lệ cải thiện: khoảng 3.83%.

Công thức:

Tỷ lệ cải thiện = (Thời gian trước - Thời gian sau) / Thời gian trước × 100%

## 5. Đánh giá

Sau khi tối ưu, thời gian thực thi của phạm vi đo giảm khoảng 3.83% so với phiên bản ban đầu.

Việc tái sử dụng DataFrame giúp loại bỏ thao tác đọc CSV trùng lặp, đồng thời giữ nguyên các bước xử lý dữ liệu hiện có.

Mức cải thiện thực tế không quá lớn, nhưng giải pháp giúp quy trình ETL gọn hơn và tránh lãng phí thao tác đọc dữ liệu.

## 6. Phạm vi và giới hạn đo

- Mỗi phiên bản được đo 3 lần.
- Sử dụng thời gian trung vị để hạn chế ảnh hưởng của dao động giữa các lần chạy.
- Kết quả trên phản ánh riêng phạm vi đọc dữ liệu, thống kê và xử lý đơn hàng; không đại diện cho tổng thời gian chạy toàn bộ pipeline ETL.
- Thời gian thực tế có thể thay đổi theo cấu hình máy và trạng thái hệ thống.

## 7. Kết luận

Đã hoàn thành tối ưu việc đọc dữ liệu đơn hàng bằng cách tái sử dụng DataFrame trong pipeline ETL.

Kết quả đo ghi nhận thời gian trung vị giảm từ 3.1156 giây xuống 2.9964 giây, tương ứng mức cải thiện khoảng 3.83%.
