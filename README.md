# Smart CRM — Track SE: Tiếp nhận và Phân loại Yêu cầu Bảo hành (Luồng L02)

Dự án Chuyên đề Tốt nghiệp 1 (Khoa CNTT, Trường Đại học Văn Lang).  
Hệ thống quản lý tiếp nhận thiết bị, tra cứu khách hàng, đối soát thời hạn bảo hành và tính toán cam kết SLA tự động cho chuỗi bán lẻ Smart CRM – Mekong Mobile.

---

## Thông tin sinh viên & Học phần

- **Họ và tên sinh viên:** Nguyễn Trương Đức Huy
- **Mã số sinh viên (MSSV):** 2374802010186
- **Lớp / Nhóm học phần:** 261_71ITGR40203_05
- **Chuyên ngành (Track):** Software Engineering (SE)
- **Mã luồng nghiệp vụ:** Luồng L02 – Tiếp nhận và Phân loại Yêu cầu Bảo hành
- **Repository GitHub:** `smartcrm-2374802010186-tiep-nhan-bao-hanh` (Nhánh `dev`)

---

## 1. Mô tả bài toán & Hệ thống làm được gì

Mekong Mobile chưa có hệ thống CRM tập trung; quy trình tiếp nhận bảo hành hoàn toàn thực hiện thủ công bằng phiếu giấy. Hệ thống Smart CRM Luồng L02 giải quyết các điểm nghẽn nghiệp vụ:

- **Tra cứu & Chuẩn hóa Khách hàng:** Nhập số điện thoại bất kỳ (ví dụ: `+84 908 123 456`, `84908123456`), hệ thống tự động chuẩn hóa về dạng 10 số `0908123456` (**QT-01**, **QT-02**) và che số điện thoại hiển thị dạng `090****456` (**QT-15**).
- **Ghi nhận & Kiểm tra Thiết bị:** Nhập số IMEI/Serial duy nhất (**QT-03**) và ngày mua từ hóa đơn; hệ thống tự động kiểm tra điều kiện bảo hành còn hạn hay hết hạn (**QT-05**).
- **Tính toán SLA Tự động:** Nhập thông tin sự cố; hệ thống tự động đề xuất mức ưu tiên và tính hạn cam kết trả máy `due_date` theo giờ làm việc T2–T7 (24h/72h/120h), **tự động nhảy qua ngày Chủ Nhật** (**QT-04**).
- **Khởi tạo Phiếu Bảo hành:** Sinh mã phiếu duy nhất dạng `BH-XXXXXX/2026`, gán trạng thái `MỚI` và tự động ghi nhật ký lịch sử chuyển trạng thái vào bảng `ticket_status_log` (**QT-06**).
- **Quản lý & Đôn đốc SLA:** Tra cứu phiếu theo IMEI/mã phiếu, lọc danh sách phiếu quá hạn hoặc sắp quá hạn SLA (<4h).

---

## 2. Phạm vi bài toán

###  Làm (Trong phạm vi CĐTN1):
1. Tra cứu và chuẩn hóa SĐT khách hàng; tự tạo hồ sơ khách hàng mới khi chưa tồn tại.
2. Ghi nhận IMEI/Serial thiết bị và đối soát hạn bảo hành 12 tháng từ ngày mua.
3. Phân loại nhóm sự cố, mức ưu tiên và tự động tính hạn cam kết SLA `due_date` (nhảy ngày Chủ Nhật).
4. Khởi tạo phiếu bảo hành `BH-XXXXXX/2026`, lưu vết trạng thái đầu tiên vào `ticket_status_log`.
5. Hiển thị danh sách phiếu bảo hành của trung tâm, hỗ trợ lọc theo trạng thái và đôn đốc phiếu quá hạn SLA.
6. Bảo mật thông tin khách hàng: che số điện thoại dạng `090****456` đối với nhân viên tiếp nhận.

