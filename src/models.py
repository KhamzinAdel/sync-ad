from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.database import Base, engine


# Модель "Пользователи и компьютеры"
class UserComputer(Base):
    __tablename__ = 'users_computers'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связь с филиалами
    branches: Mapped[list['Branch']] = relationship('Branch', back_populates='user_computer')


# Модель "Филиалы"
class Branch(Base):
    __tablename__ = 'branches'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user_computer_id: Mapped[int] = mapped_column(ForeignKey('users_computers.id'))

    # Связь с пользователями и компьютерами
    user_computer: Mapped['UserComputer'] = relationship('UserComputer', back_populates='branches')


#async def setup_database():
#    async with engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)

#if __name__ == '__main__':
#    import asyncio

#    asyncio.run(setup_database())
