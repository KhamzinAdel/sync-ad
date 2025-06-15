import logging
from datetime import datetime
from typing import Optional

from src.repositories import ADGroupRepository, AbstractADGroupRepository
from src.entities.schemas import ADGroupSchema
from src.utils import OUBuilder
from utils import Base62TimeConverter

logger = logging.getLogger(__name__)


class AdGroupService:
    def __init__(self):
        self.ad_group_repository: AbstractADGroupRepository = ADGroupRepository()

    def _create_access_group(self, group_name: str, group_path: str, base_code: str) -> Optional[ADGroupSchema]:
        """Создание группы доступа."""

        truncate_group_name = OUBuilder.truncate_name(group_name, 58) + '_' + base_code

        group = self.ad_group_repository.create_access_group(
            group_name=truncate_group_name,
            group_path=group_path,
        )

        if not group:
            logger.warning(f'Не удалось создать группу доступа: {group_name}')
            return

        logger.info("Группа доступа '%s' успешно создана.", group.group_name)

        return group

    def _create_mailing_group(self, group_name: str, group_path: str, base_code: str) -> Optional[ADGroupSchema]:
        """Создание группы рассылки."""

        truncate_group_name = OUBuilder.truncate_name(group_name, 57) + '_' + base_code

        group = self.ad_group_repository.create_mailing_group(
            group_name=truncate_group_name,
            group_path=group_path,
        )

        if not group:
            logger.warning('Не удалось создать группу рассылки: %s', group_name)
            return

        logger.info("Группа рассылки '%s' успешно создана.", group.group_name)

        return group

    def _search_parent_groups(self, group_path: str) -> Optional[dict]:
        """Поиск групп родителя."""

        parent_dn = ','.join(group_path.split(',')[1:])
        parent_group = self.ad_group_repository.search_parent_groups(parent_dn)

        if not parent_group:
            return

        result = {
            'parent_access_group': None,
            'parent_mailing_group': None
        }

        for parent_group in parent_group.parent_groups_dn:
            dn = parent_group[0]

            if dn.startswith('CN=_') and result['parent_access_group'] is None:
                result['parent_access_group'] = dn

            elif dn.startswith('CN=') and not dn.startswith('CN=_') and result['parent_mailing_group'] is None:
                result['parent_mailing_group'] = dn

        return result

    def _add_child_group_to_parent_group(self, parent_group_dn: str, child_group_dn: ADGroupSchema) -> None:
        """Добавление группы в группу родителя"""

        if parent_group_dn and child_group_dn:
            self.ad_group_repository.add_child_group_to_parent_group(
                parent_group_dn, child_group_dn.group_dn
            )
            logger.info(
                "Группа %s успешно добавлена в родительскую группу %s",
                child_group_dn.group_name, parent_group_dn
            )

    def create_all_group(self, group_name: str, group_path: str, date_create: datetime) -> None:
        """Основной метод по созданию групп"""

        base_code = Base62TimeConverter.to_base62(date_create)

        group_access = self._create_access_group(group_name, group_path, base_code)

        group_mailing = self._create_mailing_group(group_name, group_path, base_code)

        group_parent_dn = self._search_parent_groups(group_path)

        if group_parent_dn:
            if group_parent_dn['parent_access_group']:
                self._add_child_group_to_parent_group(
                    group_parent_dn['parent_access_group'], group_access
                )

            if group_parent_dn['parent_mailing_group']:
                self._add_child_group_to_parent_group(
                    group_parent_dn['parent_mailing_group'], group_mailing
                )
