# Nhật ký Điều chỉnh Thiết kế (Design Change Log)
**Dự án:** Smart CRM – Mekong Mobile (Phân hệ L02 - Tiếp nhận & Phân loại Bảo hành)
**Sinh viên:** Nguyễn Trương Đức Huy – MSSV: 2374802010186 – Track SE

---

## 1. Sau phản hồi Bài tập 1 (Buổi 8, ngày 19/10/2026)

### TD-01: Bổ sung Bảng Lịch sử Trạng thái (`ticket_status_log`)
- **Phản hồi của GV:** Cột `status` trong bảng `ticket` nếu bị ghi đè sẽ không theo dõi được lịch sử chuyển đổi và thời gian xử lý thực tế của từng bước trong vòng đời.
- **Quyết định:** SỬA
- **Lý do:** Đáp ứng quy tắc **QT-06** (mọi lần chuyển trạng thái phải ghi vết) và phục vụ yêu cầu đôn đốc tiến độ SLA.
- **Ảnh hưởng:** Giữ nguyên bảng `ticket_status_log` trong ERD, file DDL `db/schema.sql` và khởi tạo tự động 1 bản ghi log khi gọi API `POST /api/v1/tickets`.

---

### TD-02: Làm rõ Thuật toán SLA tự động bỏ qua ngày Chủ Nhật
- **Phản hồi của GV:** Cần làm rõ cách tính `due_date` khi thời gian tiếp nhận rơi vào chiều Thứ Sáu hoặc Thứ Bảy để không tính dồn giờ làm việc vào Chủ Nhật.
- **Quyết định:** SỬA
- **Lý do:** Quy tắc **QT-04** quy định thời hạn cam kết SLA (CAO: 24h, TRUNG_BINH: 72h, THAP: 120h) chỉ tính trong khung giờ làm việc từ Thứ 2 đến Thứ 7.
- **Ảnh hưởng:** Cập nhật hàm `calculate_due_date()` trong `SLAService` (`src/services/sla_service.py`) tự động kiểm tra và cộng thêm 24 giờ (1 ngày) nếu khoảng thời gian xử lý vắt qua ngày Chủ Nhật.

---

### TD-03: Giữ nguyên việc lưu thuộc tính `due_date` và `is_warranty` trong bảng `ticket`
- **Phản hồi của GV:** Cần giải thích lý do tại sao lưu `due_date` và `is_warranty` trực tiếp ở bảng `ticket` dù có thể tính toán từ `received_at` và `purchase_date`.
- **Quyết định:** GIỮ NGUYÊN
- **Lý do:** 
  1. `due_date` là mốc cam kết cố định tại thời điểm tiếp nhận (không được thay đổi retroactively khi bảng cấu hình SLA đổi). Cột này cũng cần đánh B-Tree Index để sắp xếp danh sách đôn đốc SLA dưới 300ms (NFR-01).
  2. `is_warranty` lưu vết quyết định đối soát tại thời điểm tiếp nhận phục vụ đối soát tài chính bảo hành.
- **Ảnh hưởng:** Giữ nguyên cấu trúc DDL bảng `ticket`.

---

## 2. Sau phản hồi Bài tập 2 (chấm BT2, TC2: C6 và S1 chưa đạt)

### TD-04: Khóa phiên bản dependencies trong `requirements.txt` (C6)
- **Phản hồi của GV:** `requirements.txt` dùng `>=` nên môi trường cài đặt không tái lập được, mục kiểm chứng C6 chưa đạt.
- **Quyết định:** SỬA
- **Lý do:** Khóa `==` đúng phiên bản đang chạy (FastAPI, Uvicorn, Pydantic, psycopg2-binary, SQLAlchemy, python-dotenv, httpx) để `pip install -r requirements.txt` tái lập đúng môi trường chấm bài.
- **Ảnh hưởng:** Chỉ đổi `requirements.txt`, không đổi code. Kiểm tra bằng `pip freeze`.

---

### TD-05: Bổ sung đủ CRUD cho 2 thực thể Ticket và Customer (S1)
- **Phản hồi của GV:** API mới có tạo (POST) và đọc (GET), chưa đủ bốn thao tác CRUD cho hai thực thể, mục kiểm chứng S1 chưa đạt.
- **Quyết định:** SỬA
- **Lý do:** Đáp ứng S1 — mỗi thực thể `ticket` và `customer` đều có đủ Create / Read / Update / Delete.
- **Ảnh hưởng:**
  - Thực thể Ticket (`src/routes/ticket_routes.py`, `src/repositories/ticket_repository.py`): thêm `PATCH /api/v1/tickets/{ticket_code}` (đổi trạng thái + ghi `status_log`, QT-06) và `DELETE /api/v1/tickets/{ticket_code}`; repository thêm `update_status()` và `delete()`.
  - Thực thể Customer (`src/routes/customer_routes.py`, `src/repositories/customer_repository.py`): thêm `GET /api/v1/customers`, `POST /api/v1/customers`, `PATCH /api/v1/customers/{phone}`, `DELETE /api/v1/customers/{phone}`; repository thêm `list_all()`, `create()`, `update()`, `delete()`.
  - SĐT đầu vào các endpoint customer đều qua `CustomerService.normalize_phone()` (QT-01/02), trùng SĐT trả 409.