### ❌ Không làm (Ngoài phạm vi CĐTN1):
1. Không điều phối và xuất linh kiện kho (thuộc Luồng L05).
2. Không phân công kỹ thuật viên nâng cao theo tay nghề và định mức tải (thuộc Luồng L04).
3. Không tích hợp thanh toán trực tuyến hay thu phí bảo hành ngoài phạm vi.
4. Không gửi tin nhắn SMS / Zalo thật cho khách hàng (WON'T).

---

## 3. Công nghệ sử dụng (Tech Stack)

| Thành phần | Công nghệ chọn lựa | Lý do chọn lựa |
| :--- | :--- | :--- |
| **Ngôn ngữ / Runtime** | Python 3.11+ | Đã quen thuộc, cú pháp rõ ràng, xử lý logic nhanh |
| **API Framework** | FastAPI + Uvicorn | Tự động kiểm tra dữ liệu qua Pydantic, hiệu năng cao |
| **Cơ sở dữ liệu** | PostgreSQL 16 (hoặc SQLite local) | CSDL quan hệ chuẩn 3NF, hỗ trợ B-Tree Index tra cứu |
| **Kiểm thử (Testing)** | `unittest` (Standard Library) | Chạy độc lập 1 lệnh, không phụ thuộc thư viện ngoài |
| **Đóng gói & Chạy** | Dockerfile + Docker Compose | Đảm bảo tính tái lập (reproducibility) trên mọi máy |

---

## 4. Yêu cầu môi trường & Hướng dẫn cài đặt / chạy hệ thống

### Yêu cầu môi trường tối thiểu:
- **Docker Engine 24+** & **Docker Compose v2** (nếu chạy Docker) HOẶC **Python 3.11+** & **PostgreSQL 16** (nếu chạy Cục bộ).
- Cổng **8000** (API) và cổng **5432** (Database) còn trống.

###  Cách 1: Chạy hệ thống bằng Docker Compose (Chỉ 2 lệnh)

```bash
# Bước 1: Sao chép file cấu hình môi trường
cp .env.example .env

# Bước 2: Dựng và khởi chạy toàn bộ hệ thống
docker compose up -d --build
```

###  Cách 2: Chạy trực tiếp trên máy cá nhân (Local Python + PostgreSQL)

```bash
# Bước 1: Clone repository và truy cập thư mục dự án
git clone <your-repository-url>
cd smartcrm-2374802010186-tiep-nhan-bao-hanh

# Bước 2: Tạo và kích hoạt môi trường ảo Python
python3 -m venv .venv
source .venv/bin/activate    # Trên Windows: .venv\Scripts\activate

# Bước 3: Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Bước 4: Tạo file cấu hình môi trường .env
cp .env.example .env

# Bước 5: Khởi tạo CSDL PostgreSQL và nạp dữ liệu mẫu
psql -U postgres -d smartcrm_db -f db/schema.sql
psql -U postgres -d smartcrm_db -f db/seed.sql

# Bước 6: Khởi chạy Uvicorn server
uvicorn src.main:app --reload --port 8000
```

---

## 5. Kiểm tra hệ thống đã chạy đúng (Smoke Test & Healthcheck)

```bash
# 1. Kiểm tra Healthcheck Endpoint
curl -s http://localhost:8000/health
# Trả về: {"status":"ok","db":"ok"}

# 2. Lấy danh sách phiếu bảo hành mẫu (Nạp tự động từ db/seed.sql)
curl -s http://localhost:8000/api/v1/tickets | head -c 400

# 3. Tiếp nhận một thiết bị bảo hành mới (Khởi tạo phiếu)
curl -s -X POST http://localhost:8000/api/v1/tickets   -H "Content-Type: application/json"   -d "{\"customer_phone\": \"090 812 3456\", \"serial_no\": \"SN-A52-778901\", \"purchase_date\": \"2026-01-15\", \"category_id\": 1, \"issue_desc\": \"Màn hình chớp nháy sọc ngang không hiển thị\", \"priority\": \"CAO\"}"
```

---

## 6. Chạy bộ kiểm thử (Unit Tests)

```bash
python3 -m unittest tests/test_sprint1.py
```

Bộ kiểm thử gồm **8/8 test cases** thuộc đủ 3 loại bắt buộc (100% PASS):
- **Luồng đúng (Happy path):** Chuẩn hóa SĐT (`QT-01`, `QT-02`), Masking SĐT (`QT-15`), Sinh mã phiếu `BH-XXXXXX/2026`, đối soát hạn bảo hành (`QT-05`), tính đúng SLA 24h mức CAO.
- **Giá trị biên (Edge cases):** Thuật toán SLA tự động **nhảy qua ngày Chủ Nhật** (`QT-04`).
- **Dữ liệu sai / Ngoại lệ (Invalid inputs):** Từ chối SĐT không đúng định dạng, từ chối mô tả lỗi `<10` ký tự, từ chối trùng phiếu mở đang xử lý trên cùng thiết bị (`QT-03`, `QT-09`).

---

## 7. Cấu trúc thư mục (Clean Architecture - 4 Lớp)

```text
smartcrm-2374802010186-tiep-nhan-bao-hanh/
├── db/                             # Script CSDL PostgreSQL
│   ├── schema.sql                  # DDL 3NF (customer, device, issue_category, ticket, ticket_status_log)
│   └── seed.sql                    # Dữ liệu danh mục & dữ liệu mẫu nạp tự động
├── docs/                           # Tài liệu đính kèm & Sơ đồ thiết kế
│   ├── diagrams/                   # Sơ đồ .drawio (erd.drawio, wireframe.drawio)
│   ├── screenshots/                # Ảnh chụp minh chứng giao diện M1, M2, M3, E2E và Test
│   ├── ai-disclosure.md            # Bảng Khai báo Minh bạch AI
│   ├── api-docs.md                 # Tài liệu Đặc tả REST API Contracts
│   ├── bao_cao_buoi_10_sprint_2.docx # Báo cáo Word hoàn chỉnh Sprint 2 (kèm hình ảnh & bảng kiểm chứng)
│   ├── postman_collection.json     # Bộ kiểm thử REST API qua Postman
│   ├── srs.md                      # Tài liệu Đặc tả Yêu cầu Hệ thống SRS
│   └── thay-doi-thiet-ke.md       # Nhật ký Điều chỉnh Thiết kế (TD-01, TD-02, TD-03)
├── src/                            # Mã nguồn ứng dụng Python / FastAPI
│   ├── core/                       # Config CSDL & Biến môi trường
│   ├── repositories/              # Tầng 3 — Data Access Layer (PostgreSQL & in-memory)
│   ├── routes/                     # Tầng 1 — Controller nhận HTTP & validate schema
│   ├── schemas/                    # Pydantic validation models
│   ├── services/                   # Tầng 2 — Business Logic (QT-01 -> QT-15)
│   ├── static/                     # Giao diện Web (HTML5, CSS Inter theme, API Client layer)
│   └── main.py                     # Entry point khởi chạy FastAPI & mount frontend
├── tests/                          # Bộ kiểm thử tự động Unit Tests (8/8 PASS 100%)
│   └── test_sprint1.py
├── .env.example                    # Cấu hình biến môi trường mẫu
├── .gitignore                      # Danh sách loại trừ Git
├── README.md                       # Tài liệu hướng dẫn & Báo cáo tổng quan
└── requirements.txt                # Khai báo các thư viện Python
```

### Phép thử ranh giới tầng (Layer Boundary Check):
```bash
# 1. Tầng Services KHÔNG chứa đối tượng HTTP (Request, Response, status_code)
grep -rn "Request\|Response\|status_code" src/services/*.py

# 2. Tầng Repositories KHÔNG chứa quy tắc nghiệp vụ (calculate_due_date, normalize_phone)
grep -rn "calculate_due_date\|normalize_phone" src/repositories/*.py
```

---

## 8. Trạng thái hiện tại & Bảng tự kiểm (Sprint 2 / Buổi 10 Checklist)

- [x] **Cấu trúc 4 lớp Clean Architecture:** Phân tách rõ ràng giữa Routes, Services, Repositories, Schemas.
- [x] **CSDL PostgreSQL 3NF:** Script `db/schema.sql` và `db/seed.sql` tạo bảng và nạp dữ liệu mẫu thành công.
- [x] **Module cốt lõi Sprint 1 & 2:** Hiện thực `CustomerService`, `SLAService`, `TicketService` đúng quy tắc.
- [x] **Unit Tests:** 8/8 test cases PASS 100% bằng 1 lệnh `python3 -m unittest tests/test_sprint1.py`.
- [x] **Tích hợp End-to-End:** Toàn bộ luồng L02 chạy thông suốt từ Tra cứu -> Tính SLA/Bảo hành -> Khởi tạo phiếu -> Ghi log.
- [x] **3 Màn hình Giao diện:** Hoàn thiện M1, M2, M3 kết nối API qua tầng Client duy nhất, xử lý đủ 3 trạng thái (Loading / Empty / Error).
- [x] **Tài liệu đính kèm:** `docs/srs.md`, `docs/thay-doi-thiet-ke.md`, `docs/ai-disclosure.md`, `docs/api-docs.md`, `docs/bao_cao_buoi_10_sprint_2.docx`.

---

## 9. Danh mục tài liệu đính kèm (`docs/`)

| Tệp | Nội dung mô tả |
| :--- | :--- |
| `docs/bao_cao_buoi_10_sprint_2.docx` | Báo cáo Thực hành Word hoàn chỉnh có chèn đầy đủ hình ảnh & bảng kiểm chứng |
| `docs/screenshots/` | Thư mục lưu ảnh chụp màn hình minh chứng chạy toàn luồng và kết quả test |
| `docs/postman_collection.json` | Bộ sưu tập Postman Collection kiểm thử đầy đủ các REST API endpoints |
| `docs/srs.md` | Tài liệu Đặc tả Yêu cầu Hệ thống SRS rút gọn 8 mục |
| `docs/api-docs.md` | Tài liệu Đặc tả REST API Contracts (Endpoints, Request/Response JSON, Validation) |
| `docs/thay-doi-thiet-ke.md` | Nhật ký Điều chỉnh Thiết kế (`TD-01` log trạng thái, `TD-02` SLA Chủ Nhật, `TD-03` Index) |
| `docs/ai-disclosure.md` | Bảng Khai báo Minh bạch Sử dụng Công cụ AI |
| `docs/diagrams/erd.drawio` | Sơ đồ Mô hình Dữ liệu Quan hệ ERD 3NF (5 thực thể) |
| `docs/diagrams/wireframe.drawio` | Sơ đồ Wireframe 3 màn hình nghiệp vụ M1, M2, M3 |

---

## 10. Khai báo sử dụng công cụ AI (AI Disclosure Summary)

| Công cụ AI | Áp dụng ở phần nào | Cách sử dụng (Tóm tắt Prompt) | Em đã kiểm chứng / chỉnh sửa gì |
| :--- | :--- | :--- | :--- |
| **Trợ lý AI dạng chat** | Khung mã nguồn & Unit Tests | Gợi ý cấu trúc Clean Architecture 4 lớp Python & test cases SLA | Tự kiểm thử với `unittest`, sửa logic SLA bỏ qua ngày Chủ Nhật và kiểm tra ràng buộc ngoại lệ |
