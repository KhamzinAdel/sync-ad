import ldap
import time
from config import settings


def create_entries():
    try:
        # Установка соединения
        conn = ldap.initialize(settings.ldap.LDAP_SERVER)
        conn.simple_bind_s(settings.ldap.LDAP_USER, settings.ldap.LDAP_PASSWORD)

        parent_dn = 'OU=Университет,dc=stud,dc=local'

        # Поиск существующих OU (опционально)
        try:
            search_results = conn.search_s(
                parent_dn,
                ldap.SCOPE_SUBTREE,
                '(objectClass=organizationalUnit)'
            )
            print(f'Найдено {len(search_results)} организационных подразделений')
        except ldap.LDAPError as e:
            print(f'Ошибка при поиске: {e}')

        created_count = 0
        for i in range(1000):
            ou_name = f"Подразделение_{i}"
            dn = f"OU={ou_name},{parent_dn}"
            attrs = [
                ('objectClass', [b'top', b'organizationalUnit']),
                ('ou', [ou_name.encode('utf-8')])
            ]

            try:
                conn.add_s(dn, attrs)
                print(f"Создано подразделение: {dn}")
                created_count += 1
            except ldap.ALREADY_EXISTS:
                print(f"Подразделение {dn} уже существует")
                continue
            except ldap.LDAPError as e:
                print(f"Ошибка при создании OU {dn}: {e}")
                continue

        print(f"Всего создано подразделений: {created_count}")
        return True

    except ldap.LDAPError as e:
        print(f"Ошибка подключения к AD: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.unbind_s()


if __name__ == '__main__':
    start_time = time.time()
    create_entries()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения: {total_time:.2f} секунд")