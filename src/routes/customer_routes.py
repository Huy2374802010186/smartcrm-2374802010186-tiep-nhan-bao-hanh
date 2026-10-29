from fastapi import APIRouter
from fastapi.responses import JSONResponse
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
