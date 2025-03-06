from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship, Mapped
from src.database import engine

from src.database import Base


class UserComputer(Base):
    __tablename__ = 'users_computers'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связь с филиалами
    branches: Mapped[list['Branch']] = relationship('Branch', back_populates='user_computer')


class Branch(Base):
    __tablename__ = 'branches'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user_computer_id: Mapped[int] = mapped_column(ForeignKey('users_computers.id'))

    # Связь с пользователями и компьютерами
    user_computer: Mapped['UserComputer'] = relationship('UserComputer', back_populates='branches')


def setup_database():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    setup_database()
