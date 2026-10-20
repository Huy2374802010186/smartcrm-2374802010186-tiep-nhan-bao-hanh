from datetime import datetime, timedelta

class SLAService:
    SLA_HOURS = {
        'CAO': 24,        # 1 ngày làm việc
        'TRUNG_BINH': 72, # 3 ngày làm việc
        'THAP': 120       # 5 ngày làm việc
    }

    @classmethod
    def calculate_due_date(cls, start_time: datetime, priority: str) -> datetime:
        """Tính thời hạn SLA due_date bỏ qua ngày Chủ Nhật (QT-04)"""
        target_hours = cls.SLA_HOURS.get(priority, 72)
        current = start_time
        added_hours = 0
        
        while added_hours < target_hours:
            current += timedelta(hours=1)
            if current.weekday() != 6:
                added_hours += 1
                
        return current
