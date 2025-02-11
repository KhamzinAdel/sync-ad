from sqlalchemy import select

from src.database import Session
from src.models import UserComputer, Branch


class DataRepository:

    def get_user_computer_by_id(self, user_computer_by_id: int) -> UserComputer:
        """
        Получаем объект пользователя и компьютера по id
        """
        with Session() as session:
            query = select(UserComputer.title).where(UserComputer.id == user_computer_by_id)
            result = session.execute(query)
            record = result.scalar_one_or_none()
            return record

    def get_branches(self, user_computer_by_id: int) -> UserComputer:
        """
        Получаем все филиалы по id OU
        """
        with Session() as session:
            query = select(Branch.title).where(Branch.user_computer_id == user_computer_by_id)
            result = session.execute(query)
            records = result.scalars().all()
            return records
