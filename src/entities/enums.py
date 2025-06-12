from enum import Enum


class GroupScope(Enum):
    """Перечисление для области действия группы"""

    LOCAL_DOMAIN = 'Локальная в домене'
    GLOBAL = 'Глобальная'
    UNIVERSAL = 'Универсальная'


class GroupType(Enum):
    """Перечисление для типа группы"""

    SECURITY = 'Безопасность'
    DISTRIBUTION = 'Группа распространения'
