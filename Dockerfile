# ═════════════════════════════════════════════════════════════════════════════
# Dockerfile — Multi-stage Build cho Smart CRM (Track SE - Luồng L02)
# Chuẩn Tuần 11: Ghim phiên bản, chép tệp khóa trước, user phi đặc quyền, HEALTHCHECK
# ═════════════════════════════════════════════════════════════════════════════

# ---------- GIAI ĐOẠN 1: Cài đặt phụ thuộc (Builder) ----------
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Chép tệp khóa phiên bản trước để tận dụng Docker cache layer
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && pip install --no-cache-dir --prefix=/opt/venv -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

# ---------- GIAI ĐOẠN 2: Ảnh chạy siêu nhẹ (Runtime) ----------
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Tạo người dùng không đặc quyền (appuser UID 10001) - bảo mật hệ thống
RUN groupadd -g 10001 appgroup && \
    useradd -m -u 10001 -g appgroup appuser

# Chép virtualenv từ giai đoạn builder
COPY --from=builder /opt/venv /opt/venv

# Chép mã nguồn ứng dụng và thư mục dữ liệu mẫu
COPY --chown=appuser:appgroup src ./src
COPY --chown=appuser:appgroup db ./db

# Chuyển sang user phi đặc quyền
USER appuser

EXPOSE 8000

# Healthcheck định kỳ để Docker Compose kiểm tra tình trạng sống của API
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status == 200 else 1)"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
