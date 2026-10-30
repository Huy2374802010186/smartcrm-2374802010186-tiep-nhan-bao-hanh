"""
src/core/logger.py
Bộ ghi nhật ký có cấu trúc JSON ra stdout (Tuần 11 - Chuẩn Phần D2 & QT-15).
Ghi ra stdout để `docker compose logs` đọc được. Tuyệt đối không ghi ra file trong container.
"""

import json
import logging
import os
import re
import sys
from typing import Any, Dict

# Danh sách từ khóa trường nhạy cảm cần che
TRUONG_CHE = (
    "password", "mat_khau", "token", "jwt", "authorization",
    "secret", "cvv", "so_the", "customer_phone", "raw_phone", "phone"
)

# Regex nhận diện số điện thoại Việt Nam (10 số, bắt đầu bằng 03, 05, 07, 08, 09)
REGEX_PHONE = re.compile(r"(0[3|5|7|8|9]\d)(\d{4})(\d{3})")


def mask_phone_str(text: str) -> str:
    """Che số điện thoại trong chuỗi text theo quy tắc QT-15: 0908123456 -> 090****456."""
    return REGEX_PHONE.sub(r"\1****\3", text)


def che_du_lieu_nhay_cam(obj: Any) -> Any:
    """Duyệt đệ quy và che các trường dữ liệu nhạy cảm."""
    if obj is None or isinstance(obj, (int, float, bool)):
        return obj
    if isinstance(obj, str):
        return mask_phone_str(obj)
    if isinstance(obj, Exception):
        return {"loai": type(obj).__name__, "thong_diep": mask_phone_str(str(obj))}
    if isinstance(obj, list):
        return [che_du_lieu_nhay_cam(item) for item in obj]
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            k_lower = str(k).lower()
            if any(t in k_lower for t in TRUONG_CHE):
                if isinstance(v, str) and REGEX_PHONE.match(v):
                    out[k] = mask_phone_str(v)
                else:
                    out[k] = "***"
            else:
                out[k] = che_du_lieu_nhay_cam(v)
        return out
    return str(obj)


class DinhDangJson(logging.Formatter):
    """Mỗi dòng log là một đối tượng JSON: thoi_diem, muc, nguon, thong_diep, request_id."""
    TRUONG_NGU_CANH = ("request_id", "ma_lo", "ticket_code", "serial_no", "so_dong")

    def format(self, record: logging.LogRecord) -> str:
        d: Dict[str, Any] = {
            "thoi_diem": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "muc": record.levelname,
            "nguon": record.name,
            "thong_diep": mask_phone_str(record.getMessage()),
        }

        for k in self.TRUONG_NGU_CANH:
            if hasattr(record, k):
                d[k] = getattr(record, k)

        if record.exc_info:
            d["loi"] = self.formatException(record.exc_info)

        return json.dumps(che_du_lieu_nhay_cam(d), ensure_ascii=False)


def cau_hinh_log():
    """Cấu hình logging một lần duy nhất tại điểm vào chương trình."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(DinhDangJson())
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level, handlers=[handler], force=True)


# Logger mặc định cho hệ thống
logger = logging.getLogger("smartcrm")
