# Smart CRM — Track SE: Tiếp nhận và Phân loại Yêu cầu Bảo hành (Luồng L02)

Dự án Chuyên đề tốt nghiệp 1 (Khoa CNTT, Trường Đại học Văn Lang).  
Ví dụ tham chiếu cho mức độ và cấu trúc hệ thống theo tiêu chuẩn Bài tập 2 và Bài tập 3 — Luồng L02: Tiếp nhận thiết bị vào bảo hành (Case study Smart CRM – Mekong Mobile).

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Trương Đức Huy
- **MSSV:** 2374802010186
- **Lớp:** 261_71ITGR40203_05
- **Chuyên ngành (Track):** Software Engineering (SE)
- **Phân hệ / Luồng:** Luồng L02 – Tiếp nhận và Phân loại Yêu cầu Bảo hành

---

## Hệ thống làm được gì

- **Tra cứu & Chuẩn hóa Khách hàng:** Nhập số điện thoại bất kỳ (ví dụ: `+84 908 123 456`, `84908123456`), hệ thống tự động chuẩn hóa về dạng 10 số `0908123456` (**QT-01**, **QT-02**) và che số điện thoại hiển thị dạng `090****456` (**QT-15**).
- **Ghi nhận & Kiểm tra Thiết bị:** Nhập số IMEI/Serial duy nhất (**QT-03**) và ngày mua từ hóa đơn; hệ thống tự động kiểm tra điều kiện bảo hành còn hạn hay hết hạn (**QT-05**).
- **Tính toán SLA Tự động:** Nhập thông tin sự cố; hệ thống tự động đề xuất mức ưu tiên và tính hạn cam kết trả máy `due_date` theo giờ làm việc T2–T7 (24h/72h/120h), **tự động nhảy qua ngày Chủ Nhật** (**QT-04**).
- **Khởi tạo Phiếu Bảo hành:** Sinh mã phiếu duy nhất dạng `BH-XXXXXX/2026`, gán trạng thái `MỚI` và tự động ghi nhật ký lịch sử chuyển trạng thái vào bảng `ticket_status_log` (**QT-06**).
- **Quản lý & Đôn đốc SLA:** Tra cứu phiếu theo IMEI/mã phiếu, lọc danh sách phiếu quá hạn hoặc sắp quá hạn SLA (<4h).

Các quy tắc nghiệp vụ cốt lõi đã hiện thực: **QT-01/02** (chuẩn hóa SĐT), **QT-03** (định danh IMEI/Serial duy nhất), **QT-04** (SLA tính theo giờ làm việc T2–T7 bỏ qua Chủ Nhật), **QT-05** (đối soát hạn bảo hành), **QT-06** (vòng đời phiếu & log trạng thái), **QT-15** (masking SĐT `090****456`).

---

## Yêu cầu môi trường

- **Cách 1 (Khuyên dùng khi chấm bài):** Docker Engine 24 trở lên và Docker Compose v2 (`docker compose version`).
- **Cách 2 (Chạy trực tiếp / Local Dev):** Python 3.11+ và PostgreSQL 15+ cài trực tiếp trên máy.

---

## Chạy hệ thống

### Cách 1: Chạy bằng Docker (Khuyên dùng)

```bash
cp .env.example .env
docker compose up -d --build
```

Kiểm tra hệ thống đã chạy đúng:
```bash
docker compose ps                      # Cột STATUS của db và api phải là "healthy" hoặc "running"
curl -s http://localhost:8000/health   # {"status":"ok","db":"ok"}
```

### Cách 2: Chạy trực tiếp trên máy (Không dùng Docker)

1. Tạo CSDL PostgreSQL cục bộ (ví dụ: `smartcrm_db`).
2. Nạp dữ liệu cấu trúc và dữ liệu mẫu:
   - Chạy script `db/schema.sql` để tạo bảng.
   - Chạy script `db/seed.sql` để nạp dữ liệu danh mục ban đầu.
3. Tạo file `.env` từ `.env.example` và cập nhật thông tin kết nối CSDL cục bộ:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=smartcrm_db
   ```
4. Cài đặt thư viện & Chạy Server FastAPI:
   ```bash
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

---

## Chạy bộ kiểm thử (Unit Tests)

Bộ kiểm thử có thể chạy trực tiếp **không cần Docker** và **không cần CSDL**:

```bash
python3 -m unittest tests/test_sprint1.py
```

Bộ kiểm thử gồm 6 test cases ở ba loại: **luồng đúng** (happy path), **giá trị biên** (edge cases - SLA nhảy qua Chủ Nhật), và **dữ liệu sai/ngoại lệ** (invalid inputs - SĐT sai, mô tả lỗi <10 ký tự).

---

## Cấu trúc thư mục (Clean Architecture - 4 Lớp)

```text
src/routes/          Tầng 1 — Controller nhận HTTP, validate schema, dịch response sang HTTP Status Code
src/services/        Tầng 2 — Business Logic, chứa các quy tắc nghiệp vụ (QT-01 -> QT-15), KHÔNG biết gì về HTTP
src/repositories/    Tầng 3 — Data Access Layer, tương tác PostgreSQL, KHÔNG chứa quy tắc nghiệp vụ
src/schemas/         Kiểm tra định dạng & cấu trúc dữ liệu vào (Pydantic models)
src/core/            Cấu hình kết nối CSDL và các cài đặt chung
db/                  Chứa schema.sql (DDL 3NF) và seed.sql (Dữ liệu mẫu nạp tự động)
tests/               Bộ kiểm thử tự động Unit Tests (test_sprint1.py)
docs/                Toàn bộ tài liệu đặc tả, sơ đồ kiến trúc, ERD, wireframe và nhật ký thiết kế
```

**Phép thử ranh giới tầng** (chạy được ngay trên Linux/macOS, phải trả về rỗng):

```bash
# Tầng Services KHÔNG được chứa đối tượng HTTP (Request, Response, status_code)
grep -rn "Request\|Response\|status_code" src/services/*.py

# Tầng Repositories KHÔNG được chứa quy tắc nghiệp vụ (calculate_due_date, normalize_phone)
grep -rn "calculate_due_date\|normalize_phone" src/repositories/*.py
```

---

## Tài liệu đính kèm (`docs/`)

| Tệp | Nội dung |
|---|---|
| `docs/srs.md` | Tài liệu Đặc tả Yêu cầu Hệ thống (SRS rút gọn 8 mục) |
| `docs/api-docs.md` | Tài liệu Đặc tả REST API Contracts (Endpoints, Request/Response, Validation Rules) |
| `docs/thay-doi-thiet-ke.md` | Nhật ký điều chỉnh thiết kế theo phản hồi thiết kế (`TD-01`, `TD-02`, `TD-03`) |
| `docs/ai-disclosure.md` | Bảng Khai báo Minh bạch Sử dụng Công cụ AI |
| `docs/diagrams/erd.drawio` | Sơ đồ Cơ sở Dữ liệu ERD 3NF (5 thực thể) |
| `docs/diagrams/wireframe.drawio` | Sơ đồ Wireframe 3 màn hình nghiệp vụ M1, M2, M3 |
| `docs/test-plan.md` | Kế hoạch kiểm thử rút gọn 4 mục |
| `docs/test-report.md` | Báo cáo kết quả chạy test cases |
| `docs/bug-log.md` | Bảng ghi vết lỗi và lịch sử sửa bug |
| `docs/deployment-guide.md` | Hướng dẫn triển khai hệ thống |
| `docs/checklist-bao-mat.md` | Bảng tự đánh giá an toàn bảo mật |
