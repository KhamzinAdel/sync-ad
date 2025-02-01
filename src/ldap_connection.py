import ldap

from .config import ldap_settings as settings
from .exceptions import LDAPConnectionError


class LdapConnection:
    def __init__(self):
        self.server = settings.LDAP_SERVER
        self.user = settings.LDAP_USER
        self.password = settings.LDAP_PASSWORD
        self.connection = None

    async def __aenter__(self):
        try:
            self.connection = ldap.initialize(self.server)
            self.connection.simple_bind(self.user, self.password)
            return self
        except ldap.LDAPError as e:
            raise LDAPConnectionError(f"Не удалось подключиться к серверу LDAP: {e}")

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.unbind()


# async def main():
#    async with LdapConnection() as ldap:
#        print(ldap.connection)
#
#    async with LdapConnection() as ldap:
#        print(ldap.connection)


# asyncio.run(main())
