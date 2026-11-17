from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from src.schemas.ticket_schema import CustomerSearchRequest
from src.services.customer_service import CustomerService
from src.repositories.customer_repository import CustomerRepository

router = APIRouter(prefix="/customers", tags=["Khách hàng"])
customer_repo = CustomerRepository()

@router.post("/search")
def search_customer(payload: CustomerSearchRequest):
    try:
        customer = CustomerService.get_customer_by_phone(payload.phone, customer_repo)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(e)
            }
        )
    
    if not customer:
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": "Không tìm thấy thông tin khách hàng với số điện thoại này."
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": customer
        }
    )


class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None


class CustomerPatch(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    segment: Optional[str] = None


@router.get("")
def list_customers():
    """Lấy danh sách khách hàng (CRUD-R)."""
    return JSONResponse(status_code=200, content={
        "status": "success",
        "total": len(customer_repo.list_all()),
        "data": customer_repo.list_all()
    })


@router.post("")
def create_customer(payload: CustomerCreate):
    """Thêm khách hàng mới (CRUD-C)."""
    try:
        phone_norm = CustomerService.normalize_phone(payload.phone)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    try:
        customer = customer_repo.create({
            "full_name": payload.full_name,
            "phone": phone_norm,
            "phone_normalized": phone_norm,
            "email": payload.email,
            "segment": "MOI",
        })
    except KeyError as e:
        return JSONResponse(status_code=409, content={"status": "error", "message": str(e).strip("'\"")})
    return JSONResponse(status_code=201, content={"status": "success", "data": customer})


@router.patch("/{phone}")
def update_customer(phone: str, payload: CustomerPatch):
    """Cập nhật khách hàng (CRUD-U)."""
    try:
        phone_norm = CustomerService.normalize_phone(phone)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    patch = {k: v for k, v in payload.model_dump().items() if v is not None}
    customer = customer_repo.update(phone_norm, patch)
    if not customer:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Không tìm thấy khách hàng."})
    return JSONResponse(status_code=200, content={"status": "success", "data": customer})


@router.delete("/{phone}")
def delete_customer(phone: str):
    """Xóa khách hàng (CRUD-D)."""
    try:
        phone_norm = CustomerService.normalize_phone(phone)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    removed = customer_repo.delete(phone_norm)
    if not removed:
        return JSONResponse(status_code=404, content={"status": "error", "message": "Không tìm thấy khách hàng."})
    return JSONResponse(status_code=200, content={"status": "success", "data": removed})
