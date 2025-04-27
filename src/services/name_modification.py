from datetime import datetime
from typing import Optional

from common.constants import ABBREVIATIONS


class Base36TimeConverter:
    """Кодирование и декодирование времени в формате base36."""

    _DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'

    @classmethod
    def to_base_36(cls, dt: Optional[datetime] = None) -> str:
        """Конвертирует время в количество часов с Unix эпохи и кодирует в base36."""

        result = ''
        timestamp = dt.timestamp() if dt else datetime.now().timestamp()

        ts = int(timestamp // 3600)

        while ts:
            ts, r = divmod(ts, 36)
            result = cls._DIGITS[r] + result

        return result or '0'

    @classmethod
    def from_base_36(cls, base36_str: str) -> datetime:
        """Декодирует base36 строку обратно в datetime"""

        hours = int(base36_str, 36)
        return datetime.fromtimestamp(hours * 3600)


class OUBuilder:
    """Формирование названия OU и пути"""

    @classmethod
    def remove_unnecessary_char(cls, name: str) -> str:
        """
        Удаляет ВСЕ специальные символы, кроме "-" и ".",
        без добавления пробелов и схлопывания.
        """
        allowed_chars = {'-', '.', '/', ' '}
        return ''.join(
            char for char in name
            if char.isalnum() or char in allowed_chars
        )

    @classmethod
    def build_ou_path(cls, full_name: str, parent_name: str) -> str:

        # Разделяем full_name на части и чистим от пробелов
        name_parts = [part.strip() for part in full_name.split('/')]

        allowed_name_parts = [cls.remove_unnecessary_char(name_part) for name_part in name_parts]

        ou_parts = [f'OU={part}' for part in allowed_name_parts[1:-1]] + \
                   [f'OU={parent_name}'] + [f'OU={allowed_name_parts[-1]}']

        return ','.join(ou_parts)

    @classmethod
    def truncate_name(cls, name: str, max_length: int = 64) -> str:
        """
        Сокращает имя до максимальной длины, сохраняя осмысленность.
        Сначала применяет стандартные сокращения, затем, если необходимо, удаляем слова в конце.
        """

        if len(name) <= max_length:
            return cls.remove_unnecessary_char(name)

        words = name.split()
        result_words = []

        for word in words:
            lower_word = word.lower()
            if lower_word in ABBREVIATIONS:
                if word.istitle():
                    result_words.append(ABBREVIATIONS[lower_word].capitalize())
                else:
                    result_words.append(ABBREVIATIONS[lower_word].lower())
            else:
                result_words.append(word)

        shortened_name = ' '.join(result_words)

        if len(shortened_name) <= max_length:
            return cls.remove_unnecessary_char(shortened_name)

        while len(shortened_name) > max_length and result_words:
            result_words.pop()
            shortened_name = ' '.join(result_words)

        return cls.remove_unnecessary_char(shortened_name)
