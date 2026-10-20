import re

class CustomerService:
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Chuẩn hóa số điện thoại về dạng 10 số bắt đầu bằng 0 (QT-01, QT-02)"""
        digits = re.sub(r'\D', '', phone)
        if digits.startswith('84') and len(digits) == 11:
            digits = '0' + digits[2:]
        elif len(digits) == 9 and not digits.startswith('0'):
            digits = '0' + digits
        
        if len(digits) != 10 or not digits.startswith('0'):
            raise ValueError("Số điện thoại không hợp lệ sau khi chuẩn hóa")
        return digits

    @staticmethod
    def mask_phone(phone_normalized: str) -> str:
        """Che số điện thoại dạng 090****567 (QT-15)"""
        if len(phone_normalized) == 10:
            return phone_normalized[:3] + "****" + phone_normalized[7:]
        return phone_normalized
