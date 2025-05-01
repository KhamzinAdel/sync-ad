import logging
from typing import Optional

from repositories import ADRepository, ADGroupRepository
from utils import OUBuilder


logger = logging.getLogger(__name__)


class ActiveDirectoryService:
    def __init__(self):
        self.active_directory: ADRepository = ADRepository()
        self.active_directory_group: ADGroupRepository = ADGroupRepository()

    def _create_ou(self, ou_name: str, ou_path: str) -> Optional[str]:
        update_ou_name = OUBuilder.truncate_name(ou_name)

        ou_organization = self.active_directory.create_ou(
            ou_name=update_ou_name,
            ou_path=ou_path,
        )

        if not ou_organization:
            logger.error('Не удалось создать организационную единицу: %s', ou_name)
            return None

        return ou_organization.name

    def _create_access_group(self, group_name: str, ou_path: str, base_code: str) -> Optional[str]:
        update_group_name = OUBuilder.truncate_name(group_name, 58) + '_' + base_code

        group = self.active_directory_group.create_access_group(
            group_name=update_group_name,
            ou_path=ou_path,
        )

        if not group:
            logger.warning(f'Не удалось создать группу доступа: {group_name}')
            return None

        return group.name

    def _create_mailing_group(self, group_name: str, ou_path: str, base_code: str) -> Optional[str]:
        update_group_name = OUBuilder.truncate_name(group_name, 57) + '_' + base_code

        group = self.active_directory_group.create_mailing_group(
            group_name=update_group_name,
            ou_path=ou_path,
        )

        if not group:
            logger.warning('Не удалось создать группу рассылки: %s', group_name)
            return None

        return group.name

    def create_uo_and_group(self, ou_name: str, base_code: str, ou_path: str) -> Optional[str]:
        results = {
            'access_group': 'Не создана',
            'mailing_group': 'Не создана',
        }

        ou_organization_name = self._create_ou(ou_name, ou_path)

        if not ou_organization_name:
            return None

        group_access = self._create_access_group(ou_name, f'OU={ou_organization_name},{ou_path}', base_code)

        if group_access:
            results['access_group'] = group_access

        group_mailing = self._create_mailing_group(ou_name, f'OU={ou_organization_name},{ou_path}', base_code)

        if group_mailing:
            results['mailing_group'] = group_mailing

        logger.info(
            "Создана новая организационная единица: %s. "
            "Группа доступа: %s, "
            "Группа рассылки: %s",
            ou_name,
            results['access_group'],
            results['mailing_group']
        )

        return ou_organization_name


def main():
    import time
    start_time = time.time()
    ad_service = ActiveDirectoryService()
    ou_path = "OU=Университет"
    base_name = "Подразделение_"
    for i in range(1, 1000):
        ou_name = f"{base_name}{i}"
        create_ou = ad_service.create_uo_and_group(ou_name, ou_path)
        print(f"Создано подразделение {ou_name}: {create_ou}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения: {total_time:.2f} секунд")


if __name__ == '__main__':
    main()
