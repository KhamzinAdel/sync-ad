from enum import Enum


# Перечисление для области действия группы
class GroupScope(Enum):
    LOCAL_DOMAIN = 'Локальная в домене'
    GLOBAL = 'Глобальная'
    UNIVERSAL = 'Универсальная'


# Перечисление для типа группы
class GroupType(Enum):
    SECURITY = 'Безопасность'
    DISTRIBUTION = 'Группа распространения'
