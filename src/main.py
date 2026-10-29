from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from src.core.config import settings
from src.routes.customer_routes import router as customer_router
from src.routes.ticket_routes import router as ticket_router
from src.routes.category_routes import router as category_router
import os

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# ─── CORS Middleware (cho phép Frontend gọi API từ cổng khác) ──────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global Exception Handler ────────────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    error_type = first_error.get("type", "")
    if "string_too_short" in error_type:
        error_message = "Mô tả lỗi phải có ít nhất 10 ký tự (V8)"
    else:
        field = ".".join([str(loc) for loc in first_error.get("loc", []) if loc != "body"])
        error_message = (
            f"{field}: {first_error.get('msg', 'Dữ liệu không hợp lệ')}"
            if field
            else first_error.get("msg", "Dữ liệu không hợp lệ")
        )

    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": error_message},
    )

# ─── API Routers ─────────────────────────────────────────────────────────────
app.include_router(customer_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")

# ─── Serve static Frontend files ─────────────────────────────────────────────
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="frontend")

# ─── Health & Root endpoints ─────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "db": "ok", "version": settings.VERSION}
