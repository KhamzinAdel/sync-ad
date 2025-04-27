import logging
from infrastructure.logger import configure_logging
from services import OrganizationUnitService, ActiveDirectoryService

logger = logging.getLogger(__name__)


def sync_organizations_with_ad() -> None:
    """Вызов функции создания OU и групп"""

    organization_service: OrganizationUnitService = OrganizationUnitService()
    active_directory_service: ActiveDirectoryService = ActiveDirectoryService()

    organizations = organization_service.get_ou_to_active_directory()

    for organization in organizations:
        active_directory_service.create_uo_and_group(
            ou_name=organization.name,
            ou_path=organization.ou_path,
            base_code=organization.base_code,
        )

    logger.info('Организации cинхронизированы с AD')


if __name__ == '__main__':
    configure_logging()
    sync_organizations_with_ad()
