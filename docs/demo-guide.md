# Kịch bản Demo Nhanh 3 Phút & Bộ Câu Hỏi Vấn Đáp (Buổi 12)
**Học phần:** Chuyên đề Tốt nghiệp 1 (Khoa CNTT - ĐH Văn Lang)  
**Sinh viên:** Nguyễn Trương Đức Huy — **MSSV:** 2374802010186 — **Track:** Software Engineering (SE)  
**Phân hệ:** Luồng L02 – Tiếp nhận và Phân loại Yêu cầu Bảo hành (Mekong Mobile)  

---

## ⏱️ PHẦN 1: KỊCH BẢN DEMO 3 PHÚT (BẤM GIỜ TẠI BÀN)

Giảng viên bấm giờ đúng 3 phút. Trình bày dứt khoát 4 nội dung sau:

### 1. Phút 00:00 – 01:15: Luồng chính chạy End-to-End (Từ đầu đến cuối)
- **Thao tác:** Mở trình duyệt tại `http://localhost:8000/` (hoặc cổng 80 qua Docker).
- **Lời nói:**
  > *"Em xin demo Luồng L02: Tiếp nhận và Phân loại Bảo hành. Đầu tiên em nhập SĐT khách hàng `0908 123 456` (hoặc `+84908123456`)."*
- **Quan sát:**
  - Hệ thống tự chuẩn hóa về `0908123456` (QT-01) và che hiển thị `090****456` (QT-15 bảo mật).
  - Tự tải thông tin khách hàng VIP Nguyễn Văn A và lịch sử thiết bị.
  - Chọn thiết bị `VN8492019283` $\rightarrow$ Hệ thống tự đối soát ngày mua `2026-01-15` $\rightarrow$ Báo xanh **"Còn bảo hành"** (QT-05).
  - Chọn sự cố: *"Màn hình sọc ngang"* (Nhóm Phần cứng - Màn hình) $\rightarrow$ Mức ưu tiên **CAO** $\rightarrow$ Hệ thống tự tính hạn trả máy SLA đúng **24 giờ** (QT-04).
  - Bấm **"Tạo phiếu bảo hành"** $\rightarrow$ Modal hiện mã phiếu mới sinh `BH-000004/2026`.
  - Tự chuyển sang Màn hình M2: Phiếu mới hiển thị ngay đầu danh sách; bấm **"Xem →"** mở Màn hình M3 với đầy đủ thông tin và Timeline trạng thái.

### 2. Phút 01:15 – 02:00: Trình diễn 1 trường hợp lỗi được xử lý đúng (C7)
- **Thao tác 1 (Mô tả lỗi ngắn):** Nhập mô tả lỗi dưới 10 ký tự (ví dụ: `Hỏng`) $\rightarrow$ Giao diện khóa nút tạo hoặc báo đỏ ngay: *"Mô tả lỗi phải từ 10 ký tự trở lên (QT-06)"*.
- **Thao tác 2 (Trùng phiếu mở QT-03):** Tạo tiếp phiếu cho thiết bị vừa tạo đang ở trạng thái `MOI` $\rightarrow$ Hệ thống từ chối với thông báo rõ ràng: *"Thiết bị đang có phiếu bảo hành chưa hoàn tất (QT-03)"*, mã HTTP 409, **không bị sập 500**.
- **Lời nói:**
  > *"Hệ thống chặn dữ liệu sai ở ranh giới tầng Service bằng `LoiNghiepVu`, trả mã lỗi chuẩn REST 400/409 kèm mã tra cứu Request-Id, tuyệt đối không trả lỗi thô của thư viện."*

### 3. Phút 02:00 – 02:30: Lệnh chạy kiểm thử Unit Tests (C4)
- **Thao tác:** Mở terminal chạy 1 lệnh duy nhất:
  ```bash
  python -m unittest tests/test_sprint1.py -v
  ```
- **Kết quả:** **8/8 test cases PASS 100%** trong chưa đầy 0.05s.
- **Lời nói:**
  > *"Toàn bộ 8 unit tests đều PASS 100%, bao gồm: Happy path chuẩn hóa SĐT, che số điện thoại QT-15, giá trị biên SLA tự nhảy qua Chủ Nhật QT-04, và test ngoại lệ từ chối trùng phiếu mở QT-03."*

