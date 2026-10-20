from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime

class CustomerSearchRequest(BaseModel):
    phone: str = Field(..., example="0901234567")

class TicketCreateRequest(BaseModel):
    customer_phone: str = Field(..., example="0901234567")
    serial_no: str = Field(..., example="IMEI123456789")
    purchase_date: Optional[date] = None
    category_id: int = Field(..., example=1)
    issue_desc: str = Field(..., min_length=10, example="Màn hình chớp nháy liên tục không hiển thị")
    priority: str = Field("TRUNG_BINH", example="CAO")

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['CAO', 'TRUNG_BINH', 'THAP']:
            raise ValueError("Priority phải là CAO, TRUNG_BINH hoặc THAP")
        return v
