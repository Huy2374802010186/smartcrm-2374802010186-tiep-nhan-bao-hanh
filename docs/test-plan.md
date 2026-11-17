# Kế hoạch kiểm thử — Smart CRM Luồng L02

**Sinh viên:** Nguyễn Trương Đức Huy — MSSV: 2374802010186 — Track SE  
**Phạm vi:** Buổi 13–14 · unittest Python 3.11+

## 1. Phạm vi kiểm thử (Scope)

**In-scope (Luồng L02):**
- QT-01 / QT-02 — Chuẩn hóa SĐT (`+84` / `84` / khoảng trắng → `0908123456`)
- QT-15 — Masking SĐT (`090****456`)
- QT-03 — IMEI/serial duy nhất (không trùng phiếu mở)
- QT-04 — SLA bỏ qua Chủ Nhật
- QT-05 — Hạn bảo hành 12 tháng
- QT-06 — Sinh mã `BH-XXXXXX/2026`, status `MOI`

**Out-of-scope:** Xuất kho linh kiện (L05), Phân công kỹ thuật viên (L04).

## 2. Kim tự tháp kiểm thử (12 test)

| Tầng | Số lượng | File | Test |
| :--- | :---: | :--- | :--- |
| Unit | 7 | `tests/test_sprint1.py`, `tests/test_sprint3.py` | chuẩn hóa/mask SĐT, SLA, bảo hành 12 tháng, SĐT sai, mô tả ngắn |
| Integration | 3 | `tests/test_sprint1.py`, `tests/test_sprint3.py` | tạo phiếu thành công, IMEI trùng, seed SQL `ON CONFLICT` |
| System API | 2 | `tests/test_sprint3.py` + unit SLA CAO | `POST /api/v1/tickets` → 201; SLA CAO 24h |

Lệnh chạy: `python -m unittest discover -s tests`

## 3. Tiêu chí thành công

- 12/12 test `PASS` (`OK`)
- Phủ đủ 5 loại: luồng đúng, biên, dữ liệu sai, bảo mật/chất lượng dữ liệu (mask SĐT), tái lập (seed SQL)

## 4. Môi trường & dữ liệu thử

- Python 3.11+ · `unittest` · FastAPI `TestClient`
- PostgreSQL 16 (nạp `db/schema.sql`, `db/seed.sql`) — test tái lập kiểm tra `ON CONFLICT DO NOTHING`
- Dữ liệu mẫu: SĐT `+84 908 123 456` → `0908123456` / `090****456`; serial `SN-TC12-999001`
