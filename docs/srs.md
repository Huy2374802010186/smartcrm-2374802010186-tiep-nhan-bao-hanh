# TÀI LIỆU ĐẶC TẢ YÊU CẦU HỆ THỐNG (SRS RÚT GỌN)
**Dự án:** Smart CRM – Mekong Mobile  
**Phân hệ:** Luồng L02 – Tiếp nhận và phân loại yêu cầu bảo hành  
**Sinh viên thực hiện:** Nguyễn Trương Đức Huy – MSSV: 2374802010186  
**Chuyên ngành (Track):** Software Engineering (SE) – Luồng L02  

---

## 1. Tổng quan & Bảng thuật ngữ (Overview & Glossary)

### 1.1. Tổng quan doanh nghiệp & Hệ thống
Công ty Cổ phần Bán lẻ & Dịch vụ Mekong Mobile thành lập năm 2015, kinh doanh bán lẻ điện thoại, máy tính bảng, phụ kiện và dịch vụ bảo hành - sửa chữa. Quy mô hiện tại gồm 24 cửa hàng bán lẻ và 6 trung tâm bảo hành, với khoảng 180 nhân viên (38 kỹ thuật viên bảo hành và 12 nhân viên tiếp nhận), phục vụ khoảng 65.000 khách hàng và xử lý trung bình 260 yêu cầu bảo hành/tháng.

Phân hệ **L02 – Tiếp nhận và phân loại yêu cầu bảo hành** thuộc hệ thống Smart CRM được xây dựng nhằm số hóa quy trình tiếp nhận, tra cứu thông tin khách hàng, ghi nhận thông tin thiết bị, tự động kiểm tra điều kiện bảo hành, phân loại nhóm sự cố, tính hạn cam kết SLA và khởi tạo phiếu bảo hành (`ticket`).

### 1.2. Bảng thuật ngữ nghiệp vụ (Glossary)

| Thuật ngữ | Định nghĩa nghiệp vụ | Tên kỹ thuật |
| :--- | :--- | :--- |
| **Khách hàng** | Cá nhân đã mua sản phẩm hoặc sử dụng dịch vụ tại Mekong Mobile. | `customer` |
| **Thiết bị** | Máy cụ thể của khách hàng, định danh duy nhất bằng số Serial/IMEI. | `device` |
| **Phiếu bảo hành** | Yêu cầu bảo hành/sửa chữa được ghi nhận, có mã duy nhất (`BH-XXXXXX/2026`) và vòng đời trạng thái. | `ticket` |
| **Trạng thái phiếu** | Vị trí hiện tại của phiếu trong vòng đời (`MỚI`, `ĐÃ PHÂN CÔNG`, `ĐANG XỬ LÝ`, `CHỜ LINH KIỆN`, `HOÀN TẤT`, `ĐÃ ĐÓNG`, `ĐÃ HỦY`). | `ticket_status` |
| **Hạn cam kết (SLA)** | Thời điểm chậm nhất phải hoàn tất phiếu theo mức ưu tiên (Cao: 24h, Trung bình: 72h, Thấp: 120h làm việc T2–T7). | `due_date` |
| **Nhóm sự cố** | Phân loại nguyên nhân sự cố: Màn hình, Pin, Sạc, Phần mềm, Nước vào, Khác. | `issue_category` |
| **Mức ưu tiên** | Mức độ khẩn cấp (`CAO`, `TRUNG_BINH`, `THAP`) quyết định hạn cam kết SLA. | `priority` |
| **Lịch sử trạng thái** | Nhật ký lưu mỗi lần chuyển trạng thái kèm thời gian và người thực hiện. | `ticket_status_log` |

---

## 2. Phạm vi bài toán bằng một câu (Scope)

> **"Quản lý tiếp nhận và phân loại yêu cầu bảo hành:** Nhân viên tiếp nhận tra cứu/lập hồ sơ khách hàng và thiết bị, ghi nhận thông tin sự cố; hệ thống hỗ trợ kiểm tra điều kiện bảo hành, tự động phân loại nhóm sự cố, tính hạn cam kết SLA và khởi tạo phiếu bảo hành (ticket), theo dõi chuyển dịch trạng thái tiếp nhận cho đến khi hoàn tất hoặc đóng phiếu."

