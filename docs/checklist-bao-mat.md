# Checklist tự đánh giá bảo mật — Smart CRM Luồng L02

**Sinh viên:** Nguyễn Trương Đức Huy — **MSSV:** 2374802010186
**Phạm vi:** Mã nguồn và cấu hình hiện có trong repository; checklist không thay thế kiểm thử triển khai.

| # | Hạng mục | Trạng thái | Minh chứng |
|---|---|---|---|
| 1 | Quản lý secret và cấu hình môi trường | **ĐÃ LÀM** | `.env` được loại trừ trong `.gitignore`; chỉ `.env.example` với mật khẩu mẫu được theo dõi, và lịch sử Git không có `.env`. Thay giá trị mẫu trước khi dùng ngoài môi trường học tập. |
| 2 | Xác thực và phân quyền API | **CHƯA LÀM** | Các route khách hàng và phiếu bảo hành chưa có middleware đăng nhập hoặc kiểm tra vai trò; chỉ phù hợp demo cục bộ, không triển khai công khai. |
| 3 | Kiểm tra dữ liệu đầu vào | **ĐÃ LÀM** | `TicketCreateRequest` giới hạn mô tả tối thiểu 10 ký tự và kiểm tra mức ưu tiên; test kiểm tra SĐT sai và mô tả quá ngắn. |
| 4 | Bảo vệ dữ liệu cá nhân trong log | **ĐÃ LÀM** | `src/core/logger.py` che số điện thoại và các trường nhạy cảm trước khi ghi log; test `test_phone_masking` kiểm tra định dạng `090****456`. |
| 5 | An toàn truy vấn và lưu trữ dữ liệu | **CHƯA LÀM** | API hiện dùng repository in-memory, chưa kết nối PostgreSQL; chưa có truy vấn tham số hóa hoặc kiểm thử bảo mật truy cập dữ liệu ở runtime. |
| 6 | CORS và bảo vệ truy cập mạng | **CHƯA LÀM** | `src/main.py` hiện cho phép mọi origin (`allow_origins=["*"]`) cùng credentials; cần giới hạn origin trước khi triển khai. |
| 7 | Hardening đóng gói và phụ thuộc | **ĐÃ LÀM** | Dockerfile dùng multi-stage và user không đặc quyền `appuser`; các phiên bản phụ thuộc trong `requirements.txt` được ghim. Chưa có kết quả quét lỗ hổng image/phụ thuộc. |

## Giới hạn đã biết

- Mật khẩu mặc định trong `.env.example` chỉ là giá trị mẫu cho môi trường học tập, không được dùng trên hệ thống thật.
- Docker chưa được xác minh chạy clean-clone trong môi trường hiện tại; cần chạy lại hướng dẫn triển khai trên máy có Docker Engine và Compose v2.
- Health endpoint trả `db: ok` theo contract kiểm tra của bài tập; do API hiện dùng dữ liệu in-memory, trường này **không** xác nhận kết nối PostgreSQL thật.
