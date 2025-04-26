import logging
from logger import configure_logging
from services import OrganizationUnitService, ActiveDirectoryService


from entities.schemas import OrganizationUnitADSchema

logger = logging.getLogger(__name__)


#def sync_organizations_with_ad() -> None:
#    """Вызов функции создания OU и групп"""

 #   organization_service: OrganizationUnitService = OrganizationUnitService()
 #   active_directory_service: ActiveDirectoryService = ActiveDirectoryService()

#    organizations = organization_service.get_ou_to_active_directory()

#    for organization in organizations:
#        active_directory_service.create_uo_and_group(
#            ou_name=organization.name,
#            ou_path=organization.ou_path,
#            base_code=organization.base_code,
#        )

#    logger.info('Организации cинхронизированы с AD')


def sync_organizations_with_ad_text() -> None:
    """Вызов функции создания OU и групп (тестовые данные)"""

    organization_service: OrganizationUnitService = OrganizationUnitService()
    active_directory_service: ActiveDirectoryService = ActiveDirectoryService()

    # Генерация тестовых организаций вместо получения из сервиса
    test_organizations = [
        OrganizationUnitADSchema(
            name=f"Тест_{i}",
            ou_path=f"OU=Университет",
            base_code=f"TEST_{i}"
        )
        for i in range(1, 10)  # Создаем 100 тестовых организаций
    ]

    for organization in test_organizations:
        active_directory_service.create_uo_and_group(
            ou_name=organization.name,
            ou_path=organization.ou_path,
            base_code=organization.base_code,
        )


if __name__ == '__main__':
    import time

    start_time = time.time()
    configure_logging(level=logging.DEBUG)  # Включаем DEBUG для детального логгирования
    sync_organizations_with_ad_text()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Общее время выполнения: {total_time:.2f} секунд")


#if __name__ == '__main__':
 #   configure_logging()
 #   sync_organizations_with_ad()
