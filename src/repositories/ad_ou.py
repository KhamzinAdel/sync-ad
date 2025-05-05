import ldap
import logging
import ldap.modlist as modlist
from abc import ABC, abstractmethod

from config import settings
from entities.schemas import ADSchema

logger = logging.getLogger(__name__)


class AbstractADRepository(ABC):

    @abstractmethod
    def create_ou(self, ou_name: str, ou_path: str) -> ADSchema:
        raise NotImplementedError

    @abstractmethod
    def check_ou_exists(self, ou_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_ou(self, ou_dn: str) -> bool:
        raise NotImplementedError


class ADRepository(AbstractADRepository):
    """
    Репозиторий для работы с Active Directory
    """

    def __init__(self):
        self._conn = None

    def set_connection(self, conn):
        """Установить внешнее соединение"""

        self._conn = conn

    def create_ou(self, ou_name: str, ou_path: str) -> ADSchema:
        """
        Создаем OU (Организационную единицу) в Active Directory
        """

        dn = f'OU={ou_name},{ou_path}'
        attrs = {
            'objectClass': [b'top', b'organizationalUnit'],
            'OU': [ou_name.encode('utf-8')]
        }
        ldif = modlist.addModlist(attrs)

        try:
            self._conn.add_s(dn, ldif)
            with open('ou_create.txt', 'a') as f:
                f.write(f"{dn}\n")
            return ADSchema(name=ou_name)

        except ldap.NO_SUCH_OBJECT as e:
            logger.warning("Указанный путь %s не существует: %s", ou_path, e)

        except ldap.ALREADY_EXISTS:
            logger.info("Организационная единица '%s' уже существует.", ou_name)

        except ldap.LDAPError as e:
            logger.error("Ошибка при создании OU: %s", e)

    def check_ou_exists(self, ou_name: str) -> bool:
        """
        Проверяем, существует ли OU (Организационная единица) в Active Directory
        """
        search_filter = f'(OU={ou_name})'
        attributes = ['OU']

        try:
            result = self._conn.search_s(
                settings.ldap.BASE_DN,
                ldap.SCOPE_ONELEVEL,
                search_filter,
                attributes,
            )
            logger.info("Организационная единица '%s' найдена в Active Directory.", ou_name)
            return result
        except ldap.LDAPError as e:
            logger.error("Ошибка при поиске OU: %s", e)

    def delete_ou(self, ou_dn: str) -> bool:
        """
        Удаляет OU (Организационную единицу) из Active Directory
        """

        try:
            self._conn.delete_s(ou_dn)
            logger.info("Организационная единица '%s' успешно удалена из Active Directory.", ou_dn)
            return True

        except ldap.NO_SUCH_OBJECT:
            logger.warning("Организационная единица '%s' не существует.", ou_dn)
            return False

        except ldap.LDAPError as e:
            logger.error("Ошибка при удалении OU '%s': %s", ou_dn, e)
            return False
