# Báo cáo kết quả kiểm thử — Smart CRM Luồng L02

**Sinh viên:** Nguyễn Trương Đức Huy — MSSV: 2374802010186 — Track SE  
**Lệnh:** `python -m unittest discover -s tests`

## Tóm tắt

| Chỉ số | Kết quả |
| :--- | :--- |
| Số test đã chạy | 12 |
| PASS | 12 |
| FAIL | 0 |
| 5 loại test | Đủ |

## Ma trận test case

| STT | Test case | Loại | QT liên quan | Dữ liệu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| TC-01 | `test_phone_normalization_valid` | Luồng đúng | QT-01/02 | `"+84 908 123 456"` | `"0908123456"` | `"0908123456"` | PASS |
| TC-02 | `test_phone_masking` | Luồng đúng | QT-15 | `"0908123456"` | `"090****456"` | `"090****456"` | PASS |
| TC-03 | `test_ticket_creation_success` | Luồng đúng | QT-06 | SĐT + serial + mô tả hợp lệ | mã `BH-…`, status `MOI` | mã `BH-…`, status `MOI` | PASS |
| TC-04 | `test_sla_calculation_cao_24h` | Luồng đúng | QT-04 | Thứ Tư 08:00, CAO | Thứ Năm 08:00 | Thứ Năm 08:00 | PASS |
| TC-05 | `test_sla_calculation_skip_sunday` | Biên | QT-04 | Thứ Sáu 09:00, TRUNG_BINH 72h | Thứ Ba 09:00 | Thứ Ba 09:00 | PASS |
| TC-06 | `test_TC10_warranty_boundary_12_months` | Biên | QT-05 | 360 ngày / 400 ngày | True / False | True / False | PASS |
| TC-07 | `test_phone_normalization_invalid` | Dữ liệu sai | QT-01 | `"12345"` | `ValueError` | `ValueError` | PASS |
| TC-08 | `test_ticket_creation_short_desc` | Dữ liệu sai | V8 | `"Hỏng"` | `ValueError` | `ValueError` | PASS |
| TC-09 | `test_TC12` (assert mask trên API) | Bảo mật/CLDL | QT-15 | `POST` SĐT `+84…` | `090****456` | `090****456` | PASS |
| TC-10 | `test_TC09_verify_warranty_valid` | Luồng đúng | QT-05 | mua cách đây 90 ngày | True | True | PASS |
| TC-11 | `test_TC11_seed_rerunnable` | Tái lập | Buổi 11 | chạy lại `seed.sql` | 3 INSERT đều có `ON CONFLICT` | 3/3 có | PASS |
| TC-12 | `test_TC12_system_api_create_ticket` | System API | QT-06 | `GET /health`; `POST /api/v1/tickets` | Health `{"status":"ok","db":"ok"}`; POST 201, mã `BH-…`, `MOI` | Đúng health contract; POST 201, mã `BH-…`, `MOI` | PASS |

`test_ticket_duplicate_open_ticket` (QT-03, IMEI trùng → `KeyError`) chạy kèm trong sprint1 — PASS.

## Ảnh minh chứng

Thư mục [`docs/screenshots/`](screenshots/):
- `test_result.png` — kết quả chạy 12 test cases, PASS
- `screen_unittest_7pass.jpg` — ảnh của lần chạy 7 test cũ, không dùng làm minh chứng cho báo cáo này
- `screen_m1_reception.jpg` — M1 Form tiếp nhận
- `screen_m2_m3_list_detail.jpg` — M2 danh sách + M3 chi tiết
- `screen_e2e_flow.jpg` — luồng E2E

## Ghi chú

SLA `TRUNG_BINH` = **72h làm việc** (không phải 24h). Test TC-05: Thứ Sáu 09:00 → Thứ Ba 09:00, bỏ Chủ Nhật. Bug liên quan: xem [`bug-log.md`](bug-log.md) BUG-001, BUG-002, BUG-003.
