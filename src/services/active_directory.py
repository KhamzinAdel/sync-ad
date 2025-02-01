import logging
import ldap
import ldap.modlist as modlist

from src.ldap_connection import LdapConnection
from src.config import ldap_settings as settings

logger = logging.getLogger(__name__)


class ADService:

    @classmethod
    async def create_ou(cls, ou_name: str) -> str:
        """
        Создаем OU (Организационную единицу) в Active Directory
        """

        dn = f"ou={ou_name},{settings.BASE_DN}"
        attrs = {
            'objectClass': [b'top', b'organizationalUnit'],
            'ou': [ou_name.encode('utf-8')]
        }
        ldif = modlist.addModlist(attrs)

        async with LdapConnection() as ldap_connection:
            try:
                ldap_connection.connection.add(dn, ldif)
                logger.info(f"Организационная единица '{ou_name}' успешно создана.")
                return ou_name
            except ldap.LDAPError as e:
                # logger.error(f"Ошибка при создании OU: {e}")
                return f"Ошибка: {e}"

    @classmethod
    async def add_branches_to_ou(cls, ou_name: str, branches: list) -> str:
        """
        Добавляем филиалы в OU в Active Directory
        """

        ou_dn = f"ou={ou_name},{settings.BASE_DN}"

        for branch in branches:
            async with LdapConnection() as ldap_connection:
                branch_dn = f"ou={branch},{ou_dn}"
                attrs = {
                    'objectClass': [b'top', b'organizationalUnit'],
                    'ou': [branch.encode('utf-8')]
                }
                ldif = modlist.addModlist(attrs)
                try:
                    ldap_connection.connection.add(branch_dn, ldif)
                    logger.info(f"Филиал '{branch}' успешно добавлен.")
                except ldap.LDAPError as e:
                    logger.error(f"Ошибка при добавлении филиала '{branch}': {e}")
                    return f"Ошибка: {e}"

        return "Все филиалы были успешно добавлены."
