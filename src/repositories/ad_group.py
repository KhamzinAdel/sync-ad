import logging
import ldap
from ldap.modlist import addModlist

from src.ldap_connection import LdapConnection
from src.settings import ldap_settings
from enums import GroupScope, GroupType

logger = logging.getLogger(__name__)


class ADGroupRepository:
    """
    Репозиторий для работы с Active Directory Group
    """

    def create_access_group(self, group_name: str, ou_path: str):
        """
        Создает группу доступа.
        - Имя группы (name) начинается с подчеркивания.
        - Имя samAccountName — без подчеркивания.
        - Область действия: глобальная.
        - Тип группы: безопасность.
        """

        name = f"_{group_name}"  # Имя группы начинается с подчеркивания
        sam_account_name = group_name  # samAccountName без подчеркивания

        # dn = f"cn={name},{ldap_settings.BASE_DN}"
        dn = f"cn={name},{ou_path}"

        attrs = {
            'objectClass': [b'top', b'group'],
            'cn': [name.encode('utf-8')],
            'sAMAccountName': [sam_account_name.encode('utf-8')],
            'groupType': [
                str(self._get_group_type_value(GroupScope.GLOBAL, GroupType.SECURITY)).encode('utf-8')
            ]
        }
        ldif = addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add(dn, ldif)
                logger.info(f"Группа доступа '{name}' успешно создана.")
                return name
            except ldap.LDAPError as e:
                logger.error(f"Ошибка при создании группы доступа: {e}")
                return f"Ошибка: {e}"

    def create_mailing_group(self, group_name: str, ou_path: str):
        """
        Создает группу рассылки.
        - Имя группы (name) — простое.
        - Имя samAccountName начинается с русской "Р" и подчеркивания.
        - Область действия: универсальная.
        - Тип группы: распространение.
        """

        name = group_name  # Имя группы
        sam_account_name = f"Р_{group_name}"  # samAccountName начинается с "Р_"

        # dn = f"cn={name},{ldap_settings.BASE_DN}"
        dn = f"cn={name},{ou_path}"

        # Атрибуты группы
        attrs = {
            'objectClass': [b'top', b'group'],
            'cn': [name.encode('utf-8')],
            'sAMAccountName': [sam_account_name.encode('utf-8')],
            'groupType': [
                str(self._get_group_type_value(GroupScope.UNIVERSAL, GroupType.DISTRIBUTION)).encode('utf-8')
            ]
        }
        ldif = addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add(dn, ldif)
                logger.info(f"Группа рассылки '{name}' успешно создана.")
                return name
            except ldap.LDAPError as e:
                logger.error(f"Ошибка при создании группы рассылки: {e}")
                return f"Ошибка: {e}"

    def _get_group_type_value(self, group_scope: GroupScope, group_type: GroupType) -> int:
        """
        Возвращает значение groupType на основе области действия и типа группы.
        """
        scope_value = {
            GroupScope.LOCAL_DOMAIN: 0x4,
            GroupScope.GLOBAL: 0x2,
            GroupScope.UNIVERSAL: 0x8
        }[group_scope]

        type_value = {
            GroupType.SECURITY: 0x80000000,
            GroupType.DISTRIBUTION: 0x00000000
        }[group_type]

        return scope_value | type_value


if __name__ == '__main__':
    repo = ADGroupRepository()

    # Путь к OU "Университет"
    ou_path = "OU=Университет,DC=server,DC=local"
    # ou_path = "OU=Университет,DC=server,DC=local"

    # Создание группы рассылки
    repo.create_mailing_group(
        group_name="Университет",
        ou_path=ou_path,
    )

    # Создание группы доступа
    repo.create_access_group(
        group_name="Университет",
        ou_path=ou_path,
    )


