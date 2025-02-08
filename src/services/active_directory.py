import logging
import ldap
import ldap.modlist as modlist

from src.ldap_connection import LdapConnection
from src.settings import settings

logger = logging.getLogger(__name__)


class ADService:

    @classmethod
    def create_ou(cls, ou_name: str) -> str:
        """
        Создаем OU (Организационную единицу) в Active Directory
        """

        dn = f"ou={ou_name},{settings.ldap.BASE_DN}"
        attrs = {
            'objectClass': [b'top', b'organizationalUnit'],
            'ou': [ou_name.encode('utf-8')]
        }
        ldif = modlist.addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.connection.add(dn, ldif)
                logger.info(f"Организационная единица '{ou_name}' успешно создана.")
                return ou_name
            except ldap.LDAPError as e:
                logger.error(f"Ошибка при создании OU: {e}")
                return f"Ошибка: {e}"

    @classmethod
    def add_branches_to_ou(cls, ou_name: str, branches: list) -> str:
        """
        Добавляем филиалы в OU в Active Directory
        """

        ou_dn = f"ou={ou_name},{settings.ldap.BASE_DN}"

        for branch in branches:
            with LdapConnection() as conn:
                branch_dn = f"ou={branch},{ou_dn}"
                attrs = {
                    'objectClass': [b'top', b'organizationalUnit'],
                    'ou': [branch.encode('utf-8')]
                }
                ldif = modlist.addModlist(attrs)
                try:
                    conn.connection.add(branch_dn, ldif)
                    logger.info(f"Филиал '{branch}' успешно добавлен.")
                except ldap.LDAPError as e:
                    logger.error(f"Ошибка при добавлении филиала '{branch}': {e}")
                    return f"Ошибка: {e}"

        return "Все филиалы были успешно добавлены."

    @classmethod
    def check_ou_exists(cls, ou_name: str) -> bool:
        """
        Проверяем, существует ли OU (Организационная единица) в Active Directory
        """
        search_filter = f"(ou={ou_name})"
        attributes = ['ou']

        try:
            with LdapConnection() as conn:
                result = conn.connection.search_s(
                    settings.ldap.BASE_DN,
                    ldap.SCOPE_ONELEVEL,
                    search_filter,
                    attributes,
                )
                logger.info(f"Организационная единица '{ou_name}' найдена в Active Directory.")
                return result
        except ldap.LDAPError as e:
            logger.error(f"Ошибка при поиске OU: {e}")