---

## 3. Danh mục User Story & Tiêu chí Chấp nhận (User Stories & Acceptance Criteria)

### 3.1. Bảng tổng hợp 8 User Story

| Mã US | Vai trò (Actor) | Mục tiêu (Want) | Giá trị (So that) | Quy tắc / Vấn đề | MoSCoW |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **US1** | Nhân viên tiếp nhận | Tra cứu và hệ thống tự động chuẩn hóa số điện thoại khách hàng | Nhanh chóng tìm thấy hồ sơ có sẵn, tránh tạo hồ sơ trùng lặp | V1, QT-01, QT-02 | **MUST** |
| **US2** | Nhân viên tiếp nhận | Ghi nhận số IMEI/Serial và ngày mua của thiết bị | Quản lý chính xác thông tin máy cần bảo hành | QT-03 | **MUST** |
| **US3** | Nhân viên tiếp nhận | Hệ thống tự động đối soát ngày mua với thời hạn bảo hành | Xác định thiết bị còn/hết hạn hoặc đánh dấu cần duyệt | QT-05 | **MUST** |
| **US4** | Nhân viên tiếp nhận | Chọn nhóm sự cố chuẩn hóa (`issue_category`) và nhập mô tả lỗi | Thống kê chính xác nguyên nhân bảo hành phổ biến | V8 | **SHOULD** |
| **US5** | Nhân viên tiếp nhận | Tự động gợi ý mức ưu tiên và tính hạn cam kết `due_date` | Hẹn chính xác ngày trả máy và cảnh báo quá hạn | V2, QT-04 | **MUST** |
| **US6** | Nhân viên tiếp nhận | Khởi tạo phiếu bảo hành mới ở trạng thái `MỚI` và lưu vết | Bắt đầu vòng đời xử lý phiếu minh bạch | QT-06 | **MUST** |
| **US7** | Quản lý / Nhân viên | Xem và lọc danh sách phiếu tiếp nhận theo trạng thái và SLA | Đôn đốc tiến độ và ưu tiên phiếu sắp quá hạn | V2 | **SHOULD** |
| **US8** | Quản lý trung tâm | Nhận thông báo và phê duyệt phiếu thiếu ngày mua | Quyết định thiết bị có được hưởng chế độ bảo hành miễn phí hay không | QT-05 | **COULD** |

---

### 3.2. Tiêu chí Chấp nhận Given–When–Then (GWT) cho các Story MUST

#### **US1 (MUST): Tra cứu & Chuẩn hóa Khách hàng theo Số điện thoại**
* **Kịch bản 1 (Luồng chính - Chuẩn hóa số điện thoại):**
  * **Given** Nhân viên tiếp nhận nhập số điện thoại chưa chuẩn hóa (dạng `84901234567` hoặc `090 123 4567`) vào ô tìm kiếm.
  * **When** Nhấn nút "Tìm kiếm".
  * **Then** Hệ thống tự động quy đổi về dạng 10 số chuẩn `0901234567` (QT-02) và hiển thị thông tin hồ sơ khách hàng tương ứng.
* **Kịch bản 2 (Luồng ngoại lệ - Khách hàng mới):**
  * **Given** Số điện thoại `0909999999` chưa từng tồn tại trên hệ thống Mekong Mobile.
  * **When** Nhân viên thực hiện tìm kiếm.
  * **Then** Hệ thống hiển thị thông báo "Không tìm thấy khách hàng" và hiển thị form cho phép khởi tạo hồ sơ khách hàng mới.

#### **US2 (MUST): Ghi nhận Thông tin Thiết bị & Ngày mua**
* **Kịch bản 1 (Luồng chính - Ghi nhận IMEI và ngày mua hợp lệ):**
  * **Given** Khách hàng chọn tiếp nhận bảo hành thiết bị có số IMEI `889900112233445`.
  * **When** Nhân viên nhập IMEI và ngày mua `15/01/2026` từ hóa đơn.
  * **Then** Hệ thống lưu thông tin thiết bị và liên kết thiết bị với `customer_id` hiện tại.
