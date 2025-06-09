import logging
from typing import Optional
from abc import ABC, abstractmethod

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from infrastructure.database import Session
from entities.schemas import ADSchema, OrganizationUnitListSchema, OrganizationUnitSchema

logger = logging.getLogger(__name__)


class AbstractOrganizationUnitRepository(ABC):
    """Интерфейс для работы с подразделениями"""

    @abstractmethod
    def get_organizations(self) -> list[OrganizationUnitListSchema]:
        raise NotImplementedError

    @abstractmethod
    def create_organization(self, ou_ad: ADSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_organization(self, ou_ad: ADSchema) -> OrganizationUnitSchema:
        raise NotImplementedError

    @abstractmethod
    def get_organization(self, ou_uuid: str) -> OrganizationUnitSchema:
        raise NotImplementedError


class OrganizationUnitDataRepository(AbstractOrganizationUnitRepository):
    """Репозиторий для работы с подразделениями"""

    def get_organizations(self) -> list[OrganizationUnitListSchema]:
        """Получение всех подразделений за конкретные дни"""

        days_threshold = int(settings.database.DAYS_THRESHOLD)

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
                TO_DATE(om.p_date_create, 'dd.mm.rrrr') >= TO_DATE(SYSDATE-:days_threshold, 'dd.mm.rrrr')
            ORDER BY 
                om.office_id
            """
        )
        with Session() as session:
            try:
                results = session.execute(
                    stmt,
                    {
                        'days_threshold': days_threshold,
                    }
                )
                logger.info('Получен список подразделений из базы данных')
                return [
                    OrganizationUnitListSchema(
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

    def create_organization(self, ou_ad: ADSchema) -> None:
        """
        Сохраняет UUID и путь подразделения в таблицу AD_ORGANIZATIONS
        """

        stmt = text("""
            INSERT INTO STAFF$DB.AD_ORGANIZATIONS (ID, NAME)
            VALUES (:id, :name)
        """)

        with Session() as session:
            try:
                session.execute(
                    stmt,
                    {
                        'id': str(ou_ad.ou_uuid),
                        'name': ou_ad.ou_path,
                    }
                )
                session.commit()
                logger.info('Сохранено в AD_ORGANIZATIONS: %s - %s', ou_ad.ou_uuid, ou_ad.ou_path)

            except SQLAlchemyError as e:
                session.rollback()
                logger.error('Ошибка сохранения в AD_ORGANIZATIONS: %s', e)

    def update_organization(self, ou_ad: ADSchema) -> None:
        """Обновляет существующее подразделение"""

        stmt = text("""
            UPDATE STAFF$DB.AD_ORGANIZATIONS
            SET NAME = :name
            WHERE ID = :id
        """)

        with Session() as session:
            try:
                session.execute(
                    stmt,
                    {
                        'id': str(ou_ad.ou_uuid),
                        'name': ou_ad.ou_path,
                    }
                )
                session.commit()
                logger.info(f"Обновлено подразделение: {ou_ad.ou_uuid}")
            except SQLAlchemyError as e:
                session.rollback()
                logger.error(f"Ошибка обновления подразделения {ou_ad.ou_uuid}: {e}")

    def get_organization(self, ou_uuid: str) -> Optional[OrganizationUnitSchema]:
        """Получает подразделение по UUID"""

        query = text("""
            SELECT ID, NAME
            FROM STAFF$DB.AD_ORGANIZATIONS
            WHERE ID = :id
        """)

        with Session() as session:
            try:
                result = session.execute(
                    query,
                    {
                        'id': str(ou_uuid),
                    }
                ).fetchone()

                if result:
                    return OrganizationUnitSchema(
                        ou_uuid=result.ID,
                    )
                return None
            except SQLAlchemyError as e:
                logger.error(f"Ошибка получения подразделения {ou_uuid}: {e}")
