from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class DatabaseSettings(BaseModel):
    """Настройки для подключения к Oracle"""

    ORACLE_PWD: str
    ORACLE_USERNAME: str
    ORACLE_HOST: str
    ORACLE_PORT: int
    ORACLE_SERVICE_NAME: str


class LdapSettings(BaseModel):
    """Настройки для подключения к LDAP"""

    BASE_DN: str
    LDAP_SERVER: str
    LDAP_USER: str
    LDAP_PASSWORD: str


class Settings(BaseSettings):
    """Общие настройки"""

    database: DatabaseSettings
    ldap: LdapSettings

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_prefix='APP_',
        env_nested_delimiter='__',
    )


settings = Settings()
