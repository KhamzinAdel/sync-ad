import logging
import re

from repositories import ADRepository, ADGroupRepository
from entities import GroupScope, GroupType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ad_rep = ADRepository()

ad_group_rep = ADGroupRepository()

group_scope_data = {
    "GLOBAL": GroupScope.GLOBAL,
    "UNIVERSAL": GroupScope.UNIVERSAL,
}

group_type_data = {
    "SECURITY": GroupType.SECURITY,
    "DISTRIBUTION": GroupType.DISTRIBUTION,
}


def read_and_create_ous():
    count = 0

    with open('ou.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("OU="):
                ou_path = line.strip()
                ou_name = ou_path.split(",")[0].split("=")[1]
                parent_path = ",".join(ou_path.split(",")[1:-3])
                try:
                    ad_rep.create_ou(ou_name, parent_path)
                    count += 1
                except Exception as e:
                    logger.error(f"Не удалось создать OU '{ou_name}': {e}")

    print(count)


def read_and_create_groups():
    with open('group.txt', 'r', encoding='utf-8') as file:
        file_read = file.read()

    blocks = re.split(r'\n\s*\n', file_read.strip())
    data = {}

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines[-1].split(',')) > 5:
            for line in lines:
                key, value = line.split(':')
                data[key.strip()] = value.strip()

        ad_group_rep.create_group_from_txt(
            group_name=data.get('Name'),
            sam_account_name=data.get('SamAccountName'),
            group_scope=group_scope_data.get(data.get('GroupScope').upper()),
            group_type=group_type_data.get(data.get('GroupCategory').upper()),
            ou_path=",".join(data.get('DistinguishedName').split(',')[1:-3]),
        )

if __name__ == '__main__':
    read_and_create_groups()



    def create_group_from_txt(
            self, group_name: str, sam_account_name: str, group_scope: GroupScope, group_type: GroupType, ou_path: str
    ):
        dn = f"CN={group_name},{ou_path},{ldap_settings.BASE_DN}"

        attrs = {
            'objectClass': [b'top', b'group'],
            'CN': [group_name.encode('utf-8')],
            'sAMAccountName': [sam_account_name.encode('utf-8')],
            'groupType': [
                str(self._get_group_type_value(group_scope, group_type)).encode('utf-8')
            ]
        }
        ldif = addModlist(attrs)

        with LdapConnection() as conn:
            try:
                conn.add_s(dn, ldif)
                logger.info(f"Группа доступа '{group_name}' успешно создана.")
            except ldap.LDAPError as e:
                logger.error(f"Ошибка при создании группы доступа: {e}")
                return f"Ошибка: {e}"
