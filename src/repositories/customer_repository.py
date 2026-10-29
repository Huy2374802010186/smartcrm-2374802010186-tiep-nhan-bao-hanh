from typing import Optional, Dict, Any

# ─── Dữ liệu khách hàng mẫu đồng bộ db/seed.sql (12 KH) ─────────────────────
_CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "0908123456": {"customer_id": 101, "full_name": "Nguyễn Văn An",      "phone": "0908123456", "phone_normalized": "0908123456", "email": "an.nguyen@email.com",    "segment": "VIP"},
    "0912345678": {"customer_id": 102, "full_name": "Trần Thị Bình",      "phone": "0912345678", "phone_normalized": "0912345678", "email": "binh.tran@email.com",    "segment": "THUONG_XUYEN"},
    "0987654321": {"customer_id": 103, "full_name": "Lê Văn Cường",       "phone": "0987654321", "phone_normalized": "0987654321", "email": "cuong.le@email.com",     "segment": "MOI"},
    "0901234567": {"customer_id": 104, "full_name": "Nguyễn Văn A",       "phone": "0901234567", "phone_normalized": "0901234567", "email": "nguyenvana@gmail.com",   "segment": "VIP"},
    "0903456789": {"customer_id": 105, "full_name": "Phạm Thị Dung",      "phone": "0903456789", "phone_normalized": "0903456789", "email": "dung.pham@gmail.com",    "segment": "THUONG_XUYEN"},
    "0971234567": {"customer_id": 106, "full_name": "Hoàng Minh Tuấn",    "phone": "0971234567", "phone_normalized": "0971234567", "email": "tuan.hoang@email.com",   "segment": "VIP"},
    "0961234567": {"customer_id": 107, "full_name": "Vũ Thị Lan",         "phone": "0961234567", "phone_normalized": "0961234567", "email": "lan.vu@email.com",       "segment": "MOI"},
    "0931234567": {"customer_id": 108, "full_name": "Đặng Văn Hải",       "phone": "0931234567", "phone_normalized": "0931234567", "email": "hai.dang@email.com",     "segment": "THUONG_XUYEN"},
    "0941234567": {"customer_id": 109, "full_name": "Ngô Thị Thu",        "phone": "0941234567", "phone_normalized": "0941234567", "email": "thu.ngo@email.com",      "segment": "MOI"},
    "0951234567": {"customer_id": 110, "full_name": "Lý Văn Phúc",        "phone": "0951234567", "phone_normalized": "0951234567", "email": "phuc.ly@email.com",      "segment": "VIP"},
    "0921234567": {"customer_id": 111, "full_name": "Bùi Thị Hoa",        "phone": "0921234567", "phone_normalized": "0921234567", "email": "hoa.bui@email.com",      "segment": "THUONG_XUYEN"},
    "0911234567": {"customer_id": 112, "full_name": "Trịnh Văn Khoa",     "phone": "0911234567", "phone_normalized": "0911234567", "email": "khoa.trinh@email.com",   "segment": "MOI"},
}

class CustomerRepository:
    def __init__(self):
        self._customers = _CUSTOMERS

    def find_by_phone_number(self, phone: str) -> Optional[Dict[str, Any]]:
        """Tra cứu khách hàng theo SĐT đã chuẩn hóa 10 số."""
        return self._customers.get(phone)
