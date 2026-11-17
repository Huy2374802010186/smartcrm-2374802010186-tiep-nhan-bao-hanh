-- ============================================================
-- SCRIPT DỮ LIỆU MẪU BAN ĐẦU (SEED DATA SPRINT 1)
-- Phân hệ L02: Tiếp nhận và Phân loại Bảo hành
-- ============================================================

-- 1. Thêm danh mục nhóm sự cố chuẩn hóa (issue_category)
INSERT INTO issue_category (category_id, category_name, default_priority, description, is_active) VALUES
(1, 'MÀN_HÌNH', 'CAO', 'Lỗi sọc màn hình, chớp nháy, chảy mực, vỡ kính cảm ứng', true),
(2, 'PIN_NGUỒN', 'TRUNG_BINH', 'Chai pin, pin phồng, sạc không vào, sập nguồn đột ngột', true),
(3, 'PHẦN_MỀM', 'THAP', 'Lỗi hệ điều hành, treo logo, quên mật khẩu, lỗi ứng dụng', true),
(4, 'NƯỚC_VÀO', 'CAO', 'Thiết bị ngấm nước, ẩm ướt linh kiện nội bộ', true),
(5, 'KHÁC', 'TRUNG_BINH', 'Các sự cố phần cứng, camera, loa, mic hoặc linh kiện khác', true)
ON CONFLICT (category_id) DO NOTHING;

-- 2. Thêm dữ liệu mẫu khách hàng (customer)
INSERT INTO customer (customer_id, full_name, phone, phone_normalized, email, segment) VALUES
(101, 'Nguyễn Văn An', '0908123456', '0908123456', 'an.nguyen@email.com', 'VIP'),
(102, 'Trần Thị Bình', '0912345678', '0912345678', 'binh.tran@email.com', 'THUONG_XUYEN'),
(103, 'Lê Văn Cường', '0987654321', '0987654321', 'cuong.le@email.com', 'MOI')
ON CONFLICT (customer_id) DO NOTHING;

-- 3. Thêm dữ liệu mẫu thiết bị (device)
INSERT INTO device (device_id, customer_id, serial_no, product_name, purchase_date, warranty_months) VALUES
(201, 101, 'SN-A52-778901', 'Samsung Galaxy A52', '2026-01-15', 12),
(202, 102, 'SN-S21-441207', 'Samsung Galaxy S21', '2025-05-10', 12),
(203, 103, 'SN-IP12-990113', 'iPhone 12 Pro Max', '2026-03-20', 12)
ON CONFLICT (device_id) DO NOTHING;
