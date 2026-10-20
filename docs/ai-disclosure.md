# KHAI BÁO SỬ DỤNG CÔNG CỤ AI (AI DISCLOSURE)

**Dự án:** Smart CRM – Mekong Mobile  
**Phân hệ:** Luồng L02 – Tiếp nhận và phân loại yêu cầu bảo hành  
**Sinh viên thực hiện:** Nguyễn Trương Đức Huy  
**MSSV:** 2374802010186 | **Lớp:** 261_71ITGR40203_05  
**Chuyên ngành (Track):** Software Engineering (SE)  

---

## 1. Danh mục các công cụ AI đã sử dụng

| STT | Tên công cụ AI | Mục đích sử dụng chính | Tần suất sử dụng |
| :--- | :--- | :--- | :--- |
| 1 | **Gemini / ChatGPT** | Gợi ý cấu trúc thư mục 4 lớp, tham khảo kịch bản Given-When-Then và sinh mã khung SQL DDL / Unit Tests. | Hàng tuần |
| 2 | **GitHub Copilot / Cursor** | Gợi ý hoàn thiện cú pháp Python (Pydantic, FastAPI), sinh Docstring cho hàm. | Trong lúc lập trình |

---

## 2. Bảng kê khai chi tiết nội dung áp dụng & Quy trình kiểm chứng

| Hạng mục sản phẩm | Công cụ AI | Nội dung Prompt / Yêu cầu gửi AI | Cách thức tự kiểm chứng & Chỉnh sửa của Sinh viên |
| :--- | :--- | :--- | :--- |
| **Yêu cầu & User Story** | ChatGPT | *"Gợi ý 8 User Story theo tiêu chí INVEST cho luồng L02 tiếp nhận bảo hành CRM"* | Rà soát loại bỏ các story ngoài phạm vi L02, viết lại kịch bản Given-When-Then cho các sự cố thực tế tại Mekong Mobile. |
| **Thiết kế Kiến trúc (Mục 3 BT1)** | Gemini | *"Viết 3 câu lập luận NFR theo khuôn NFR - Ngưỡng - Quyết định - Đánh đổi"* | Đưa các con số thực tế (API < 300ms, 50 kết nối), gắn đúng mã NFR-01, NFR-02, NFR-04 và đối soát với sơ đồ 4 lớp. |
| **Cơ sở dữ liệu (Mục 4 BT1)** | Gemini | *"Sinh mã SQL DDL 3NF cho 5 bảng chính luồng L02"* | Tự bổ sung các ràng buộc `CHECK`, `UNIQUE`, tạo 3 B-Tree Index tối ưu tra cứu SĐT/SLA và gắn comment quy tắc `QT-01` -> `QT-06`. |
| **Mã nguồn Module cốt lõi (Buổi 8)** | Copilot | *"Gợi ý thuật toán tính SLA do_date bỏ qua ngày Chủ Nhật trong Python"* | Viết lại hàm `calculate_due_date` dùng vòng lặp `timedelta`, bổ sung Unit Test tự động kiểm tra 100% các trường hợp biên. |

---

## 3. Cam kết Liêm chính Học thuật
Em xin cam đoan toàn bộ logic nghiệp vụ (`QT-01` đến `QT-15`), sơ đồ kiến trúc, mô hình CSDL và mã nguồn module cốt lõi đã được em hiểu rõ, tự kiểm thử và làm chủ hoàn toàn. Công cụ AI chỉ đóng vai trò trợ lý hỗ trợ tăng năng suất.
