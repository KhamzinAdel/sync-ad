from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import settings


engine = create_engine(
    f"oracle+oracledb://{settings.database.ORACLE_USERNAME}:{settings.database.ORACLE_PWD}"
    f"@{settings.database.ORACLE_HOST}?service_name={settings.database.ORACLE_SERVICE_NAME}",
    echo=True,
)

Session = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