* **Kịch bản 2 (Luồng ngoại lệ - Trùng IMEI ở khách hàng khác):**
  * **Given** Số IMEI `889900112233445` đã được gán cho một khách hàng khác trên hệ thống.
  * **When** Nhân viên lưu thông tin thiết bị.
  * **Then** Hệ thống ngăn chặn lưu bản ghi và hiển thị cảnh báo vi phạm quy tắc QT-03: "Số IMEI này đã thuộc về khách hàng khác, vui lòng kiểm tra lại".

#### **US3 (MUST): Tự động Kiểm tra Điều kiện Bảo hành**
* **Kịch bản 1 (Luồng chính - Còn hạn bảo hành):**
  * **Given** Ngày tiếp nhận phiếu là `02/10/2026`, ngày mua của thiết bị là `15/01/2026` (thời hạn bảo hành 12 tháng).
  * **When** Hệ thống đối soát điều kiện bảo hành.
  * **Then** Hệ thống xác nhận "Còn bảo hành" và tự động gán chi phí `is_warranty = True`.
* **Kịch bản 2 (Luồng ngoại lệ - Thiếu thông tin ngày mua):**
  * **Given** Khách hàng không nhớ ngày mua và không giữ hóa đơn.
  * **When** Nhân viên tiếp nhận chọn tùy chọn "Thiếu ngày mua".
  * **Then** Hệ thống gán trạng thái phiếu là "Chưa xác minh bảo hành" (`is_warranty = False`) và gửi yêu cầu phê duyệt tới Quản lý trung tâm theo quy tắc QT-05.

#### **US5 (MUST): Tự động Phân loại SLA & Tính Hạn Trả máy (`due_date`)**
* **Kịch bản 1 (Luồng chính - Mức ưu tiên CAO):**
  * **Given** Phiếu bảo hành được chọn mức ưu tiên "CAO" (SLA 24h làm việc) và tiếp nhận lúc 09:00 Thứ Sáu.
  * **When** Hệ thống tính toán hạn cam kết SLA (QT-04).
  * **Then** Hệ thống tự động gán `due_date` là 09:00 Thứ Bảy cùng tuần.
* **Kịch bản 2 (Luồng chính - Bỏ qua ngày Chủ Nhật):**
  * **Given** Phiếu bảo hành được chọn mức ưu tiên "TRUNG_BINH" (SLA 72h làm việc, tương đương 3 ngày) tiếp nhận lúc 09:00 Thứ Sáu.
  * **When** Hệ thống tính toán `due_date` theo lịch làm việc T2–T7.
  * **Then** Hệ thống tự động bỏ qua ngày Chủ Nhật và gán `due_date` là 09:00 Thứ Ba tuần kế tiếp.

#### **US6 (MUST): Khởi tạo Phiếu & Lưu vết Trạng thái**
* **Kịch bản 1 (Luồng chính - Khởi tạo thành công):**
  * **Given** Thông tin khách hàng, thiết bị, mô tả lỗi và SLA đã được điền đầy đủ.
  * **When** Nhân viên nhấn nút "Tạo phiếu bảo hành".
  * **Then** Hệ thống sinh mã phiếu tự động dạng `BH-XXXXXX/2026`, gán trạng thái `status = 'MOI'`, và ghi tự động 1 bản ghi vào bảng `ticket_status_log` theo quy tắc QT-06.

---

## 4. Yêu cầu Chức năng (FR) & Đặc tả Use Case

### 4.1. Bảng Danh mục Yêu cầu Chức năng (Functional Requirements - FR)

| Mã FR | Tên chức năng | User Story liên quan | Use Case liên quan | Mức MoSCoW |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Tra cứu & chuẩn hóa thông tin khách hàng | US1 | UC-01 | MUST |
| **FR-02** | Ghi nhận thông tin thiết bị bảo hành | US2 | UC-02 | MUST |
| **FR-03** | Tự động kiểm tra điều kiện bảo hành | US3 | UC-03 | MUST |
| **FR-04** | Phân loại nhóm sự cố & mô tả lỗi | US4 | UC-04 | SHOULD |
| **FR-05** | Tự động tính hạn cam kết SLA | US5 | UC-04 | MUST |
| **FR-06** | Khởi tạo phiếu bảo hành & lưu log | US6 | UC-05 | MUST |
| **FR-07** | Xem & lọc danh sách phiếu tiếp nhận | US7 | UC-06 | SHOULD |
| **FR-08** | Phê duyệt phiếu thiếu thông tin ngày mua | US8 | UC-07 | COULD |

