import logging
from abc import ABC, abstractmethod

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.database import Session
from entities.schemas import OrganizationUnitSchema

logger = logging.getLogger(__name__)


class AbstractOrganizationUnitRepository(ABC):

    @abstractmethod
    def get_ou(self) -> list[OrganizationUnitSchema]:
        """Получает список подразделений"""
        raise NotImplementedError


class OrganizationUnitRepository(AbstractOrganizationUnitRepository):
    """Репозиторий для работы с подразделениями"""

    def get_ou(self) -> list[OrganizationUnitSchema]:
        stmt = text(
            """
            SELECT 
                om.office_id,
                (SELECT MAX(name) 
                 FROM STAFF$DB.OFFICE_GROUP 
                 WHERE id = om.new_group) group_name,
                om.new_name,
                om.p_date_create,
                org.NAME as full_path
            FROM 
                office_mail om
            JOIN 
                STAFF$DB.OFFICE off ON om.office_id = off.cod
            JOIN 
                STAFF$DB.OFFICE_AD oa ON oa.office_id = off.parent_cod
            JOIN 
                STAFF$DB.AD_ORGANIZATIONS org ON oa.AD_GUID = org.ID
            WHERE 
                TO_DATE(om.p_date_create, 'dd.mm.rrrr') >= TO_DATE(SYSDATE-1000, 'dd.mm.rrrr')
            ORDER BY 
                om.office_id
            """
        )
        with Session() as session:
            try:
                results = session.execute(stmt)
                logger.info('Получен список подразделений из базы данных')
                return [
                    OrganizationUnitSchema(
                        id=result.office_id,
                        parent_name=result.group_name.strip() if result.group_name else None,
                        name=result.new_name.strip(),
                        data_create=result.p_date_create if result.p_date_create else None,
                        full_path=result.full_path,
                    )
                    for result in results
                ]
            except SQLAlchemyError as e:
                logger.error('Ошибка при получении списка подразделений: %s', e)
