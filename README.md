# Smart CRM — Track SE: Tiếp nhận và Phân loại Yêu cầu Bảo hành (Luồng L02)

Dự án Chuyên đề tốt nghiệp 1 (Khoa CNTT, Trường Đại học Văn Lang).

**Thông tin sinh viên:**
- **Họ và tên:** Nguyễn Trương Đức Huy
- **MSSV:** 2374802010186
- **Lớp:** 261_71ITGR40203_05
- **Chuyên ngành (Track):** Software Engineering (SE)
- **Phân hệ / Luồng:** Luồng L02 – Tiếp nhận và Phân loại Yêu cầu Bảo hành

---

## Hệ thống làm được gì

- **Tra cứu & Chuẩn hóa Khách hàng:** Nhập SĐT bất kỳ (`+84 908 123 456`, `84908123456`), hệ thống tự động chuẩn hóa về dạng 10 số `0908123456` (**QT-01**, **QT-02**) và che số điện thoại hiển thị dạng `090****456` (**QT-15**).
- **Ghi nhận & Kiểm tra Thiết bị:** Nhập số IMEI/Serial duy nhất (**QT-03**) và ngày mua từ hóa đơn; hệ thống tự động kiểm tra điều kiện bảo hành còn hạn hay hết hạn (**QT-05**).
- **Tính toán SLA Tự động:** Nhập thông tin sự cố; hệ thống tự động đề xuất mức ưu tiên và tính hạn cam kết trả máy `due_date` theo giờ làm việc T2–T7 (24h/72h/120h), **tự động nhảy qua ngày Chủ Nhật** (**QT-04**).
- **Khởi tạo Phiếu Bảo hành:** Sinh mã phiếu duy nhất dạng `BH-XXXXXX/2026`, gán trạng thái `MỚI` và tự động ghi nhật ký lịch sử chuyển trạng thái vào bảng `ticket_status_log` (**QT-06**).
- **Quản lý & Đôn đốc SLA:** Tra cứu phiếu theo IMEI/mã phiếu, lọc danh sách phiếu quá hạn hoặc sắp quá hạn SLA (<4h).
- **3 Màn hình Frontend (Sprint 2):** M1 (Tạo phiếu), M2 (Danh sách & Lọc SLA), M3 (Chi tiết & Log trạng thái).
- **DataState 3 trạng thái:** Loading (spinner), Empty (khi lọc rỗng), Error (lỗi mạng kèm nút Retry).

Các quy tắc nghiệp vụ đã hiện thực: **QT-01/02** (chuẩn hóa SĐT), **QT-03** (định danh IMEI/Serial duy nhất), **QT-04** (SLA tính theo giờ làm việc T2–T7 bỏ qua Chủ Nhật), **QT-05** (đối soát hạn bảo hành), **QT-06** (vòng đời phiếu & log trạng thái), **QT-15** (masking SĐT `090****456`).

---

## Yêu cầu môi trường

- **Python 3.11+** và pip
- **Không cần PostgreSQL** để chạy và kiểm thử (dữ liệu in-memory đồng bộ `db/seed.sql`)
- **Cần PostgreSQL 15+** chỉ khi muốn kết nối CSDL thật

---

## Chạy hệ thống (Cách 2 — Local Dev, không cần Docker)

```bash
# Bước 1: Clone repository
git clone <repo-url>
cd smartcrm-2374802010186-tiep-nhan-bao-hanh
```

```bash
# Bước 2: Tạo file môi trường
cp .env.example .env
```

```bash
# Bước 3: Cài đặt thư viện Python
pip install -r requirements.txt
```

```bash
# Bước 4: Chạy Unit Tests (không cần DB, không cần Docker)
python -m unittest tests/test_sprint1.py -v
```

```bash
# Bước 5: Khởi động Backend API
uvicorn src.main:app --reload
```

```bash
# Bước 6: Mở Frontend trên trình duyệt
# Truy cập: http://localhost:8000
```

---

## Chạy bộ kiểm thử (Unit Tests)

Bộ kiểm thử chạy trực tiếp **không cần Docker** và **không cần CSDL**:

```bash
python -m unittest tests/test_sprint1.py -v
```

Bộ kiểm thử gồm **8 test cases** chia làm 3 nhóm:
1. **Luồng đúng (Happy path):** Chuẩn hóa SĐT hợp lệ, Masking SĐT, Tạo phiếu thành công.
2. **Giá trị biên (Edge cases):** SLA nhảy qua Chủ Nhật (QT-04), SLA mức CAO 24h.
3. **Dữ liệu sai / Ngoại lệ:** SĐT không hợp lệ, Mô tả lỗi <10 ký tự (V8), Trùng phiếu mở (QT-03/QT-09).

---

## Cấu trúc thư mục (Clean Architecture — 4 Lớp)

```text
src/routes/          Tầng 1 — Controller HTTP, validate schema, dịch HTTP Status Code
src/services/        Tầng 2 — Business Logic (QT-01 → QT-15), KHÔNG biết gì về HTTP
src/repositories/    Tầng 3 — Data Access Layer, tương tác CSDL, KHÔNG chứa nghiệp vụ
src/schemas/         Kiểm tra định dạng & cấu trúc dữ liệu vào (Pydantic models)
src/core/            Cấu hình kết nối CSDL và cài đặt chung
src/static/          Frontend SPA (3 màn hình M1, M2, M3) — Track SE Module mở rộng
  ├── index.html     Cấu trúc HTML 3 màn hình + sidebar navigation
  ├── css/app.css    Design system dark theme (navy/teal)
  └── js/
      ├── api/       Tầng API Client (client.js + ticket.api.js)
      └── app.js     Controller chính M1/M2/M3
db/                  schema.sql (DDL 3NF) + seed.sql (Dữ liệu mẫu)
tests/               Bộ kiểm thử Unit Tests — 8/8 PASS (test_sprint1.py)
docs/                Tài liệu đặc tả, sơ đồ kiến trúc, ERD, wireframe
docs/screenshots/    Ảnh chụp màn hình minh chứng chạy toàn luồng
```

**Kiểm tra tính phân tầng** (phải trả về rỗng):
```bash
# Tầng Services KHÔNG được chứa đối tượng HTTP
grep -rn "Request\|Response\|status_code" src/services/

# Tầng Frontend KHÔNG được gọi fetch() trực tiếp (phải qua api/client.js)
grep -rn "fetch(" src/static/js/app.js src/static/js/api/ticket.api.js
```

---

## API Endpoints (Sprint 2)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `POST` | `/api/v1/customers/search` | Tra cứu KH theo SĐT (QT-01, QT-02, QT-15) |
| `POST` | `/api/v1/tickets` | Tạo phiếu bảo hành mới (QT-03 → QT-06) |
| `GET`  | `/api/v1/tickets` | Danh sách phiếu + lọc SLA (US7) |
| `GET`  | `/api/v1/tickets/{ticket_code}` | Chi tiết phiếu kèm log (M3) |
| `GET`  | `/api/v1/categories` | Danh sách nhóm sự cố |
| `GET`  | `/api/health` | Health check |

---

## Commit History (Conventional Commits)

Toàn bộ commits tuân thủ chuẩn [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`

Tổng số commits ≥ 8 trên nhánh `dev`.
