-- ============================================================
-- SCRIPT KHỞI TẠO CƠ SỞ DỮ LIỆU (SQL DDL SKELETON - 3NF chuẩn Buổi 5 & 6)
-- Dự án: Smart CRM - Mekong Mobile (Luồng L02)
-- Sinh viên: Nguyễn Trương Đức Huy - MSSV: 2374802010186 - Track SE
-- ============================================================

-- 1. Bảng Khách hàng (customer)
CREATE TABLE customer (
    customer_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,                -- QT-01: SĐT duy nhất
    phone_normalized VARCHAR(10) NOT NULL UNIQUE,     -- QT-02: Chuẩn hóa 10 số bắt đầu bằng 0
    email VARCHAR(120),
    segment VARCHAR(20) DEFAULT 'MOI' 
        CHECK (segment IN ('VIP', 'THUONG_XUYEN', 'MOI', 'NGU_DONG')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_customer_phone_norm ON customer(phone_normalized); -- NFR-01 / US1

-- 2. Bảng Thiết bị (device)
CREATE TABLE device (
    device_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(customer_id) ON DELETE RESTRICT,
    serial_no VARCHAR(50) NOT NULL UNIQUE,            -- QT-03: Định danh duy nhất IMEI/Serial
    product_name VARCHAR(120) NOT NULL,
    purchase_date DATE,                               -- QT-05: Ngày mua đối soát bảo hành
    warranty_months SMALLINT NOT NULL DEFAULT 12,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_device_serial ON device(serial_no);

-- 3. Bảng Nhóm sự cố (issue_category)
CREATE TABLE issue_category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(60) NOT NULL UNIQUE,        -- V8: MÀN_HÌNH, PIN, SẠC...
    default_priority VARCHAR(12) NOT NULL DEFAULT 'TRUNG_BINH'
        CHECK (default_priority IN ('CAO', 'TRUNG_BINH', 'THAP')),
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true
);

-- Thêm dữ liệu danh mục ban đầu
INSERT INTO issue_category (category_name, default_priority, description) VALUES
('MÀN_HÌNH', 'CAO', 'Lỗi sọc, chớp nháy, chảy mực, vỡ kính'),
('PIN_NGUỒN', 'TRUNG_BINH', 'Chai pin, sạc không vào, sập nguồn'),
('PHẦN_MỀM', 'THAP', 'Lỗi hệ điều hành, treo logo, quên mật khẩu'),
('NƯỚC_VÀO', 'CAO', 'Thiết bị ngấm nước, ẩm ướt nội bộ'),
('KHÁC', 'TRUNG_BINH', 'Các sự cố phần cứng hoặc chức năng khác');

-- 4. Bảng Phiếu bảo hành (ticket)
CREATE TABLE ticket (
    ticket_id BIGSERIAL PRIMARY KEY,
    ticket_code VARCHAR(20) NOT NULL UNIQUE,          -- Dạng BH-XXXXXX/2026
    customer_id BIGINT NOT NULL REFERENCES customer(customer_id),
    device_id BIGINT NOT NULL REFERENCES device(device_id),
    category_id INT REFERENCES issue_category(category_id),
    issue_desc TEXT NOT NULL CHECK (length(issue_desc) >= 10), -- V8
    priority VARCHAR(12) NOT NULL DEFAULT 'TRUNG_BINH'
        CHECK (priority IN ('CAO', 'TRUNG_BINH', 'THAP')),     -- QT-04
    status VARCHAR(20) NOT NULL DEFAULT 'MOI'
        CHECK (status IN ('MOI', 'DA_PHAN_CONG', 'DANG_XU_LY', 'CHO_LINH_KIEN', 'HOAN_TAT', 'DA_DONG', 'DA_HUY')), -- QT-06
    is_warranty BOOLEAN NOT NULL DEFAULT true,        -- QT-05
    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    due_date TIMESTAMPTZ NOT NULL,                    -- QT-04: Hạn SLA
    closed_at TIMESTAMPTZ,
    CONSTRAINT chk_closed_after_received CHECK (closed_at IS NULL OR closed_at >= received_at)
);
CREATE INDEX idx_ticket_status_due ON ticket(status, due_date); -- NFR-01 / US7

-- 5. Bảng Lịch sử chuyển trạng thái (ticket_status_log)
CREATE TABLE ticket_status_log (
    log_id BIGSERIAL PRIMARY KEY,
    ticket_id BIGINT NOT NULL REFERENCES ticket(ticket_id) ON DELETE CASCADE,
    from_status VARCHAR(20),                          -- QT-06
    to_status VARCHAR(20) NOT NULL,                   -- QT-06
    note TEXT,
    changed_by VARCHAR(60) NOT NULL DEFAULT 'SYSTEM',
    changed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_log_ticket_id ON ticket_status_log(ticket_id, changed_at);
