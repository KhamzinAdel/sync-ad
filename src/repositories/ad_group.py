import logging
from abc import ABC, abstractmethod

import ldap
from ldap.modlist import addModlist

from config import settings
from infrastructure.ldap_connection import LdapConnection
from entities.enums import GroupScope, GroupType
from entities.schemas import ADGroupSchema

logger = logging.getLogger(__name__)


class AbstractADGroupRepository(ABC):

    @abstractmethod
    def create_access_group(self, group_name: str, ou_path: str) -> ADGroupSchema:
        raise NotImplementedError

    @abstractmethod
    def create_mailing_group(self, group_name: str, ou_path: str) -> ADGroupSchema:
        raise NotImplementedError

    @abstractmethod
    def delete_group(self, ou_dn: str) -> bool:
        raise NotImplementedError


class ADGroupRepository(AbstractADGroupRepository):
    """
    Репозиторий для работы с Active Directory Group
    """

    def create_access_group(self, group_name: str, ou_path: str) -> ADGroupSchema:
        """
        Создает группу доступа.
        - Имя группы (name) начинается с подчеркивания.
        - Имя samAccountName — без подчеркивания.
        - Область действия: глобальная.
        - Тип группы: безопасность.
        """

        name = f'_{group_name}'
        sam_account_name = group_name

        dn = f'CN={name},{ou_path}'

        attrs = {
            'objectClass': [b'top', b'group'],
            'CN': [name.encode('utf-8')],
            'sAMAccountName': [sam_account_name.encode('utf-8')],
            'groupType': [
                str(self._get_group_type_value(GroupScope.GLOBAL, GroupType.SECURITY)).encode('utf-8')
            ]
        }
        ldif = addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add_s(dn, ldif)
                return ADGroupSchema(name=name)

            except ldap.NO_SUCH_OBJECT as e:
                logger.warning("Указанный путь %s не существует: %s", ou_path, e)

            except ldap.ALREADY_EXISTS as e:
                logger.info("Группа доступа '%s' уже существует.", name)

            except ldap.LDAPError as e:
                logger.error("Ошибка при создании группы доступа: %s", e)

    def create_mailing_group(self, group_name: str, ou_path: str) -> ADGroupSchema:
        """
        Создает группу рассылки.
        - Имя группы (name) — простое.
        - Имя samAccountName начинается с русской "Р" и подчеркивания.
        - Область действия: универсальная.
        - Тип группы: распространение.
        """

        name = group_name
        sam_account_name = f'Р_{group_name}'

        dn = f'CN={name},{ou_path}'

        # Атрибуты группы
        attrs = {
            'objectClass': [b'top', b'group'],
            'CN': [name.encode('utf-8')],
            'sAMAccountName': [sam_account_name.encode('utf-8')],
            'groupType': [
                str(self._get_group_type_value(GroupScope.UNIVERSAL, GroupType.DISTRIBUTION)).encode('utf-8')
            ]
        }
        ldif = addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add_s(dn, ldif)
                return ADGroupSchema(name=name)

            except ldap.NO_SUCH_OBJECT as e:
                logger.warning("Указанный путь %s не существует: %s", ou_path, e)

            except ldap.ALREADY_EXISTS:
                logger.info("Группа рассылки '%s' уже существует.", name)

            except ldap.LDAPError as e:
                logger.error("Ошибка при создании группы рассылки: %s", e)

    def delete_group(self, group_dn: str) -> bool:
        """
        Удаляет группу из Active Directory.
        """

        with LdapConnection() as conn:
            try:
                conn.delete_s(group_dn)
                logger.info(f"Группа '{group_dn}' успешно удалена.")
                return True

            except ldap.NO_SUCH_OBJECT:
                logger.warning(f"Группа '{group_dn}' не найдена.")
                return False

            except ldap.LDAPError as e:
                logger.error(f"Ошибка при удалении группы '{group_dn}': {e}")
                return False

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
