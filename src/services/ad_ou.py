import logging
import uuid
from typing import Optional

from repositories import AbstractADRepository, ADRepository
from entities.schemas import ADSchema
from utils import OUBuilder


logger = logging.getLogger(__name__)


class ADService:
    def __init__(self):
        self.ad_repository: AbstractADRepository = ADRepository()

    def get_ou_guid_by_dn(self, ou_dn: str) -> Optional[uuid.UUID]:
        """Получает GUID организационной единицы по её DN"""

        result = self.ad_repository.get_ou_guid_by_dn(ou_dn)

        if not result:
            logger.error("Не удалось получить GUID для OU: %s", ou_dn)
            return

        return uuid.UUID(bytes_le=result.guid)

    def create_ou(self, ou_name: str, ou_path: str) -> Optional[ADSchema]:
        update_ou_name = OUBuilder.truncate_name(ou_name, 64)

        ou_organization = self.ad_repository.create_ou(
            ou_name=update_ou_name,
            ou_path=ou_path,
        )

        if not ou_organization:
            logger.error('Не удалось создать организационную единицу: %s', ou_name)
            return

        logger.info("Организационная единица '%s' (путь: '%s') успешно создана.",
                    ou_organization.ou_name, ou_path)

        full_ou_path = f'OU={ou_organization.ou_name},{ou_organization.ou_path}'

        ou_uuid = self.get_ou_guid_by_dn(full_ou_path)

        return ADSchema(
            ou_name=ou_organization.ou_name,
            ou_path=full_ou_path,
            ou_uuid=ou_uuid,
        )
