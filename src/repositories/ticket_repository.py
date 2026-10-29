from typing import Optional, Dict, Any, List
from datetime import datetime

# ─── Dữ liệu seed in-memory đồng bộ db/seed.sql ─────────────────────────────
_SEED_TICKETS: List[Dict[str, Any]] = [
    {
        "ticket_id": 1,
        "ticket_code": "BH-000001/2026",
        "customer_phone_normalized": "0908123456",
        "customer_phone_masked": "090****456",
        "serial_no": "SN-A52-778901",
        "category_id": 1,
        "category_name": "MÀN_HÌNH",
        "customer_name": "Nguyễn Văn An",
        "issue_desc": "Màn hình chớp nháy sọc ngang không hiển thị đúng màu",
        "is_warranty": True,
        "priority": "CAO",
        "status": "MOI",
        "due_date": "2026-10-24T09:00:00",
        "created_at": "2026-10-23T09:00:00",
        "status_log": [
            {"from_status": None, "to_status": "MOI", "note": "Khởi tạo phiếu tiếp nhận bảo hành", "changed_by": "SYSTEM", "changed_at": "2026-10-23T09:00:00"}
        ]
    },
    {
        "ticket_id": 2,
        "ticket_code": "BH-000002/2026",
        "customer_phone_normalized": "0912345678",
        "customer_phone_masked": "091****678",
        "serial_no": "SN-S21-441207",
        "category_id": 2,
        "category_name": "PIN_NGUỒN",
        "customer_name": "Trần Thị Bình",
        "issue_desc": "Pin chai không sạc được điện, thời lượng giảm nhanh",
        "is_warranty": False,
        "priority": "TRUNG_BINH",
        "status": "DANG_XU_LY",
        "due_date": "2026-10-23T12:00:00",   # sắp quá hạn
        "created_at": "2026-10-20T09:00:00",
        "status_log": [
            {"from_status": None,    "to_status": "MOI",        "note": "Khởi tạo phiếu",               "changed_by": "SYSTEM",      "changed_at": "2026-10-20T09:00:00"},
            {"from_status": "MOI",   "to_status": "DANG_XU_LY", "note": "Phân công kỹ thuật viên",      "changed_by": "nam.nguyen",  "changed_at": "2026-10-20T10:30:00"},
        ]
    },
    {
        "ticket_id": 3,
        "ticket_code": "BH-000003/2026",
        "customer_phone_normalized": "0987654321",
        "customer_phone_masked": "098****321",
        "serial_no": "SN-IP12-990113",
        "category_id": 3,
        "category_name": "PHẦN_MỀM",
        "customer_name": "Lê Văn Cường",
        "issue_desc": "Hệ điều hành bị treo logo khi khởi động máy",
        "is_warranty": True,
        "priority": "THAP",
        "status": "HOAN_TAT",
        "due_date": "2026-10-15T09:00:00",   # đã quá hạn
        "created_at": "2026-10-10T14:00:00",
        "status_log": [
            {"from_status": None,        "to_status": "MOI",        "note": "Khởi tạo phiếu",          "changed_by": "SYSTEM",     "changed_at": "2026-10-10T14:00:00"},
            {"from_status": "MOI",       "to_status": "DANG_XU_LY", "note": "Bắt đầu cài lại phần mềm","changed_by": "kv.hung",    "changed_at": "2026-10-11T08:00:00"},
            {"from_status": "DANG_XU_LY","to_status": "HOAN_TAT",   "note": "Đã sửa xong, trả máy",    "changed_by": "kv.hung",    "changed_at": "2026-10-14T16:30:00"},
        ]
    },
]


class TicketRepository:
    def __init__(self):
        self._tickets: List[Dict[str, Any]] = list(_SEED_TICKETS)
        self._counter: int = len(_SEED_TICKETS) + 1

    def find_open_by_serial(self, serial: str) -> Optional[Dict[str, Any]]:
        """Kiểm tra thiết bị đang có phiếu chưa đóng (QT-03)."""
        for t in self._tickets:
            if t.get("serial_no") == serial and t.get("status") not in ["HOAN_TAT", "DA_DONG", "DA_HUY"]:
                return t
        return None

    def find_by_code(self, ticket_code: str) -> Optional[Dict[str, Any]]:
        """Lấy chi tiết phiếu theo mã phiếu (cho M3)."""
        for t in self._tickets:
            if t.get("ticket_code") == ticket_code:
                return t
        return None

    def save(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Lưu phiếu mới, tự động sinh ticket_id và ticket_code (QT-06)."""
        ticket = dict(ticket_data)
        ticket["ticket_id"] = self._counter
        ticket["ticket_code"] = f"BH-{self._counter:06d}/2026"
        ticket["status_log"] = [
            {
                "from_status": None,
                "to_status": "MOI",
                "note": "Khởi tạo phiếu tiếp nhận bảo hành tự động",
                "changed_by": "SYSTEM",
                "changed_at": datetime.now().isoformat()
            }
        ]
        self._counter += 1
        self._tickets.append(ticket)
        return ticket

    def list_all(
        self,
        status: Optional[str] = None,
        overdue_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Danh sách phiếu với bộ lọc trạng thái và SLA (US7)."""
        results = list(self._tickets)
        if status:
            results = [t for t in results if t.get("status") == status]
        if overdue_only:
            now = datetime.now()
            results = [
                t for t in results
                if t.get("due_date") and datetime.fromisoformat(t["due_date"]) < now
            ]
        return results
