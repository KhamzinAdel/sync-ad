from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings


engine = create_engine(
    f"oracle+oracledb://{settings.database.ORACLE_USERNAME}:{settings.database.ORACLE_PWD}"
    f"@{settings.database.ORACLE_HOST}:{settings.database.ORACLE_PORT}/{settings.database.ORACLE_SERVICE_NAME}",
)

Session = sessionmaker(bind=engine, expire_on_commit=False)
