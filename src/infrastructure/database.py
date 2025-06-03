from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings


engine = create_engine(
    f"oracle+oracledb://{settings.database.ORACLE_USERNAME}:{settings.database.ORACLE_PWD}"
    f"@{settings.database.ORACLE_HOST}:{settings.database.ORACLE_PORT}/{settings.database.ORACLE_SERVICE_NAME}",
)

engine_test = create_engine(
    "oracle+oracledb://system:<password>@localhost:1521/FREE"
)

Session = sessionmaker(bind=engine, expire_on_commit=False)
Session_test = sessionmaker(bind=engine_test, expire_on_commit=False)
