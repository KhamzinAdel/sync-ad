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
        sql = text("""
                SELECT 
                    office_id, 
                    (SELECT MAX(to_char(datestart,'dd.mm.rrrr')) 
                     FROM office 
                     WHERE cod=office_mail.office_id) start_date, 
                    (SELECT MAX(name) 
                     FROM STAFF$DB.OFFICE_GROUP 
                     WHERE id = office_mail.new_group) group_name, 
                    office_mail.new_name,
                    office_mail.p_date_create,
                    get_full_officename(office_mail.office_id) full_name 
                FROM office_mail 
                WHERE to_date(office_mail.p_date_create,'dd.mm.rrrr') >= to_date(sysdate-90,'dd.mm.rrrr')
                """)

        with Session() as session:
            try:
                results = session.execute(sql)
                logger.info('Получен список подразделений из базы данных')
                return [
                    OrganizationUnitSchema(
                        id=result.office_id,
                        parent_name=result.group_name.strip() if result.group_name else None,
                        name=result.new_name,
                        data_create=result.p_date_create if result.p_date_create else None,
                        full_name=result.full_name,
                    )
                    for result in results
                ]
            except SQLAlchemyError as e:
                logger.error('Ошибка при получении списка подразделений: %s', e)


def main():
    repository = OrganizationUnitRepository()

    logging.info("Получаем список подразделений...")
    print(repository.get_ou())

    logging.info("Запрос выполнен успешно")



if __name__ == "__main__":
    main()