### 4.2. Sơ đồ Use Case Diagram
*Sơ đồ Use Case được thiết kế chuẩn gồm ranh giới hệ thống, chú thích (legend) và được lưu trữ dưới dạng file gốc tại `docs\diagrams\UseCase_SmartCRM_L02.drawio` trong repository.*

### 4.3. Bản đặc tả chi tiết Use Case cốt lõi (`UC-05`)

* **Mã Use Case:** `UC-05`
* **Tên Use Case:** Tiếp nhận & khởi tạo phiếu bảo hành
* **Actor chính:** Nhân viên tiếp nhận
* **Mô tả ngắn gọn:** Nhân viên tiếp nhận nhập/xác nhận thông tin khách hàng, thiết bị, mô tả lỗi và SLA để hệ thống tự động khởi tạo phiếu bảo hành mới (`ticket`) ở trạng thái `MỚI` và ghi nhật ký trạng thái.
* **Điều kiện tiên quyết (Pre-conditions):**
  1. Nhân viên tiếp nhận đã đăng nhập thành công vào hệ thống Smart CRM.
  2. Hệ thống đã xác định được mã trung tâm tiếp nhận (`center_id`).
* **Điều kiện sau (Post-conditions):**
  1. Một bản ghi phiếu bảo hành mới được lưu vào bảng `ticket` với trạng thái `status = 'MOI'`, gán chi phí `is_warranty`, và sinh mã phiếu duy nhất dạng `BH-XXXXXX/2026`.
  2. Một bản ghi lịch sử được thêm vào bảng `ticket_status_log` lưu vết khởi tạo.

#### Luồng chính (Main Flow):
1. **Nhân viên** nhập số điện thoại khách hàng. Hệ thống tự động chuẩn hóa về dạng 10 số (QT-01, QT-02) và hiển thị thông tin khách hàng.
2. **Nhân viên** nhập số IMEI/Serial của thiết bị và ngày mua từ hóa đơn (QT-03).
3. **Hệ thống** tự động kiểm tra điều kiện bảo hành theo ngày mua (QT-05) và xác nhận thiết bị "Còn bảo hành" (`is_warranty = True`).
4. **Nhân viên** chọn nhóm sự cố (`issue_category`) và nhập mô tả chi tiết lỗi ban đầu (`issue_desc`).
5. **Hệ thống** tự động đề xuất mức ưu tiên và tính hạn cam kết trả máy `due_date` theo quy tắc giờ làm việc T2–T7 (QT-04).
6. **Nhân viên** rà soát toàn bộ thông tin trên màn hình và nhấn nút "Tạo phiếu bảo hành".
7. **Hệ thống** thực hiện:
   * Sinh mã phiếu hiển thị dạng `BH-XXXXXX/2026`.
   * Lưu thông tin vào bảng `ticket` với trạng thái `status = 'MOI'`.
   * Ghi tự động 1 bản ghi vào bảng `ticket_status_log` (QT-06).
8. **Hệ thống** hiển thị thông báo "Tạo phiếu thành công" kèm mã phiếu và ngày hẹn trả máy `due_date`.

#### Các luồng ngoại lệ (Alternative / Exception Flows):
* **3a. IMEI thiết bị đã tồn tại thuộc về khách hàng khác (Vi phạm QT-03):**
  * *3a1.* Hệ thống cảnh báo "Số IMEI này đã được gán cho một khách hàng khác trên hệ thống".
  * *3a2.* Nhân viên kiểm tra lại IMEI trên vỏ máy hoặc hóa đơn.
  * *3a3.* Nếu nhập sai, nhân viên nhập lại IMEI đúng và quay lại Bước 3 của luồng chính.
* **3b. Không xác minh được ngày mua / Thiếu hóa đơn (Vi phạm QT-05):**
  * *3b1.* Hệ thống đánh dấu phiếu là "Chưa xác minh bảo hành" (`is_warranty = False / Pending`).
  * *3b2.* Hệ thống khởi tạo phiếu ở trạng thái chờ duyệt và gửi thông báo tới Quản lý trung tâm.
  * *3b3.* Luồng tiếp nhận tạm dừng cho đến khi Quản lý trung tâm thực hiện phê duyệt (`UC-07`).

