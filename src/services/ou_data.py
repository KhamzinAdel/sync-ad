import logging

from src.repositories import AbstractOrganizationUnitRepository, OrganizationUnitDataRepository
from src.entities.schemas import OrganizationUnitADSchema, ADSchema
from src.utils import Base62TimeConverter, OUBuilder

logger = logging.getLogger(__name__)


class OrganizationUnitDataService:
    def __init__(self):
        self.organization_unit_repository: AbstractOrganizationUnitRepository = OrganizationUnitDataRepository()

    def get_organizations(self) -> list[OrganizationUnitADSchema]:
        """Получение всех подразделений за конкретные дни"""

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

    def create_or_update_organization(self, ou_ad: ADSchema) -> None:
        """Создание или обновление подразделения"""

        if ou_ad.ou_uuid and ou_ad.ou_path:
            existing = self.organization_unit_repository.get_organization(ou_uuid=ou_ad.ou_uuid)
            if existing:
                self.organization_unit_repository.update_organization(ou_ad=ou_ad)
            else:
                self.organization_unit_repository.create_organization(ou_ad=ou_ad)
