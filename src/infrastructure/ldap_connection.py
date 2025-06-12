import ldap

from src.common.exception import LDAPConnectionError
from src.config import settings


class LdapConnection:
    def __init__(self):
        self.server = settings.ldap.LDAP_SERVER
        self.user = settings.ldap.LDAP_USER
        self.password = settings.ldap.LDAP_PASSWORD

    def __enter__(self):
        try:
            self.connection = ldap.initialize(self.server)
            self.connection.simple_bind_s(self.user, self.password)
            return self.connection
        except ldap.LDAPError as e:
            raise LDAPConnectionError('Не удалось подключиться к серверу LDAP: %s', e)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.unbind_s()
