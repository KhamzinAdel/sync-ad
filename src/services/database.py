from sqlalchemy import select

from src.database import async_session_maker
from src.models import UserComputer, Branch


class UserComputerService:

    @classmethod
    async def get_user_computer_by_id(cls, user_computer_by_id: int) -> UserComputer:
        """
        Получаем объект пользователя и компьютера по id
        """
        async with async_session_maker() as session:
            query = select(UserComputer.title).where(UserComputer.id == user_computer_by_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record


class BranchService:

    @classmethod
    async def get_branches(cls, user_computer_by_id: int) -> UserComputer:
        """
        Получаем все филиалы по id OU
        """
        async with async_session_maker() as session:
            query = select(Branch.title).where(Branch.user_computer_id == user_computer_by_id)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
