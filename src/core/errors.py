"""
src/core/errors.py
Xử lý lỗi xuyên lớp cho FastAPI (Tuần 11 - Chuẩn Phần D3).
Lớp nghiệp vụ ném lỗi có MÃ; Bộ xử lý duy nhất dịch lỗi thành HTTP và ghi log đúng một lần.
"""

import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

log = logging.getLogger("smartcrm.errors")


class LoiNghiepVu(Exception):
    """Vi phạm quy tắc nghiệp vụ (QT-xx): trả 4xx, KHÔNG phải sự cố hệ thống."""
    def __init__(self, ma: str, thong_diep: str, http_status: int = 409):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep
        self.http_status = http_status


class LoiTruyCapDuLieu(Exception):
    """Lỗi hạ tầng CSDL, mất kết nối: trả 503."""
    def __init__(self, thong_diep: str = "Lỗi kết nối cơ sở dữ liệu", cause: Exception = None):
        super().__init__(thong_diep)
        self.cause = cause


def dang_ky_xu_ly_loi(app: FastAPI):
    """Đăng ký middleware gán requestId và các exception handlers tập trung."""

    @app.middleware("http")
    async def middleware_request_id_va_log(request: Request, call_next):
        # Gán hoặc lấy request_id từ Header
        req_id = request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:8]}"
        request.state.request_id = req_id

        response = await call_next(request)
        response.headers["X-Request-Id"] = req_id
        return response

    @app.exception_handler(LoiNghiepVu)
    async def _handle_loi_nghiep_vu(request: Request, exc: LoiNghiepVu):
        req_id = getattr(request.state, "request_id", uuid.uuid4().hex[:8])
        # Lỗi nghiệp vụ chỉ log ở mức INFO
        log.info(
            f"Vi phạm quy tắc nghiệp vụ [{exc.ma}]: {exc.thong_diep}",
            extra={"request_id": req_id}
        )
        return JSONResponse(
            status_code=exc.http_status,
            content={
                "status": "error",
                "error": exc.ma,
                "message": exc.thong_diep,
                "request_id": req_id
            }
        )

    @app.exception_handler(RequestValidationError)
    async def _handle_validation_error(request: Request, exc: RequestValidationError):
        req_id = getattr(request.state, "request_id", uuid.uuid4().hex[:8])
        errors = exc.errors()
        first_msg = errors[0].get("msg", "Dữ liệu đầu vào không hợp lệ") if errors else "Validation Error"
        log.info(
            f"Lỗi xác thực dữ liệu đầu vào: {first_msg}",
            extra={"request_id": req_id}
        )
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "error": "DU_LIEU_KHONG_HOP_LE",
                "message": first_msg,
                "details": errors,
                "request_id": req_id
            }
        )

    @app.exception_handler(Exception)
    async def _handle_he_thong(request: Request, exc: Exception):
        req_id = getattr(request.state, "request_id", uuid.uuid4().hex[:8])
        # Lỗi hệ thống: log ERROR kèm toàn bộ traceback
        log.exception(
            "Lỗi hệ thống chưa được kiểm soát",
            extra={"request_id": req_id}
        )
        # KHÔNG trả str(exc) hay traceback cho người dùng
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": "LOI_HE_THONG",
                "message": f"Hệ thống đang gặp sự cố. Vui lòng thử lại. Mã tra cứu: {req_id}",
                "request_id": req_id
            }
        )
