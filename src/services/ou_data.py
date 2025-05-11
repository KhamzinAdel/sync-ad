import logging

from repositories import OrganizationUnitDataRepository
from entities.schemas import OrganizationUnitADSchema
from utils import Base62TimeConverter, OUBuilder

logger = logging.getLogger(__name__)


class OrganizationUnitDataService:
    def __init__(self):
        self.organization_unit_data_repository: OrganizationUnitDataRepository = OrganizationUnitDataRepository()

    def get_organizations(self) -> list[OrganizationUnitADSchema]:
        organization_units = self.organization_unit_data_repository.get_organizations()

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