---

## 5. Yêu cầu Phi Chức năng (Non-Functional Requirements - NFR)

| Mã NFR | Tiêu chí chất lượng | Ngưỡng con số đo lường cụ thể |
| :--- | :--- | :--- |
| **NFR-01** | **Hiệu năng (Performance)** | Thời gian phản hồi của API tra cứu khách hàng và tạo phiếu `ticket` < **300ms** cho 95% số request khi đạt mức tải 50 kết nối đồng thời. |
| **NFR-02** | **Chính xác (Accuracy)** | Thuật toán chuẩn hóa số điện thoại tự động đạt tỷ lệ chính xác **100%** đối với các định dạng đầu số Việt Nam (`+84`, `84`, `0x`). |
| **NFR-03** | **Độ tin cậy (Availability)** | Hệ thống đạt độ sẵn sàng **≥ 99.5%** trong khung giờ hành chính (07:30 – 20:30 từ Thứ 2 đến Thứ 7). |
| **NFR-04** | **Bảo mật (Security/Privacy)** | Che (masking) số điện thoại hiển thị dạng `090****567` với vai trò Nhân viên tiếp nhận theo đúng quy tắc QT-15. |

---

## 6. Bảng Truy vết (Traceability Matrix) & API Contract (Track SE)

### 6.1. Bảng Truy vết Ma trận (Traceability Matrix)

| Mã FR | Tên chức năng | Mã US | Mã Use Case | Mức MoSCoW |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Tra cứu & chuẩn hóa thông tin khách hàng | US1 | UC-01 | MUST |
| **FR-02** | Ghi nhận thông tin thiết bị bảo hành | US2 | UC-02 | MUST |
| **FR-03** | Tự động kiểm tra điều kiện bảo hành | US3 | UC-03 | MUST |
| **FR-04** | Phân loại nhóm sự cố & mô tả lỗi | US4 | UC-04 | SHOULD |
| **FR-05** | Tự động tính hạn cam kết SLA | US5 | UC-04 | MUST |
| **FR-06** | Khởi tạo phiếu bảo hành & lưu log | US6 | UC-05 | MUST |
| **FR-07** | Xem & lọc danh sách phiếu tiếp nhận | US7 | UC-06 | SHOULD |
| **FR-08** | Phê duyệt phiếu thiếu thông tin ngày mua | US8 | UC-07 | COULD |

---

### 6.2. Thiết kế API Contract (Dành riêng cho Track SE)

#### **Endpoint 1: `POST /api/v1/tickets`**
* **Mục đích:** Khởi tạo phiếu bảo hành mới ở trạng thái `MỚI` (Phục vụ `US1`, `US2`, `US3`, `US5`, `US6`).
* **Request Header:** `Content-Type: application/json`
* **Request Body JSON Mẫu:**
  ```json
  {
    "customer_phone": "090 123 4567",
    "serial_no": "IMEI889900112233445",
    "purchase_date": "2026-01-15",
    "category_id": 2,
    "issue_desc": "Màn hình chớp nháy không hiển thị",
    "priority": "CAO"
  }
  ```
* **Response Mẫu Thành công (`201 Created`):**
  ```json
  {
    "status": "success",
    "data": {
      "ticket_id": 1024,
      "ticket_code": "BH-000123/2026",
      "customer_phone_normalized": "0901234567",
      "status": "MOI",
      "is_warranty": true,
      "due_date": "2026-10-03T09:00:00Z",
      "created_at": "2026-10-02T09:00:00Z"
    }
  }
  ```

#### **Endpoint 2: `POST /api/v1/customers/search`**
* **Mục đích:** Tra cứu và chuẩn hóa số điện thoại khách hàng (Phục vụ `US1`).
* **Request Body JSON Mẫu:**
  ```json
  {
    "phone": "84901234567"
  }
  ```
