from datetime import datetime, date
from src.services.customer_service import CustomerService
from src.services.sla_service import SLAService

class TicketService:
    @staticmethod
    def verify_warranty(purchase_date: date) -> bool:
        """Đối soát ngày mua với thời hạn bảo hành 12 tháng (QT-05)"""
        if not purchase_date:
            return False
        today = date.today()
        months = (today.year - purchase_date.year) * 12 + (today.month - purchase_date.month)
        return months <= 12

    @classmethod
    def create_ticket(
        cls,
        raw_phone: str,
        serial_no: str,
        category_id: int,
        issue_desc: str,
        priority: str = "TRUNG_BINH",
        purchase_date: date = None
    ) -> dict:
        if len(issue_desc) < 10:
            raise ValueError("Mô tả lỗi phải có ít nhất 10 ký tự (V8)")
            
        phone_norm = CustomerService.normalize_phone(raw_phone)
        phone_masked = CustomerService.mask_phone(phone_norm)
        is_warranty = cls.verify_warranty(purchase_date) if purchase_date else True
        due_date = SLAService.calculate_due_date(datetime.now(), priority)
        
        return {
            "ticket_code": "BH-000101/2026",
            "customer_phone_normalized": phone_norm,
            "customer_phone_masked": phone_masked,
            "serial_no": serial_no,
            "category_id": category_id,
            "issue_desc": issue_desc,
            "is_warranty": is_warranty,
            "priority": priority,
            "status": "MOI",
            "due_date": due_date.isoformat(),
            "created_at": datetime.now().isoformat()
        }

    @classmethod
    def create_ticket_payload(cls, customer_phone: str, serial_no: str, issue_desc: str, priority: str, purchase_date: date = None):
        return cls.create_ticket(
            raw_phone=customer_phone,
            serial_no=serial_no,
            category_id=1,
            issue_desc=issue_desc,
            priority=priority,
            purchase_date=purchase_date
        )
