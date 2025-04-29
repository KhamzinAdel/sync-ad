import logging

from repositories import OrganizationUnitRepository
from entities.schemas import OrganizationUnitADSchema
from .name_modification import Base36TimeConverter, OUBuilder

logger = logging.getLogger(__name__)


class OrganizationUnitService:
    def __init__(self):
        self.organization_unit_repository: OrganizationUnitRepository = OrganizationUnitRepository()

    def get_ou_to_active_directory(self) -> list[OrganizationUnitADSchema]:
        organization_units = self.organization_unit_repository.get_ou()

        if organization_units:
            return [
                OrganizationUnitADSchema(
                    name=ou.name,
                    base_code=Base36TimeConverter.to_base_36(ou.data_create),
                    ou_path=OUBuilder.build_ou_path(ou.full_path, ou.parent_name),
                ) for ou in organization_units
            ]
