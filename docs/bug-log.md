# Nhật ký Gỡ lỗi Hệ thống (Bug Log)
**Học phần:** Chuyên đề Tốt nghiệp 1 (HK1 / 2026–2027)  
**Sinh viên:** Nguyễn Trương Đức Huy — **MSSV:** 2374802010186 — **Track:** Software Engineering (SE)  
**Phân hệ:** Luồng L02 – Tiếp nhận và Phân loại Yêu cầu Bảo hành (Smart CRM – Mekong Mobile)  
**Quy chuẩn ghi chép:** Đầy đủ 7 dòng theo hướng dẫn Bài tập 2 & Bài tập 3 (Buổi 11 / Buổi 12).

---

## 1. BUG-001 · Major — Thuật toán tính hạn cam kết SLA tính gộp cả ngày Chủ Nhật

| Dòng | Nội dung |
| :--- | :--- |
| **1. Mã và mức độ** | `BUG-001` · **Major** (Hạn SLA cam kết bị sai lệch đối với phiếu tiếp nhận vào cuối tuần). |
| **2. Phát hiện bởi** | Unit test case `test_sla_calculation_skip_sunday` trong `tests/test_sprint1.py`. |
| **3. Triệu chứng** | Phiếu mức `TRUNG_BINH` (72h) tiếp nhận lúc 09:00 Thứ Sáu trả về `due_date` là 09:00 Thứ Hai (thực tế chỉ có 24h làm việc Thứ Bảy). |
| **4. Cách tái lập** | `python -c "from src.services.sla_service import SLAService; from datetime import datetime; print(SLAService.calculate_due_date(datetime(2026, 10, 16, 9, 0), 'TRUNG_BINH'))"` |
| **5. Nguyên nhân** | `SLAService.calculate_due_date()` cộng trực tiếp `timedelta(hours=target_hours)` theo giờ tự nhiên thay vì cộng từng ngày và bỏ qua ngày nghỉ Chủ Nhật theo quy tắc **QT-04**. |
| **6. Cách sửa** | Viết lại vòng lặp cộng ngày làm việc: nếu rơi vào Chủ Nhật (`current.weekday() == 6`), tự động tịnh tiến thêm 24 giờ để nhảy sang Thứ Hai. |
| **7. Commit và xác nhận** | Commit: `2f3be03` · Test `test_sla_calculation_skip_sunday` chuyển từ FAIL sang **PASS 100%**. |

---

## 2. BUG-002 · Major — Không xem được chi tiết phiếu có chứa ký tự gạch chéo `/2026` (Lỗi HTTP 404)

| Dòng | Nội dung |
| :--- | :--- |
| **1. Mã và mức độ** | `BUG-002` · **Major** (Nhân viên tiếp nhận không thể bấm xem chi tiết phiếu vừa tạo trên màn hình M3). |
| **2. Phát hiện bởi** | Kiểm thử giao diện trực tiếp khi bấm nút "Xem →" của phiếu `BH-000004/2026` từ danh sách M2. |
| **3. Triệu chứng** | Màn hình M3 hiện thông báo đỏ: *"Không tải được phiếu — HTTP 404: Not Found"*. |
| **4. Cách tái lập** | `curl -s -X GET http://localhost:8000/api/v1/tickets/BH-000004/2026` $\rightarrow$ Trả về `404 Not Found`. |
| **5. Nguyên nhân** | Route backend khai báo `@router.get("/{ticket_code}")`. Trong FastAPI/Starlette, `{ticket_code}` chỉ khớp một phân đoạn URL (không chứa dấu `/`). Khi đường dẫn là `.../tickets/BH-000004/2026`, Starlette coi `/2026` là đường dẫn con và trả về 404. |
| **6. Cách sửa** | Đổi khai báo route thành `@router.get("/{ticket_code:path}")` để nhận toàn bộ chuỗi chứa dấu gạch chéo, kết hợp hàm `unquote(ticket_code)`. |
| **7. Commit và xác nhận** | Commit: `117780f` · Giao diện M3 hiển thị đầy đủ thông tin phiếu và Timeline lịch sử trạng thái ngay lập tức. |

---

## 3. BUG-003 · Major — Lộ số điện thoại khách hàng chưa che trong nhật ký hệ thống (Vi phạm QT-15)

| Dòng | Nội dung |
| :--- | :--- |
| **1. Mã và mức độ** | `BUG-003` · **Major** (Nguy cơ rò rỉ thông tin cá nhân khách hàng qua tệp nhật ký khi đẩy ra stdout/logging). |
| **2. Phát hiện bởi** | Phép thử rà quét rò rỉ dữ liệu nhạy cảm theo checklist tự học Buổi 11 (Mục D4). |
| **3. Triệu chứng** | Lệnh gọi `POST /api/v1/customers/search` in nguyên văn SĐT khách hàng `0908123456` vào luồng log của ứng dụng. |
| **4. Cách tái lập** | Gửi request tìm kiếm khách hàng bằng SĐT thô và đọc log terminal: SĐT hiển thị nguyên vẹn 10 chữ số. |
| **5. Nguyên nhân** | Ứng dụng dùng cấu hình log cơ bản chưa có bộ lọc (filter/formatter) che mờ trường thông tin nhạy cảm. |
| **6. Cách sửa** | Tạo bộ lọc regex trong `src/core/logger.py` (`mask_phone_str`), tự động che mờ mọi số điện thoại thành `090****456` trước khi xuất log JSON ra `stdout`. |
| **7. Commit và xác nhận** | Commit: `feat(core): add structured json logger with QT-15 phone masking` · Đọc `docker compose logs` xác nhận số điện thoại luôn được che dạng `090****456`. |
