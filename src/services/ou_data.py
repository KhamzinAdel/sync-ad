import logging

from repositories import AbstractOrganizationUnitRepository, OrganizationUnitDataRepository
from entities.schemas import OrganizationUnitADSchema, ADSchema
from utils import Base62TimeConverter, OUBuilder

logger = logging.getLogger(__name__)


class OrganizationUnitDataService:
    def __init__(self):
        self.organization_unit_repository: AbstractOrganizationUnitRepository = OrganizationUnitDataRepository()

    def get_organizations(self) -> list[OrganizationUnitADSchema]:
        """"Получаем все подразделения"""

        organization_units = self.organization_unit_repository.get_organizations()

        if organization_units:
            return [
                OrganizationUnitADSchema(
                    name=ou.name.strip(),
                    base_code=Base62TimeConverter.to_base62(ou.data_create),
                    ou_path=OUBuilder.build_ou_path(
                        ou.full_path,
                        ou.parent_name.strip(),
                    ),
                ) for ou in organization_units
            ]

    def save_ou_path_and_uuid(self, ou_ad: ADSchema) -> None:
        """Сохраняет UUID и путь подразделения в таблицу AD_ORGANIZATIONS"""

        if ou_ad.ou_uuid and ou_ad.ou_path:
            self.organization_unit_repository.save_ou_path_and_uuid(ou_ad)
