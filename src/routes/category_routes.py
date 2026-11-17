from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/categories", tags=["Nhóm sự cố"])

# Danh mục nhóm sự cố (in-memory, đồng bộ db/seed.sql)
_CATEGORIES = [
    {"category_id": 1, "category_name": "MÀN_HÌNH",  "default_priority": "CAO",       "description": "Lỗi sọc màn hình, chớp nháy, chảy mực, vỡ kính cảm ứng", "is_active": True},
    {"category_id": 2, "category_name": "PIN_NGUỒN",  "default_priority": "TRUNG_BINH","description": "Chai pin, pin phồng, sạc không vào, sập nguồn đột ngột",  "is_active": True},
    {"category_id": 3, "category_name": "PHẦN_MỀM",   "default_priority": "THAP",      "description": "Lỗi hệ điều hành, treo logo, quên mật khẩu, lỗi ứng dụng","is_active": True},
    {"category_id": 4, "category_name": "NƯỚC_VÀO",   "default_priority": "CAO",       "description": "Thiết bị ngấm nước, ẩm ướt linh kiện nội bộ",             "is_active": True},
    {"category_id": 5, "category_name": "KHÁC",        "default_priority": "TRUNG_BINH","description": "Các sự cố phần cứng, camera, loa, mic hoặc linh kiện khác","is_active": True},
]

@router.get("")
def list_categories():
    """Lấy danh sách tất cả nhóm sự cố đang hoạt động."""
    active = [c for c in _CATEGORIES if c["is_active"]]
    return JSONResponse(
        status_code=200,
        content={"status": "success", "total": len(active), "data": active}
    )

@router.get("/{category_id}")
def get_category(category_id: int):
    """Lấy chi tiết một nhóm sự cố theo ID."""
    cat = next((c for c in _CATEGORIES if c["category_id"] == category_id), None)
    if not cat:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Nhóm sự cố không tồn tại."})
    return JSONResponse(status_code=200, content={"status": "success", "data": cat})
