from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки для подключения к Oracle"""

    ORACLE_PWD: str
    ORACLE_USERNAME: str
    ORACLE_HOST: str
    ORACLE_PORT: int
    ORACLE_SERVICE_NAME: str

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='/Users/khamzin/PycharmProjects/synchronization-ad/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


database_settings = DatabaseSettings()
