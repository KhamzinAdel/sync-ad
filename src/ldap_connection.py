import ldap

from settings import ldap_settings
from src.exceptions import LDAPConnectionError


class LdapConnection:
    def __init__(self):
        self.server = ldap_settings.LDAP_SERVER
        self.user = ldap_settings.LDAP_USER
        self.password = ldap_settings.LDAP_PASSWORD

    def __enter__(self):
        try:
            self.connection = ldap.initialize(self.server)
            self.connection.simple_bind(self.user, self.password)
            return self.connection
        except ldap.LDAPError as e:
            raise LDAPConnectionError(f"Не удалось подключиться к серверу LDAP: {e}")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.unbind()


# def main():
#    with LdapConnection() as conn:
#        print(conn)


# if __name__ == '__main__':
#     main()
