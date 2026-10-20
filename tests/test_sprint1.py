import unittest
from datetime import datetime
from src.services.customer_service import CustomerService
from src.services.sla_service import SLAService
from src.services.ticket_service import TicketService

class TestSprint1CoreModules(unittest.TestCase):

    def test_phone_normalization_valid(self):
        self.assertEqual(CustomerService.normalize_phone("84908123456"), "0908123456")
        self.assertEqual(CustomerService.normalize_phone("+84 908 123 456"), "0908123456")
        self.assertEqual(CustomerService.normalize_phone("090 812 3456"), "0908123456")

    def test_phone_normalization_invalid(self):
        with self.assertRaises(ValueError):
            CustomerService.normalize_phone("12345")

    def test_phone_masking(self):
        self.assertEqual(CustomerService.mask_phone("0908123456"), "090****456")

    def test_sla_calculation_skip_sunday(self):
        friday_dt = datetime(2026, 10, 2, 9, 0, 0)
        due_date = SLAService.calculate_due_date(friday_dt, "TRUNG_BINH")
        expected_dt = datetime(2026, 10, 6, 9, 0, 0)
        self.assertEqual(due_date, expected_dt)

    def test_ticket_creation_success(self):
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
        service = TicketService()
        with self.assertRaises(ValueError):
            service.create_ticket(
                raw_phone="0908123456",
                serial_no="SN-A52-778901",
                category_id=1,
                issue_desc="Hỏng",
                priority="CAO"
            )

if __name__ == "__main__":
    unittest.main()
