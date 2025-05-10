import logging
from infrastructure.logger import configure_logging
from services import OrganizationUnitService, ADService, AdGroupService

logger = logging.getLogger(__name__)


def sync_organizations_with_ad() -> None:
    """Вызов функции создания OU и групп"""

    organization_service: OrganizationUnitService = OrganizationUnitService()
    ad_service: ADService = ADService()
    ad_group_service: AdGroupService = AdGroupService()

    organizations = organization_service.get_ou_to_active_directory()

    if not organizations:
        logger.info('Организации не получены с AD')
        return

    for organization in organizations:
        ou_ad = ad_service.create_ou(
            ou_name=organization.name,
            ou_path=organization.ou_path,
        )
        if ou_ad:
            ad_group_service.create_all_group(
                group_name=ou_ad.ou_name,
                group_path=ou_ad.ou_path,
                base_code=organization.base_code,
            )

    logger.info('Организации cинхронизированы с AD')


if __name__ == '__main__':
    configure_logging()
    sync_organizations_with_ad()
