# BÀI TẬP 1 — BẢN ĐẶC TẢ YÊU CẦU & THIẾT KẾ HỆ THỐNG (SRS RÚT GỌN)
**Học phần:** Chuyên đề Tốt nghiệp 1 (71ITGR40203)  
**Dự án:** Smart CRM – Mekong Mobile  
**Phân hệ:** Luồng L02 – Tiếp nhận và phân loại yêu cầu bảo hành  
**Sinh viên thực hiện:** Nguyễn Trương Đức Huy – MSSV: 2374802010186  
**Chuyên ngành (Track):** Software Engineering (SE)  
**Lớp / Nhóm:** 261_71ITGR40203_05  

---

## MỤC 1 — BẢN SRS RÚT GỌN

### 1.1. Giới thiệu và phạm vi
* **Bối cảnh:** Mekong Mobile vận hành 24 cửa hàng bán lẻ và 6 trung tâm bảo hành. Hiện chưa có hệ thống CRM tập trung; quy trình tiếp nhận hoàn toàn thủ công bằng phiếu giấy. Thực trạng này gây ra trùng lặp 18–22% hồ sơ khách hàng (V1), tra cứu ngày mua mất 5–10 phút/khách và khoảng 30% không tra cứu được, 15% phiếu bị xử lý quá hạn SLA không cảnh báo (V2) và ghi lỗi tự do không thống kê được nguyên nhân hỏng hóc phổ biến (V8).
* **Phạm vi bài toán bằng một câu (Scope):** "Quản lý tiếp nhận và phân loại yêu cầu bảo hành: Nhân viên tiếp nhận tra cứu/lập hồ sơ khách hàng và thiết bị, ghi nhận thông tin sự cố; hệ thống hỗ trợ kiểm tra điều kiện bảo hành, tự động phân loại nhóm sự cố, tính hạn cam kết SLA và khởi tạo phiếu bảo hành (ticket), theo dõi chuyển dịch trạng thái tiếp nhận cho đến khi hoàn tất hoặc đóng phiếu."
* **Chủ ý KHÔNG làm (WON'T / Out of Scope):**
  * Chọn và phân công kỹ thuật viên cụ thể (thuộc luồng L04).
  * Phê duyệt ngoại lệ bảo hành miễn phí của Quản lý trung tâm đối với các trường hợp thiếu ngày mua (QT-05).
  * Tự động gửi SMS/Zalo thông báo tiến độ cho khách.
  * Quản lý kho và xuất nhập linh kiện thay thế (thuộc luồng L05).
  * Khảo sát đo lường CSAT/NPS (L08) và Báo cáo doanh thu tổng hợp (L06).
* **Hướng mở rộng (COULD):** Báo cáo thống kê tần suất các nhóm sự cố theo từng dòng sản phẩm/model thiết bị.

#### Bảng thuật ngữ nghiệp vụ (Glossary):
| Thuật ngữ | Định nghĩa nghiệp vụ | Tên kỹ thuật |
| :--- | :--- | :--- |
| **Khách hàng** | Người đã mua sản phẩm hoặc sử dụng dịch vụ tại Mekong Mobile |  |
| **Thiết bị** | Máy cụ thể của khách hàng, định danh duy nhất bằng số Serial/IMEI |  |
| **Phiếu bảo hành** | Một yêu cầu bảo hành/sửa chữa được ghi nhận, có mã duy nhất và vòng đời trạng thái |  |
| **Trạng thái phiếu** | Vị trí hiện tại trong vòng đời (MỚI, ĐÃ PHÂN CÔNG, ĐANG XỬ LÝ, CHỜ LINH KIỆN, HOÀN TẤT, ĐÃ ĐÓNG, ĐÃ HỦY) |  |
| **Lịch sử trạng thái** | Nhật ký lưu mỗi lần chuyển trạng thái kèm thời gian và người thực hiện |  |
| **Hạn cam kết (SLA)** | Thời điểm chậm nhất phải hoàn tất phiếu, tính từ lúc tiếp nhận theo mức ưu tiên |  |
| **Nhóm sự cố** | Phân loại nguyên nhân: Màn hình, Pin, Sạc, Phần mềm, Nước vào, Khác |  |
| **Mức ưu tiên** | Mức khẩn cấp của phiếu (CAO, TRUNG_BINH, THAP) quyết định hạn cam kết SLA |  |
| **Tình trạng bảo hành** | Còn bảo hành / Hết bảo hành / Chưa xác minh, xác định tại thời điểm tiếp nhận |  |
| **Trung tâm** | Trung tâm bảo hành tiếp nhận phiếu (định danh bằng mã do hệ thống ngoài cấp) |  |

### 1.2. Các bên liên quan và vai trò
| Tác nhân (Actor) | Quyền hạn / Được làm | Không được làm |
| :--- | :--- | :--- |
| **Nhân viên tiếp nhận** | Tra cứu khách hàng, tạo khách hàng mới, tạo phiếu bảo hành mới, xem danh sách phiếu của trung tâm mình | Xem phiếu của trung tâm khác; xem số điện thoại đầy đủ của khách hàng (QT-15) |
| **Quản lý trung tâm** | Xem danh sách phiếu bảo hành của trung tâm mình, xem đầy đủ số điện thoại khách hàng, đôn đốc tiến độ SLA | Tạo trực tiếp hoặc sửa đổi nội dung phiếu bảo hành của nhân viên |

### 1.3. Yêu cầu chức năng và User Story
| Mã FR | Yêu cầu chức năng (phát biểu kiểm chứng được) | User Story | MoSCoW |
| :--- | :--- | :--- | :--- |
| **FR1** | Tra cứu khách hàng theo số điện thoại; tự động quy đổi SĐT về dạng 10 số bắt đầu bằng 0 và hiển thị hồ sơ khách hàng cùng danh sách thiết bị | **US1** | **MUST** |
| **FR2** | Tạo hồ sơ khách hàng mới khi số điện thoại chưa tồn tại; từ chối và báo lỗi nếu số điện thoại đã tồn tại trên hệ thống (QT-01, QT-02) | **US2** | **MUST** |
| **FR3** | Ghi nhận thông tin thiết bị (IMEI/Serial, ngày mua) và liên kết thiết bị với hồ sơ khách hàng hiện tại (QT-03) | **US3** | **MUST** |
| **FR4** | Cho phép chọn nhóm sự cố chuẩn hóa và nhập mô tả lỗi chi tiết (tối thiểu 10 ký tự) | **US4** | **SHOULD** |
| **FR5** | Tự động đối soát điều kiện bảo hành (QT-05) và tự động tính hạn cam kết SLA due_date theo quy tắc giờ làm việc T2–T7 (QT-04) | **US5** | **MUST** |
| **FR6** | Hiển thị danh sách phiếu bảo hành đã tiếp nhận của trung tâm, hỗ trợ lọc theo trạng thái và sắp xếp theo hạn SLA tăng dần | **US6** | **SHOULD** |
| **FR7** | Khởi tạo phiếu ở trạng thái MỚI, cho phép cập nhật trạng thái đúng vòng đời (QT-06) và tự động ghi log vào ticket_status_log | **US7** | **MUST** |

#### Bảng chi tiết 7 User Story (INVEST & MoSCoW):
| Mã US | MoSCoW | User Story (Là <vai trò>, tôi muốn <mục tiêu> để <giá trị>) |
| :--- | :--- | :--- |
| **US1** | **MUST** | Là Nhân viên tiếp nhận, tôi muốn tra cứu và tự động chuẩn hóa số điện thoại khách hàng để nhanh chóng tìm thấy hồ sơ có sẵn, tránh tạo hồ sơ trùng lặp (giải quyết V1). |
| **US2** | **MUST** | Là Nhân viên tiếp nhận, tôi muốn khởi tạo hồ sơ khách hàng mới khi số điện thoại chưa tồn tại để ghi nhận đầy đủ thông tin khách hàng mới đến cửa hàng lần đầu. |
| **US3** | **MUST** | Là Nhân viên tiếp nhận, tôi muốn ghi nhận số IMEI/Serial và ngày mua của thiết bị để quản lý chính xác thông tin thiết bị cần bảo hành (QT-03). |
| **US4** | **SHOULD** | Là Nhân viên tiếp nhận, tôi muốn chọn nhóm sự cố chuẩn hóa và nhập mô tả lỗi chi tiết để thống kê chính xác nguyên nhân hỏng hóc phổ biến (giải quyết V8). |
| **US5** | **MUST** | Là Nhân viên tiếp nhận, tôi muốn hệ thống tự động đối soát bảo hành và tính hạn cam kết due_date theo SLA để hẹn chính xác ngày trả máy cho khách (giải quyết V2). |
| **US6** | **SHOULD** | Là Quản lý trung tâm, tôi muốn xem và lọc danh sách phiếu tiếp nhận theo trạng thái và SLA để đôn đốc tiến độ xử lý và ưu tiên các phiếu sắp quá hạn. |
| **US7** | **MUST** | Là Nhân viên tiếp nhận, tôi muốn khởi tạo phiếu mới và cập nhật trạng thái đúng vòng đời để bắt đầu xử lý phiếu minh bạch và lưu vết lịch sử (QT-06). |

#### Tiêu chí Chấp nhận Given–When–Then (GWT) cho các Story MUST:
* **US1 (MUST) — Tra cứu & Chuẩn hóa Khách hàng theo SĐT:**
  * *Kịch bản 1 (Chuẩn hóa SĐT đầu vào):* **Given** Nhân viên tiếp nhận nhập chuỗi SĐT '84908123456' hoặc '090 812 3456' vào ô tìm kiếm; **When** nhấn 'Tìm kiếm'; **Then** hệ thống tự động quy đổi về dạng 10 số chuẩn '0908123456' (QT-02) và hiển thị thông tin hồ sơ khách hàng.
  * *Kịch bản 2 (Ngoại lệ - Khách hàng mới):* **Given** SĐT '0909888777' chưa tồn tại trên hệ thống; **When** nhấn 'Tìm kiếm'; **Then** hệ thống hiển thị thông báo 'Không tìm thấy khách hàng' và tự động mở form cho phép tạo khách hàng mới.
* **US2 (MUST) — Khởi tạo Hồ sơ Khách hàng mới:**
  * *Kịch bản 1 (Tạo thành công):* **Given** Form tạo khách hàng mới được mở; **When** Nhân viên nhập 'Nguyễn Văn B' và SĐT '0909888777' rồi nhấn 'Lưu'; **Then** hệ thống khởi tạo bản ghi mới trong bảng customer và gán customer_id.
  * *Kịch bản 2 (Ngoại lệ - SĐT đã tồn tại):* **Given** SĐT '0908123456' đã thuộc về khách hàng 'Nguyễn Văn A'; **When** Nhân viên cố tình tạo mới với SĐT này; **Then** hệ thống từ chối lưu, trả mã lỗi HTTP 409 Conflict và cảnh báo vi phạm QT-01.
* **US3 (MUST) — Ghi nhận Thông tin Thiết bị:**
  * *Kịch bản 1 (Ghi nhận hợp lệ):* **Given** Khách hàng đã được chọn; **When** Nhân viên nhập IMEI '358990011223344' và ngày mua '15/01/2026'; **Then** hệ thống lưu thiết bị vào bảng device và gán liên kết với customer_id.
  * *Kịch bản 2 (Ngoại lệ - Trùng IMEI ở khách khác):* **Given** IMEI '358990011223344' đã được gán cho một khách hàng khác; **When** Nhân viên lưu thiết bị; **Then** hệ thống ngăn chặn lưu bản ghi và cảnh báo vi phạm quy tắc QT-03.
* **US5 (MUST) — Tính Hạn SLA & Đối soát Bảo hành:**
  * *Kịch bản 1 (Mức ưu tiên CAO):* **Given** Phiếu được chọn mức 'CAO' (SLA 24h làm việc) tiếp nhận lúc 09:00 Thứ Sáu (02/10/2026); **When** hệ thống tính toán due_date; **Then** due_date được gán tự động là 09:00 Thứ Bảy (03/10/2026).
  * *Kịch bản 2 (Ngoại lệ - Trực qua Chủ Nhật):* **Given** Phiếu được chọn mức 'TRUNG_BINH' (SLA 72h làm việc) tiếp nhận lúc 09:00 Thứ Sáu; **When** hệ thống tính due_date theo lịch T2–T7; **Then** hệ thống tự động bỏ qua ngày Chủ Nhật và gán due_date là 09:00 Thứ Ba tuần kế tiếp (QT-04).
* **US7 (MUST) — Khởi tạo Phiếu & Lưu vết Trạng thái:**
  * *Kịch bản 1 (Khởi tạo thành công):* **Given** Đủ thông tin khách hàng, thiết bị và mô tả lỗi; **When** Nhân viên nhấn 'Tạo phiếu bảo hành'; **Then** hệ thống sinh mã 'BH-000123/2026', gán status = 'MOI' và ghi tự động 1 dòng lịch sử vào ticket_status_log (QT-06).
  * *Kịch bản 2 (Ngoại lệ - Chuyển trạng thái sai vòng đời):* **Given** Phiếu đang ở trạng thái 'ĐÃ PHÂN CÔNG'; **When** ai đó cố tình cập nhật ngược về 'MỚI'; **Then** hệ thống từ chối cập nhật và báo lỗi vi phạm quy tắc QT-06.

### 1.4. Yêu cầu phi chức năng (NFR)
| Mã NFR | Loại tiêu chí | Ngưỡng con số đo lường cụ thể |
| :--- | :--- | :--- |
| **NFR1** | **Hiệu năng (Performance)** | Thời gian phản hồi của API tra cứu khách hàng và khởi tạo phiếu < 300ms cho 95% số request khi hệ thống đạt tải 50 kết nối đồng thời. Màn hình danh sách hiển thị < 2 giây với 1.000 bản ghi phân trang 20 dòng. |
| **NFR2** | **Bảo mật (Security/Privacy)** | Số điện thoại khách hàng hiển thị dạng che (masking 090****567) đối với vai trò Nhân viên tiếp nhận theo QT-15; 0 endpoint API trả về SĐT đầy đủ cho người dùng không có quyền Quản lý. |
| **NFR3** | **Khả dụng (Usability)** | Nhân viên tiếp nhận mới có thể thực hiện thành công việc tra cứu và khởi tạo một phiếu bảo hành mới trong thời gian < 2.5 phút ngay trong lần đầu thao tác mà không cần trợ giúp. |
| **NFR4** | **Bảo trì (Maintainability)** | Việc thay đổi cấu hình thời hạn SLA (QT-04) chỉ phải thực hiện chỉnh sửa duy nhất trong 1 module của lớp Business/Service; 0 file nguồn bị ảnh hưởng ở lớp Presentation và Data Access. |

### 1.5. Ràng buộc và quy tắc nghiệp vụ
| Mã Quy tắc | Nội dung Quy tắc Nghiệp vụ |
| :--- | :--- |
| **QT-01** | Số điện thoại khách hàng là duy nhất; khi nhập số đã tồn tại, hệ thống hiển thị hồ sơ có sẵn thay vì tạo mới. |
| **QT-02** | Số điện thoại được chuẩn hóa về dạng 10 chữ số bắt đầu bằng 0 trước khi lưu (+84, 84, dấu cách đều quy về chuẩn). |
| **QT-03** | Thiết bị xác định duy nhất bằng số Serial/IMEI; một thiết bị chỉ thuộc về một khách hàng tại một thời điểm. |
| **QT-04** | Hạn cam kết SLA tự sinh từ lúc tiếp nhận: CAO = 24h, TRUNG_BINH = 72h, THAP = 120h; chỉ tính ngày làm việc T2–T7. |
| **QT-05** | Thiết bị còn bảo hành nếu (ngày tiếp nhận − ngày mua) ≤ số tháng bảo hành; không có ngày mua thì đánh dấu 'Chưa xác minh'. |
| **QT-06** | Phiếu chỉ chuyển trạng thái theo đúng vòng đời; không được quay lại trạng thái trước; mọi chuyển trạng thái ghi log vào ticket_status_log. |
| **QT-13** | Không xóa vật lý phiếu bảo hành và hồ sơ khách hàng (chỉ soft delete nếu cần). |
| **QT-15** | Số điện thoại hiển thị dạng che (090****567) với mọi vai trò trừ Quản lý trung tâm. |

### 1.6. Bảng truy vết yêu cầu (Traceability Matrix)
| FR | User Story | Use Case | MoSCoW | Bảng dữ liệu | Màn hình |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR1** | **US1** | **UC1** | **MUST** | customer, device | M1 |
| **FR2** | **US2** | **UC2** | **MUST** | customer | M1 |
| **FR3** | **US3** | **UC3** | **MUST** | device, customer | M1 |
| **FR4** | **US4** | **UC4** | **SHOULD** | ticket, issue_category | M1, M3 |
| **FR5** | **US5** | **UC3** | **MUST** | ticket | M1, M2 |
| **FR6** | **US6** | **UC5** | **SHOULD** | ticket, customer, device | M2 |
| **FR7** | **US7** | **UC6** | **MUST** | ticket, ticket_status_log | M1, M3 |

---

## MỤC 2 — USE CASE

### 2.1. Sơ đồ Use Case (Use Case Diagram)
Sơ đồ Use Case được thiết kế tuân thủ đầy đủ chuẩn ký pháp: ranh giới hệ thống rõ ràng, 2 tác nhân ngoài ranh giới (Nhân viên tiếp nhận, Quản lý trung tâm), có khung chú thích Ký hiệu (Legend) và ranh giới hệ thống 'Phân hệ L02 - Smart CRM'. Tên Use Case tuân thủ quy tắc ĐỘNG TỪ + ĐỐI TƯỢNG (VD: Tra cứu khách hàng, Khởi tạo phiếu bảo hành mới). File gốc: .

### 2.2. Đặc tả chi tiết Use Case cốt lõi: UC3 — Khởi tạo phiếu bảo hành mới
* **Tác nhân chính:** Nhân viên tiếp nhận
* **Mục tiêu:** Ghi nhận thông tin khách hàng, thiết bị và lỗi để hệ thống tự động kiểm tra bảo hành, tính SLA và khởi tạo phiếu mới
* **Điều kiện trước:** Nhân viên tiếp nhận đã đăng nhập vào hệ thống CRM và đã xác định được mã trung tâm tiếp nhận ()
* **Điều kiện sau:** Một bản ghi phiếu bảo hành trạng thái 'MỚI' được lưu vào bảng , mã phiếu duy nhất sinh ra, và 1 dòng log lưu vào 
* **User Story liên quan:** US3, US4, US5, US7 (Mức ưu tiên MoSCoW: MUST)

#### Luồng chính (Main Flow):
1. Nhân viên tiếp nhận chọn chức năng 'Tạo phiếu bảo hành mới' trên giao diện M1.
2. Nhân viên nhập số điện thoại khách hàng và bấm 'Tra cứu'.
3. Hệ thống tự động chuẩn hóa SĐT về dạng 10 số (QT-01, QT-02) và hiển thị thông tin khách hàng kèm danh sách thiết bị đã mua. 
4. Nhân viên chọn thiết bị bảo hành từ danh sách; hệ thống hiển thị ngày mua và đối soát điều kiện bảo hành (QT-05).
5. Nhân viên chọn nhóm sự cố () và nhập mô tả lỗi chi tiết do khách kể (tối thiểu 10 ký tự). 
6. Hệ thống đề xuất mức ưu tiên và tự động tính hạn cam kết  theo quy tắc làm việc T2–T7 (QT-04).
7. Nhân viên rà soát toàn bộ thông tin trên form và nhấn nút 'Lưu phiếu'.
8. Hệ thống sinh mã phiếu duy nhất dạng , lưu bản ghi vào bảng  với , tự động ghi 1 dòng log vào  (QT-06), và hiển thị thông báo thành công kèm ngày hẹn trả máy.

#### Các luồng ngoại lệ (Alternative / Exception Flows):
* **3a. SĐT không tồn tại trên hệ thống:** Hệ thống báo 'Không tìm thấy khách hàng' và gợi ý nút 'Tạo khách hàng mới'. Sau khi lưu khách mới (), hệ thống tự chuyển lại bước 4.
* **4a. Thiết bị chưa từng có trong lịch sử mua:** Hệ thống cho phép nhập thiết bị ngoài: bắt buộc nhập số IMEI/Serial và chọn thương hiệu/model; hệ thống tự tạo bản ghi  và gán với khách này (QT-03).
* **4b. Không có thông tin ngày mua / mất hóa đơn:** Hệ thống tự động đánh dấu  ('Chưa xác minh bảo hành') và thông báo phiếu sẽ chuyển Quản lý duyệt trước khi làm dịch vụ miễn phí (QT-05).
* **5a. Mô tả lỗi quá ngắn (< 10 ký tự):** Hệ thống chặn không cho bấm lưu và hiển thị cảnh báo ngay bên dưới ô nhập: 'Mô tả lỗi phải từ 10 ký tự trở lên'.
* **7a. Thiết bị đang có phiếu bảo hành chưa đóng:** Hệ thống phát hiện thiết bị đang ở trạng thái xử lý khác 'ĐÃ ĐÓNG'/'ĐÃ HỦY', từ chối tạo mới và hiển thị mã phiếu đang mở để Nhân viên tra cứu.

---

## MỤC 3 — THIẾT KẾ KIẾN TRÚC

### 3.1. Sơ đồ Kiến trúc Phân lớp (4-Tier Layered Architecture)
Hệ thống Smart CRM (Phân hệ L02) áp dụng mô hình Kiến trúc Phân lớp 4 tầng (4-Tier Layered Architecture) với nguyên tắc phụ thuộc một chiều từ trên xuống dưới:
* **Layer 1: Presentation Layer (React Web Frontend):** Hiển thị M1, M2, M3; gửi REST API requests và nhận kết quả JSON. Không chứa Business Logic.
* **Layer 2: Business / Service Layer (FastAPI Backend):** Chứa các Service xử lý nghiệp vụ:  (QT-01, QT-02, QT-15 masking),  (QT-05),  (QT-04),  (QT-06 sinh mã phiếu và ghi log).
* **Layer 3: Data Access / Repository Layer (SQLAlchemy ORM):** Truy xuất dữ liệu thông qua các Repository độc lập (, , , ), tách biệt SQL khỏi Service.
* **Layer 4: Database Layer (PostgreSQL Database):** Lưu trữ 5 thực thể chính chuẩn 3NF, áp dụng B-Tree Index tối ưu hóa truy vấn.

### 3.2. Ba câu Lập luận Quyết định Kiến trúc (Trade-off Arguments)
1. **Lập luận 1 (về Hiệu năng - NFR1):**
   > "Vì NFR1 yêu cầu thời gian phản hồi API tra cứu khách hàng và khởi tạo phiếu < 300ms với 50 kết nối đồng thời và danh sách hiển thị < 2s với 1.000 bản ghi, tôi chọn đánh B-Tree Index ghép  trên bảng  và thực hiện phân trang 20 dòng ngay tại lớp Data Access; đánh đổi là tốn thêm dung lượng lưu trữ index và thời gian ghi (Write latency) khi tạo mới/cập nhật phiếu chậm hơn một chút."
2. **Lập luận 2 (về Bảo mật - NFR2):**
   > "Vì NFR2 yêu cầu che (masking) số điện thoại dạng  đối với vai trò Nhân viên tiếp nhận theo QT-15, tôi chọn thực hiện kiểm tra Scope vai trò và Masking trực tiếp tại  tầng Backend trước khi trả về Presentation Layer; đánh đổi là mọi API endpoint khách hàng đều phải truyền JWT Token chứa thông tin vai trò và trải qua bước biến đổi dữ liệu trên CPU Backend."
3. **Lập luận 3 (về Bảo trì - NFR4):**
   > "Vì NFR4 yêu cầu việc thay đổi cấu hình thời hạn SLA (QT-04) chỉ được thực hiện trong 1 module duy nhất và 0 file bị ảnh hưởng ở lớp khác, tôi chọn kiến trúc 4 lớp độc lập với phụ thuộc một chiều và đóng gói toàn bộ thuật toán SLA vào  của tầng Business; đánh đổi là phải viết thêm các file trung gian (Controller, Service, Repository) cho mỗi thao tác xử lý dữ liệu."

---

## MỤC 4 — MÔ HÌNH DỮ LIỆU (TRACK SE)

### 4.1. Sơ đồ ERD (5 Bảng chuẩn 3NF, Ký pháp Chân chim)
Mô hình ERD chuẩn 3NF gồm 5 bảng chính, sử dụng ký pháp Chân chim (Crow's Foot). Mọi thực thể đều dùng khóa chính nhân tạo ( / ) để tối ưu hiệu năng nối bảng. File gốc: .

### 4.2. Bảng Truy vết Thực thể Dữ liệu về Yêu cầu Chức năng
| Tên Bảng (Entity) | Phục vụ FR | Lý do tồn tại Nghiệp vụ & Ràng buộc |
| :--- | :--- | :--- |
| **** | FR1, FR2, FR3 | Thực thể lưu thông tin khách hàng; cột  là khóa nghiệp vụ UNIQUE (QT-01, QT-02) |
| **** | FR1, FR3 | Thực thể lưu thông tin thiết bị; cột  là khóa nghiệp vụ UNIQUE định danh duy nhất (QT-03) |
| **** | FR4 | Danh mục nhóm sự cố chuẩn hóa; thêm nhóm sự cố mới chỉ cần thêm dòng dữ liệu mà không sửa code |
| **** | FR3, FR4, FR5, FR6, FR7 | Thực thể trung tâm lưu phiếu bảo hành, trạng thái, chi phí  và hạn SLA  |
| **** | FR7 | Bảng nhật ký lưu vết mọi lần chuyển trạng thái theo đúng vòng đời (QT-06), đáp ứng tính minh bạch |

### 4.3. Thiết kế Index & Lựa chọn Tối ưu CSDL
| Tên Index | Cột áp dụng Index | Phục vụ Yêu cầu / Nghiệp vụ |
| :--- | :--- | :--- |
| **** |  | Phục vụ FR1 / NFR1 — Tối ưu tốc độ tra cứu khách hàng theo SĐT < 300ms |
| **** |  | Phục vụ FR6 / NFR1 — Tối ưu lọc danh sách phiếu theo trung tâm + trạng thái và sắp SLA |
| **** |  | Phục vụ US3 (luồng 7a) — Ép ở cấp CSDL: 1 thiết bị chỉ có tối đa 1 phiếu chưa đóng |

### 4.4. Mã nguồn SQL DDL Skeleton ()


### 4.5. Thiết kế API Contract (Track SE)
* **POST ** — Tra cứu & Chuẩn hóa SĐT khách hàng (US1)
* **POST ** — Khởi tạo phiếu bảo hành mới (US3, US5, US7)

#### Bảng Quy tắc Validation Dữ liệu đầu vào API:
| Trường dữ liệu | Bắt buộc | Kiểu dữ liệu | Quy tắc Validation | HTTP Status Code |
| :--- | :--- | :--- | :--- | :--- |
|  | Có | String | Phải quy đổi về 10 chữ số bắt đầu bằng 0 (QT-02) | 400 Bad Request |
|  | Có | String | Độ dài 10-50 ký tự; Không trùng với khách khác (QT-03) | 400 Bad / 409 Conflict |
|  | Không | String (Date) | Định dạng YYYY-MM-DD; Không lớn hơn ngày hiện tại | 400 Bad Request |
|  | Có | String | Độ dài từ 10 đến 2000 ký tự | 400 Bad Request |
|  | Có | String | Chỉ nhận 1 trong 3 giá trị: CAO, TRUNG_BINH, THAP | 400 Bad Request |

---

## MỤC 5 — WIREFRAME 3 MÀN HÌNH

### 5.1. Màn hình M1: Tra cứu & Tiếp nhận / Tạo phiếu bảo hành
* **User Story liên quan:** US1, US2, US3, US4, US5, US7
* **Mô tả Bố cục Wireframe:**
  * Header: Tiêu đề 'Tiếp nhận Yêu cầu Bảo hành', Mã trung tâm tiếp nhận ().
  * Khối Tra cứu Khách hàng (US1): Ô nhập SĐT, Nút 'Tìm kiếm'. Tự động quy đổi SĐT và hiển thị Họ tên/Địa chỉ hoặc Nút 'Tạo khách mới' (US2).
  * Khối Thông tin Thiết bị (US3): Ô nhập IMEI/Serial, Ngày mua. Badge trạng thái bảo hành 'Còn bảo hành' () hoặc 'Chưa xác minh ngày mua' (QT-05).
  * Khối Mô tả Lỗi & SLA (US4, US5): Dropdown Nhóm sự cố (), Ô nhập Mô tả lỗi (), Select Mức ưu tiên (CAO, TRUNG_BINH, THAP). Ô hiển thị Hạn cam kết  tự động tính bỏ qua Chủ Nhật (QT-04).
  * Thanh thao tác: Nút chính 'Tạo phiếu bảo hành' (US7) sinh mã .

### 5.2. Màn hình M2: Danh sách Phiếu Tiếp nhận & Lọc SLA
* **User Story liên quan:** US6
* **Mô tả Bố cục Wireframe:**
  * Thanh Tìm kiếm & Bộ lọc: Ô tìm kiếm Mã phiếu/SĐT/IMEI; Dropdown lọc Trạng thái (MỚI, ĐÃ PHÂN CÔNG...); Checkbox 'Chỉ hiện phiếu Quá hạn SLA'.
  * Bảng Dữ liệu (Data Table): Cột Mã phiếu | Khách hàng | IMEI/Thiết bị | Nhóm sự cố | Trạng thái | Hạn SLA () | Thao tác.
  * Highlight trực quan: Tô màu Đỏ cảnh báo phiếu đã quá hạn SLA, màu Vàng cho phiếu còn dưới 4 giờ.
  * Thao tác: Nút 'Xem chi tiết' chuyển sang màn hình M3.

### 5.3. Màn hình M3: Chi tiết Phiếu Bảo hành & Nhật ký Lịch sử Trạng thái
* **User Story liên quan:** US7
* **Mô tả Bố cục Wireframe:**
  * Header Màn hình: Mã phiếu , Badge trạng thái hiện tại (MỚI), Badge đếm ngược SLA.
  * Bố cục 2 Cột Thông tin:
    * Cột trái: Thông tin khách hàng (SĐT được masking  theo QT-15), Thông tin máy, Ngày mua, Tình trạng bảo hành.
    * Cột phải: Nhóm sự cố, Mô tả lỗi chi tiết ban đầu.
  * Khối Timeline Lịch sử Trạng thái (): Bảng dòng thời gian hiển thị Thời gian | Trạng thái cũ -> Trạng thái mới | Người thực hiện | Ghi chú (QT-06).

---

## PHỤ LỤC — BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI

| Công cụ AI | Phần áp dụng | Cách dùng (Tóm tắt prompt gửi AI) | Em đã kiểm chứng / chỉnh sửa gì |
| :--- | :--- | :--- | :--- |
| **Trợ lý AI dạng chat** | Mục 1 — User Story & GWT | Gợi ý danh sách 7 User Story chuẩn INVEST và kịch bản GWT cho luồng L02 tiếp nhận bảo hành | Em chọn lọc 7 story, viết lại đúng khuôn 3 phần, tự phân hạng MoSCoW và bổ sung kịch bản ngoại lệ thực tế. |
| **Trợ lý AI dạng chat** | Mục 3 — Lập luận NFR | Viết 3 câu lập luận kỹ thuật theo khuôn: Vì <NFR>..., tôi chọn..., đánh đổi là... | Gắn trực tiếp mã NFR-01, NFR-02, NFR-04 có con số đo lường thực tế và điều chỉnh đánh đổi theo kiến trúc 4 lớp. |
| **Trợ lý AI dạng chat** | Mục 4 — SQL DDL & API Contract | Gợi ý cấu trúc DDL PostgreSQL 3NF cho 5 bảng chính và mẫu JSON Response | Tự thêm các ràng buộc CHECK, UNIQUE, tạo INDEX tối ưu tốc độ tra cứu SĐT/SLA và đính kèm comment quy tắc QT-01 đến QT-06. |
| **Không sử dụng AI** | Mục 2 & Mục 5 — Sơ đồ & Wireframe | Tự vẽ sơ đồ Use Case, sơ đồ Kiến trúc và mô tả Wireframe 3 màn hình | Đảm bảo tính nhất quán giữa actor, use case, các lớp kiến trúc và trường dữ liệu hiển thị trên wireframe. |
