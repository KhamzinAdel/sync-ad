import ldap

from settings import settings
from src.exceptions import LDAPConnectionError


class LdapConnection:
    def __init__(self):
        self.server = settings.ldap.LDAP_SERVER
        self.user = settings.ldap.LDAP_USER
        self.password = settings.ldap.LDAP_PASSWORD
        self.connection = None

    def __enter__(self):
        try:
            self.connection = ldap.initialize(self.server)
            self.connection.simple_bind(self.user, self.password)
            return self
        except ldap.LDAPError as e:
            raise LDAPConnectionError(f"Не удалось подключиться к серверу LDAP: {e}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.unbind()


# def main():
#    with LdapConnection() as ldap:
#        print(ldap.connection)


# if __name__ == '__main__':
#     main()
