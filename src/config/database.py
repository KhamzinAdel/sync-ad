from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки для подключения к Oracle."""

    ORACLE_PWD: str
    ORACLE_USERNAME: str
    ORACLE_HOST: str
    ORACLE_PORT: int
    ORACLE_SERVICE_NAME: str

    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')