### 4. Phút 02:30 – 03:00: Kể một lỗi đã gỡ và mở Bug Log
- **Thao tác:** Mở tệp [`docs/bug-log.md`](file:///d:/Works/ChuyenDeTotNghiep1/Tuan8/smartcrm-2374802010186-tiep-nhan-bao-hanh/docs/bug-log.md).
- **Lời nói:**
  > *"Trong quá trình tích hợp, em gặp lỗi `BUG-002`: Khi xem chi tiết phiếu `BH-000004/2026` thì bị lỗi 404 Not Found do mã phiếu có dấu gạch chéo `/2026` khiến Starlette phân đoạn URL sai. Em đã khoanh vùng và sửa bằng cách dùng path converter `{ticket_code:path}` kết hợp hàm `unquote()`. Test xác nhận chạy thành công và em đã ghi lại đầy đủ 7 dòng theo chuẩn vào `docs/bug-log.md`."*

---

## 🎯 PHẦN 2: BỘ BA CÂU HỎI CHUẨN CỦA GIẢNG VIÊN (TRẢ LỜI ĐỂ ĐẠT ĐIỂM 10)

Giảng viên sẽ chọn ngẫu nhiên 1 hàm hoặc 1 quyết định kiến trúc để hỏi. Dưới đây là câu trả lời chuẩn:

### ❓ Câu 1: "Vì sao em chọn cách này mà không phải cách kia?"
- **Câu trả lời chuẩn về SLA (QT-04):**
  > *"Trong `SLAService.calculate_due_date`, thay vì dùng công thức cộng giờ cố định `datetime + timedelta(hours=24)`, em cài đặt thuật toán cộng giờ theo từng ngày làm việc (Thứ 2 đến Thứ 7). Khi duyệt qua ngày Chủ Nhật (`weekday() == 6`), thuật toán tự động bỏ qua 24 giờ của ngày nghỉ để nhảy sang sáng Thứ 2. Cách này đảm bảo cam kết SLA đúng thực tế vận hành của các trung tâm bảo hành Mekong Mobile."*
- **Câu trả lời chuẩn về API Client trên Frontend:**
  > *"Ở tầng giao diện, em đóng gói toàn bộ lệnh gọi API qua module `src/static/js/api/client.js` duy nhất thay vì gọi `fetch()` rải rác ở từng component. Cách này giúp tập trung xử lý lỗi mạng, gán Request-Id đồng bộ và không bị phụ thuộc vào URL cứng."*

---

### ❓ Câu 2: "Nếu dữ liệu tăng gấp 10 thì chỗ nào hỏng trước?"
- **Câu trả lời chuẩn:**
  > *"Chỗ sẽ bị chậm và nghẽn đầu tiên là **Endpoint `GET /api/v1/tickets` (Màn hình M2)**. Hiện tại endpoint đang tải toàn bộ danh sách phiếu trong bảng. Khi số lượng phiếu lên đến hàng trăm nghìn bản ghi, thời gian truy vấn và băng thông mạng sẽ tăng vọt, gây nghẽn bộ nhớ trình duyệt.*  
  > *Cách khắc phục của em:  
  > 1. Bổ sung phân trang `LIMIT` và `OFFSET` (hoặc Keyset pagination) ở tầng Repository.  
  > 2. Đánh chỉ mục (Index) trên các cột thường xuyên lọc: `status`, `due_date` và `customer_phone_normalized` như em đã ghi trong `docs/thay-doi-thiet-ke.md` (TD-03)."*

---

### ❓ Câu 3: "Chỉ cho thầy dòng mã chịu trách nhiệm cho việc này"
- **Nếu thầy hỏi về tính SLA bỏ qua Chủ Nhật:**
  - Mở tệp: [`src/services/sla_service.py`](file:///d:/Works/ChuyenDeTotNghiep1/Tuan8/smartcrm-2374802010186-tiep-nhan-bao-hanh/src/services/sla_service.py#L30-L45)
  - Chỉ đúng vào dòng: `if current_dt.weekday() == 6: current_dt += timedelta(days=1)`
- **Nếu thầy hỏi về kiểm tra trùng phiếu mở (QT-03):**
  - Mở tệp: [`src/services/ticket_service.py`](file:///d:/Works/ChuyenDeTotNghiep1/Tuan8/smartcrm-2374802010186-tiep-nhan-bao-hanh/src/services/ticket_service.py#L32-L37)
  - Chỉ đúng vào dòng: `existing = repo.find_open_by_serial(serial_no)` và `raise KeyError(...)`
- **Nếu thầy hỏi về che số điện thoại khách hàng (QT-15):**
  - Mở tệp: [`src/services/customer_service.py`](file:///d:/Works/ChuyenDeTotNghiep1/Tuan8/smartcrm-2374802010186-tiep-nhan-bao-hanh/src/services/customer_service.py#L25-L30) và [`src/core/logger.py`](file:///d:/Works/ChuyenDeTotNghiep1/Tuan8/smartcrm-2374802010186-tiep-nhan-bao-hanh/src/core/logger.py#L22-L26)
  - Chỉ vào logic regex `r"(0[3|5|7|8|9]\d)(\d{4})(\d{3})" -> r"\1****\3"`.
