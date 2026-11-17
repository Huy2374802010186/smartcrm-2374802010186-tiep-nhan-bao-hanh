# ĐẶC TẢ CHI TIẾT REST API CONTRACT (LUỒNG L02)

**Phân hệ:** Tiếp nhận và Phân loại Bảo hành (Smart CRM Mekong Mobile)  
**Base URL:** `http://localhost:8000/api/v1`  
**Định dạng dữ liệu:** `application/json`  

---

## 1. Tra cứu & Chuẩn hóa Khách hàng
* **Endpoint:** `POST /api/v1/customers/search`
* **Mô tả:** Tra cứu khách hàng theo SĐT. Tự động quy đổi SĐT về dạng 10 số chuẩn `0x` (QT-01, QT-02) và thực hiện Masking dạng `090****567` (QT-15).
* **Request Body:**
  ```json
  {
    "phone": "84901234567"
  }
  ```
* **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "data": {
      "customer_id": 1,
      "full_name": "Nguyễn Văn A",
      "phone_normalized": "0901234567",
      "phone_masked": "090****567",
      "email": "nguyenvana@gmail.com"
    }
  }
  ```
* **Response `404 Not Found`:**
  ```json
  {
    "status": "error",
    "message": "Không tìm thấy thông tin khách hàng với số điện thoại này."
  }
  ```

---

## 2. Khởi tạo Phiếu bảo hành mới
* **Endpoint:** `POST /api/v1/tickets`
* **Mô tả:** Tiếp nhận máy, đối soát điều kiện bảo hành (QT-05), tính SLA bỏ qua Chủ Nhật (QT-04), sinh mã phiếu `BH-XXXXXX/2026` và ghi nhật ký trạng thái `MOI` (QT-06).
* **Request Body:**
  ```json
  {
    "customer_phone": "090 123 4567",
    "serial_no": "IMEI889900112233445",
    "purchase_date": "2026-01-15",
    "category_id": 1,
    "issue_desc": "Màn hình bị sọc ngang và nhấp nháy liên tục",
    "priority": "CAO"
  }
  ```
* **Response `201 Created`:**
  ```json
  {
    "status": "success",
    "data": {
      "ticket_id": 101,
      "ticket_code": "BH-000101/2026",
      "customer_phone_normalized": "0901234567",
      "serial_no": "IMEI889900112233445",
      "is_warranty": true,
      "priority": "CAO",
      "status": "MOI",
      "due_date": "2026-10-20T09:00:00Z",
      "created_at": "2026-10-19T09:00:00Z"
    }
  }
  ```

---

## 3. Lọc & Báo cáo SLA Danh sách Phiếu
* **Endpoint:** `GET /api/v1/tickets`
* **Query Parameters:**
  * `status` (optional): `MOI`, `DANG_XU_LY`, `HOAN_TAT`
  * `overdue_only` (optional, boolean): `true` (chỉ lấy phiếu quá hạn SLA)
* **Response `200 OK`:**
  ```json
  {
    "status": "success",
    "total": 1,
    "data": [
      {
        "ticket_code": "BH-000101/2026",
        "customer_name": "Nguyễn Văn A",
        "serial_no": "IMEI889900112233445",
        "status": "MOI",
        "due_date": "2026-10-20T09:00:00Z",
        "is_overdue": false
      }
    ]
  }
  ```

---

## 4. Bảng Quy tắc HTTP Status Codes & Error Handling

| Status Code | Ý nghĩa | Kịch bản áp dụng |
| :--- | :--- | :--- |
| `200 OK` | Thành công | Tra cứu KH, Lấy danh sách phiếu. |
| `201 Created` | Tạo mới thành công | Khởi tạo phiếu bảo hành mới thành công. |
| `400 Bad Request` | Vi phạm Validation | SĐT không đúng định dạng, Mô tả lỗi < 10 ký tự. |
| `409 Conflict` | Trùng lặp dữ liệu | Thiết bị đang có phiếu bảo hành chưa đóng (`QT-03`). |
