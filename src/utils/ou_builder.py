from src.common.constants import (
    ABBREVIATIONS,
    GROUP_NAME,
    FULL_PATH_AD,
)


class OUBuilder:
    """Формирование названия OU и пути"""

    @classmethod
    def _remove_unnecessary_char(cls, name: str) -> str:
        """
        Удаляет ВСЕ специальные символы, кроме "-" и ".",
        без добавления пробелов и схлопывания.
        """

        allowed_chars = {'-', '.', ' '}
        return ''.join(
            char for char in name
            if char.isalnum() or char in allowed_chars
        )

    @classmethod
    def build_ou_path(cls, full_path: str, parent_name: str) -> str:
        """Формирует путь к OU"""

        if full_path in FULL_PATH_AD:
            resolved_parent_name = GROUP_NAME.get(parent_name, parent_name)
            full_path = f'OU={resolved_parent_name},' + full_path

        return full_path

    @classmethod
    def truncate_name(cls, name: str, max_length: int = 64) -> str:
        """
        Сокращает имя до максимальной длины, сохраняя осмысленность.

        Процесс сокращения происходит в несколько этапов:
        1. Удаление ненужных символов
        2. Замена слов на стандартные сокращения
        3. Постепенное удаление слов с конца
        4. Удаление предлога в конце, если он остался
        """

        PREPOSITIONS = {'в', 'на', 'по', 'за', 'под', 'с', 'из', 'у', 'о', 'об', 'от', 'до', 'и'}

        resolved_name = cls._remove_unnecessary_char(name)
        if len(resolved_name) <= max_length:
            return resolved_name

        words = resolved_name.split()
        processed_words = []

        for word in words:
            lower_word = word.lower()
            replacement = ABBREVIATIONS.get(lower_word, word)
            if word.istitle():
                replacement = replacement.capitalize()
            processed_words.append(replacement)

        shortened_name = ' '.join(processed_words)
        if len(shortened_name) <= max_length:
            return shortened_name

        while processed_words and len(' '.join(processed_words)) > max_length:
            processed_words.pop()

        if processed_words and processed_words[-1].lower() in PREPOSITIONS:
            processed_words.pop()

        return ' '.join(processed_words) if processed_words else ''