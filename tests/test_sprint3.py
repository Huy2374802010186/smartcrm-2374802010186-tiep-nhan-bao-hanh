"""Sprint 3 — 4 test cases bổ sung cho đủ 12 (Buổi 13/14).

TC09-TC10: bảo hành 12 tháng (QT-05) — unit.
TC11: seed SQL chạy lại được (tái lập) — kiểm tra tĩnh file SQL.
TC12: System API POST /api/v1/tickets → 201 — TestClient.
"""
import os
import unittest
from datetime import date, timedelta

from fastapi.testclient import TestClient

from src.main import app
from src.services.ticket_service import TicketService

SQL_DIR = os.path.join(os.path.dirname(__file__), "..", "db")


class TestSprint3Buoi1314(unittest.TestCase):
    def test_TC09_verify_warranty_valid(self):
        """QT-05: mua cách đây 3 tháng → còn bảo hành."""
        purchase = date.today() - timedelta(days=90)
        self.assertTrue(TicketService.verify_warranty(purchase))

    def test_TC10_warranty_boundary_12_months(self):
        """QT-05 biên: ~360 ngày → True; ~400 ngày → False."""
        self.assertTrue(TicketService.verify_warranty(date.today() - timedelta(days=360)))
        self.assertFalse(TicketService.verify_warranty(date.today() - timedelta(days=400)))

    def test_TC11_seed_rerunnable(self):
        """Tái lập: seed.sql dùng ON CONFLICT DO NOTHING nên chạy lại không lỗi PK."""
        with open(os.path.join(SQL_DIR, "seed.sql"), encoding="utf-8") as f:
            seed = f.read().upper()
        inserts = [ln for ln in seed.splitlines() if ln.strip().startswith("INSERT")]
        self.assertEqual(len(inserts), 3)
        self.assertEqual(seed.count("ON CONFLICT"), len(inserts))

    def test_TC12_system_api_create_ticket(self):
        """System API: POST /api/v1/tickets → 201, mã BH-, status MOI, SĐT đã mask."""
        client = TestClient(app)
        resp = client.post("/api/v1/tickets", json={
            "customer_phone": "+84 908 123 456",
            "serial_no": "SN-TC12-999001",
            "category_id": 1,
            "issue_desc": "Màn hình chớp nháy sọc ngang không hiển thị",
            "priority": "CAO",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()["data"]
        self.assertTrue(data["ticket_code"].startswith("BH-"))
        self.assertEqual(data["status"], "MOI")
        self.assertEqual(data["customer_phone_masked"], "090****456")


if __name__ == "__main__":
    unittest.main(verbosity=2)