* **Response Mẫu Thành công (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "customer_id": 852,
      "full_name": "Nguyễn Văn A",
      "phone_normalized": "0901234567",
      "phone_masked": "090****567"
    }
  }
  ```

#### **Bảng Quy tắc Validation Dữ liệu Đầu vào & HTTP Status Codes:**

| Trường dữ liệu | Bắt buộc | Kiểu dữ liệu | Quy tắc Validation | HTTP Status Code khi vi phạm |
| :--- | :--- | :--- | :--- | :--- |
| `customer_phone` | Có | String | Phải quy đổi được về 10 chữ số bắt đầu bằng `0` (QT-02) | `400 Bad Request` |
| `serial_no` | Có | String | Bắt buộc có độ dài 10-50 ký tự; Không trùng với khách hàng khác (QT-03) | `400 Bad Request` / `409 Conflict` |
| `purchase_date` | Không | String (ISO Date) | Định dạng `YYYY-MM-DD`; Không lớn hơn ngày hiện tại | `400 Bad Request` |
| `category_id` | Có | Integer | Phải tồn tại trong bảng `issue_category` | `404 Not Found` |
| `priority` | Có | String | Chỉ nhận 1 trong 3 giá trị: `"CAO"`, `"TRUNG_BINH"`, `"THAP"` | `400 Bad Request` |

---

## 7. Thiết kế Kiến trúc Hệ thống (Architecture Design)

### 7.1. Sơ đồ Kiến trúc Phân lớp (4-Tier Layered Architecture)
*Sơ đồ kiến trúc được thiết kế và lưu trữ dưới dạng file gốc tại `docs/architecture.drawio` trong repository.*

* **Lớp Presentation (Giao diện):** Xây dựng bằng React (Vite), chịu trách nhiệm hiển thị 3 màn hình nghiệp vụ M1 (Tiếp nhận/Tạo phiếu), M2 (Danh sách & Lọc SLA), M3 (Chi tiết phiếu & Nhật ký lịch sử).
* **Lớp Business/Service (Xử lý nghiệp vụ):** Xây dựng bằng Python FastAPI, chứa toàn bộ business logic: chuẩn hóa SĐT (QT-01, QT-02), đối soát bảo hành (QT-05), thuật toán tính SLA tự động bỏ qua Chủ Nhật (QT-04), sinh mã phiếu và ghi log chuyển trạng thái (QT-06).
* **Lớp Data Access/Repository (Truy xuất dữ liệu):** Sử dụng SQLAlchemy ORM để tách biệt logic truy vấn CSDL khỏi Service Layer.
* **Lớp Database (Lưu trữ):** Cơ sở dữ liệu quan hệ PostgreSQL lưu trữ 5 thực thể chính.

### 7.2. Ba câu Lập luận Quyết định Kiến trúc (Architectural Trade-offs)

1. **Lập luận 1 (Hiệu năng - NFR-01):**
> "Vì **NFR-01** yêu cầu thời gian phản hồi API tra cứu khách hàng và tạo phiếu `< 300ms` với 50 kết nối đồng thời, tôi chọn **đánh B-Tree Index trên cột `phone` (bảng `customer`) và các cột `status`, `due_date` (bảng `ticket`)**, đánh đổi là **tốn thêm dung lượng bộ nhớ lưu trữ index và làm tăng nhẹ thời gian ghi (Write latency) khi khởi tạo phiếu mới."

2. **Lập luận 2 (Chính xác nghiệp vụ - NFR-02):**
> "Vì **NFR-02** yêu cầu thuật toán chuẩn hóa số điện thoại tự động đạt độ chính xác **100%** cho các đầu số Việt Nam (`+84`, `84`, `0x`), tôi chọn **thực hiện chuẩn hóa Regex Pipeline tại Service Layer** trước khi truy vấn CSDL, đánh đổi là **tăng thêm một lượng nhỏ chi phí tính toán CPU trên Backend Server cho mỗi request tìm kiếm."

3. **Lập luận 3 (Bảo mật - NFR-04):**
> "Vì **NFR-04** yêu cầu **che (masking) số điện thoại dạng `090****567`** đối với vai trò Nhân viên tiếp nhận theo quy tắc QT-15, tôi chọn **thực hiện Masking ngay tại Data Response Transformer của Backend** trước khi trả dữ liệu về Client, đánh đổi là **Backend không thể dùng cơ chế Caching tĩnh cho API thông tin khách hàng mà phải render động theo Scope người dùng."
