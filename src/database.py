from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import database_settings


engine = create_engine(
    f"oracle+oracledb://{database_settings.ORACLE_USERNAME}:{database_settings.ORACLE_PWD}"
    f"@{database_settings.ORACLE_HOST}?service_name={database_settings.ORACLE_SERVICE_NAME}",
    echo=True,
)

Session = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
