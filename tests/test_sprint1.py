import unittest
from datetime import datetime, date
from src.services.customer_service import CustomerService
from src.services.sla_service import SLAService
from src.services.ticket_service import TicketService

class TestSprint1CoreModules(unittest.TestCase):

    # ──────────────────────────────────────────────
    # NHÓM 1: CHUẨN HÓA & MASKING SĐT (QT-01, QT-02, QT-15)
    # ──────────────────────────────────────────────

    def test_phone_normalization_valid(self):
        """Happy path: chuẩn hóa nhiều định dạng SĐT về 10 số."""
        self.assertEqual(CustomerService.normalize_phone("84908123456"), "0908123456")
        self.assertEqual(CustomerService.normalize_phone("+84 908 123 456"), "0908123456")
        self.assertEqual(CustomerService.normalize_phone("090 812 3456"), "0908123456")

    def test_phone_normalization_invalid(self):
        """Ngoại lệ: SĐT quá ngắn không chuẩn hóa được phải raise ValueError."""
        with self.assertRaises(ValueError):
            CustomerService.normalize_phone("12345")

    def test_phone_masking(self):
        """Happy path: che SĐT đúng dạng 090****456 (QT-15)."""
        self.assertEqual(CustomerService.mask_phone("0908123456"), "090****456")

    # ──────────────────────────────────────────────
    # NHÓM 2: TÍNH SLA BỎ QUA CHỦ NHẬT (QT-04)
    # ──────────────────────────────────────────────

    def test_sla_calculation_skip_sunday(self):
        """Giá trị biên: phiếu mức TRUNG_BINH nhận vào Thứ Sáu phải nhảy qua CN."""
        # Thứ Sáu 02/10/2026 09:00 + 72h làm việc → Thứ Ba 06/10/2026 09:00
        friday_dt = datetime(2026, 10, 2, 9, 0, 0)
        due_date = SLAService.calculate_due_date(friday_dt, "TRUNG_BINH")
        expected_dt = datetime(2026, 10, 6, 9, 0, 0)
        self.assertEqual(due_date, expected_dt)

    def test_sla_calculation_cao_24h(self):
        """Happy path: phiếu mức CAO (24h) tính đúng hạn SLA."""
        # Thứ Tư 01/10/2026 08:00 + 24h → Thứ Năm 02/10/2026 08:00 (không qua CN)
        wed_dt = datetime(2026, 10, 1, 8, 0, 0)
        due_date = SLAService.calculate_due_date(wed_dt, "CAO")
        expected_dt = datetime(2026, 10, 2, 8, 0, 0)
        self.assertEqual(due_date, expected_dt)

    # ──────────────────────────────────────────────
    # NHÓM 3: KHỞI TẠO PHIẾU BẢO HÀNH (QT-06, QT-03, V8)
    # ──────────────────────────────────────────────

    def test_ticket_creation_success(self):
        """Happy path: tạo phiếu thành công với đầy đủ dữ liệu hợp lệ."""
        service = TicketService()
        ticket = service.create_ticket(
            raw_phone="0908123456",
            serial_no="SN-A52-778901",
            category_id=1,
            issue_desc="Màn hình chớp nháy sọc ngang không hiển thị",
            priority="CAO"
        )
        self.assertTrue(ticket["ticket_code"].startswith("BH-"))
        self.assertEqual(ticket["status"], "MOI")
        self.assertEqual(ticket["customer_phone_masked"], "090****456")

    def test_ticket_creation_short_desc(self):
        """Ngoại lệ (V8): mô tả lỗi dưới 10 ký tự phải raise ValueError."""
        service = TicketService()
        with self.assertRaises(ValueError):
            service.create_ticket(
                raw_phone="0908123456",
                serial_no="SN-A52-778901",
                category_id=1,
                issue_desc="Hỏng",
                priority="CAO"
            )

    def test_ticket_duplicate_open_ticket(self):
        """Ngoại lệ (QT-03/QT-09): thiết bị đang có phiếu mở phải raise KeyError."""
        from src.repositories.ticket_repository import TicketRepository

        repo = TicketRepository()
        service = TicketService()

        # Tạo phiếu đầu tiên thành công
        service.create_ticket(
            raw_phone="0912345678",
            serial_no="SN-DUPLICATE-TEST-001",
            category_id=2,
            issue_desc="Pin chai không sạc được điện bình thường",
            priority="TRUNG_BINH",
            repo=repo
        )

        # Tạo phiếu thứ hai với cùng serial_no → phải bị từ chối
        with self.assertRaises(KeyError):
            service.create_ticket(
                raw_phone="0987654321",
                serial_no="SN-DUPLICATE-TEST-001",
                category_id=3,
                issue_desc="Phần mềm bị treo logo khởi động lại liên tục",
                priority="THAP",
                repo=repo
            )

if __name__ == "__main__":
    unittest.main(verbosity=2)
