from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from src.schemas.ticket_schema import TicketCreateRequest
from src.services.ticket_service import TicketService
from src.repositories.ticket_repository import TicketRepository

router = APIRouter(prefix="/tickets", tags=["Phiếu bảo hành"])
ticket_repo = TicketRepository()

@router.post("")
def create_ticket(payload: TicketCreateRequest):
    """Khởi tạo phiếu bảo hành mới (US1→US6, QT-01 đến QT-06)."""
    try:
        ticket = TicketService.create_ticket(
            raw_phone=payload.customer_phone,
            serial_no=payload.serial_no,
            category_id=payload.category_id,
            issue_desc=payload.issue_desc,
            priority=payload.priority,
            purchase_date=payload.purchase_date,
            repo=ticket_repo
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except KeyError as e:
        return JSONResponse(status_code=409, content={"status": "error", "message": str(e).strip("'\"")} )

    return JSONResponse(status_code=201, content={"status": "success", "data": ticket})


@router.get("")
def list_tickets(
    status: Optional[str] = Query(None, description="Lọc theo trạng thái: MOI, DANG_XU_LY, HOAN_TAT"),
    overdue_only: bool = Query(False, description="Chỉ lấy phiếu quá hạn SLA"),
    keyword: Optional[str] = Query(None, description="Tìm theo mã phiếu / IMEI / SĐT"),
):
    """Danh sách & lọc phiếu bảo hành (US7, QT-04 - đánh dấu quá hạn SLA)."""
    from datetime import datetime
    tickets = ticket_repo.list_all(status=status, overdue_only=overdue_only)

    # Lọc theo keyword
    if keyword:
        kw = keyword.lower()
        tickets = [
            t for t in tickets
            if kw in t.get("ticket_code", "").lower()
            or kw in t.get("serial_no", "").lower()
            or kw in t.get("customer_phone_normalized", "").lower()
            or kw in t.get("customer_phone_masked", "").lower()
        ]

    # Đánh dấu is_overdue và warning_sla cho từng phiếu
    now = datetime.now()
    for t in tickets:
        due_str = t.get("due_date", "")
        if due_str:
            try:
                due = datetime.fromisoformat(due_str)
                t["is_overdue"] = due < now
                t["warning_sla"] = not t["is_overdue"] and (due - now).total_seconds() < 4 * 3600
            except Exception:
                t["is_overdue"] = False
                t["warning_sla"] = False

    return JSONResponse(
        status_code=200,
        content={"status": "success", "total": len(tickets), "data": tickets}
    )


@router.get("/{ticket_code}")
def get_ticket(ticket_code: str):
    """Chi tiết phiếu bảo hành kèm log trạng thái (M3)."""
    ticket = ticket_repo.find_by_code(ticket_code)
    if not ticket:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": f"Không tìm thấy phiếu {ticket_code}"}
        )
    return JSONResponse(status_code=200, content={"status": "success", "data": ticket})
