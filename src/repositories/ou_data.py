import logging
from abc import ABC, abstractmethod

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.database import Session, Session_test
from entities.schemas import OrganizationUnitSchema, ADSchema

logger = logging.getLogger(__name__)


class AbstractOrganizationUnitRepository(ABC):

    @abstractmethod
    def get_organizations(self) -> list[OrganizationUnitSchema]:
        raise NotImplementedError

    @abstractmethod
    def save_ou_path_and_uuid(self, ou_ad: ADSchema) -> None:
        raise NotImplementedError


class OrganizationUnitDataRepository(AbstractOrganizationUnitRepository):
    """Репозиторий для работы с подразделениями"""

    def get_organizations(self) -> list[OrganizationUnitSchema]:
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
                        parent_name=result.group_name,
                        name=result.new_name,
                        data_create=result.p_date_create,
                        full_path=result.full_path,
                    )
                    for result in results
                ]
            except SQLAlchemyError as e:
                logger.error('Ошибка при получении списка подразделений: %s', e)

    def save_ou_path_and_uuid(self, ou_ad: ADSchema) -> None:
        """
        Сохраняет UUID и путь подразделения в таблицу AD_ORGANIZATIONS
        """

        stmt = text("""
            INSERT INTO AD_ORGANIZATIONS (UUID, OU_PATH) 
            VALUES (:uuid, :path)
        """)

        with Session_test() as session:
            try:
                session.execute(
                    stmt,
                    {
                        'uuid': ou_ad.ou_uuid,
                        'path': ou_ad.ou_path
                    }
                )
                session.commit()
                logger.info('Сохранено в AD_ORGANIZATIONS: %s - %s', ou_ad.ou_uuid, ou_ad.ou_path)

            except SQLAlchemyError as e:
                logger.error('Ошибка сохранения в AD_ORGANIZATIONS: %s', e)
