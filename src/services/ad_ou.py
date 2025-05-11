import logging
from typing import Optional

from repositories import ADRepository
from entities.schemas import ADSchema
from utils import OUBuilder


logger = logging.getLogger(__name__)


class ADService:
    def __init__(self):
        self.ad_repository: ADRepository = ADRepository()

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

        ou_path_for_group = f'OU={ou_organization.ou_name},{ou_organization.ou_path}'

        return ADSchema(
            ou_name=ou_organization.ou_name,
            ou_path=ou_path_for_group,
        )
