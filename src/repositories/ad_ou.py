import ldap
import logging
import ldap.modlist as modlist
from abc import ABC, abstractmethod

from infrastructure.ldap_connection import LdapConnection
from entities.schemas import ADSchema, ADGuidSchema

logger = logging.getLogger(__name__)


class AbstractADRepository(ABC):
    @abstractmethod
    def create_ou(self, ou_name: str, ou_path: str):
        raise NotImplementedError

    @abstractmethod
    def delete_ou(self, ou_dn: str):
        raise NotImplementedError

    @abstractmethod
    def get_ou_guid_by_dn(self, ou_dn: str):
        raise NotImplementedError


class ADRepository(AbstractADRepository):
    """
    Репозиторий для работы с Active Directory
    """

    def create_ou(self, ou_name: str, ou_path: str) -> ADSchema:
        """
        Создаем OU (Организационную единицу) в Active Directory
        """

        dn = f"OU={ou_name},{ou_path}"
        attrs = {
            "objectClass": [b"top", b"organizationalUnit"],
            "OU": [ou_name.encode("utf-8")],
        }
        ldif = modlist.addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add_s(dn, ldif)
                return ADSchema(ou_name=ou_name, ou_path=ou_path)

            except ldap.NO_SUCH_OBJECT as e:
                logger.warning("Указанный путь %s не существует: %s", ou_path, e)

            except ldap.ALREADY_EXISTS:
                logger.warning("Организационная единица '%s' уже существует.", ou_name)

            except ldap.LDAPError as e:
                logger.error("Ошибка при создании OU: %s", e)

    def delete_ou(self, ou_dn: str) -> bool:
        """
        Удаляет OU (Организационную единицу) из Active Directory
        """

        with LdapConnection() as conn:
            try:
                conn.delete_s(ou_dn)
                logger.info(
                    "Организационная единица '%s' успешно удалена из Active Directory.",
                    ou_dn,
                )
                return True

            except ldap.NO_SUCH_OBJECT:
                logger.warning("Организационная единица '%s' не существует.", ou_dn)
                return False

            except ldap.LDAPError as e:
                logger.error("Ошибка при удалении OU '%s': %s", ou_dn, e)
                return False

    def get_ou_guid_by_dn(self, ou_dn: str) -> ADGuidSchema:
        """Получает GUID организационной единицы по её названию"""

        with LdapConnection() as conn:
            try:
                result = conn.search_s(
                    ou_dn,
                    ldap.SCOPE_BASE,
                    "(objectClass=organizationalUnit)",
                    ["objectGUID"],
                )

                return ADGuidSchema(guid=result[0][1].get("objectGUID", [None])[0])

            except ldap.NO_SUCH_OBJECT:
                logger.warning("GUID для '%s' не найден.", ou_dn)

            except ldap.LDAPError as e:
                logger.error("Ошибка при получении GUID для OU '%s': %s", ou_dn, e)
