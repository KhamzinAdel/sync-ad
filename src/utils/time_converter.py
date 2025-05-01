from typing import Optional
from datetime import datetime


class Base62TimeConverter:
    """Кодирование и декодирование времени в формате base63."""

    _DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    @classmethod
    def to_base62(cls, dt: Optional[datetime] = None) -> str:
        """Конвертирует время в количество часов с Unix эпохи и кодирует в base62."""

        timestamp = dt.timestamp() if dt else datetime.now().timestamp()
        ts = int(timestamp // 3600)

        result = []
        while ts > 0:
            ts, rem = divmod(ts, 62)
            result.append(cls._DIGITS[rem])
        return ''.join(reversed(result)) or '0'

    @classmethod
    def from_base62(cls, base62_str: str) -> datetime:
        """Декодирует base62 строку обратно в datetime."""

        hours = 0
        for char in base62_str:
            hours = hours * 62 + cls._DIGITS.index(char)
        return datetime.fromtimestamp(hours * 3600)
