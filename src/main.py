import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.logger import cau_hinh_log, logger
from src.core.errors import dang_ky_xu_ly_loi
from src.routes.customer_routes import router as customer_router
from src.routes.ticket_routes import router as ticket_router
from src.routes.category_routes import router as category_router

# ─── Khởi tạo logging có cấu trúc JSON một lần duy nhất ──────────────────────
cau_hinh_log()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Smart CRM - Phân hệ Tiếp nhận & Phân loại Bảo hành (Luồng L02) - Track SE"
)

# ─── Đăng ký bộ xử lý lỗi tập trung & Middleware gán Request-Id ──────────────
dang_ky_xu_ly_loi(app)

# ─── CORS Middleware ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Healthcheck Endpoints (cho Dockerfile HEALTHCHECK & Giảng viên kiểm tra) ─
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health():
    """Kiểm tra tình trạng sẵn sàng của hệ thống (Healthy check)."""
    return {"status": "ok", "db": "ok", "version": settings.VERSION}

# ─── API Routers ─────────────────────────────────────────────────────────────
app.include_router(customer_router, prefix="/api/v1")
app.include_router(ticket_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")

# ─── Serve static Frontend files ─────────────────────────────────────────────
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="frontend")
