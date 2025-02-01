from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import database_settings as settings


engine = create_async_engine(
    f"oracle+oracledb_async://{settings.ORACLE_USERNAME}:"
    f"{settings.ORACLE_PWD}@{settings.ORACLE_HOST}"
    f"?service_name={settings.ORACLE_SERVICE_NAME}",
    echo=True,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
