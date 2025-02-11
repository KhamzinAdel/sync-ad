from pydantic_settings import BaseSettings, SettingsConfigDict


class LdapSettings(BaseSettings):
    """Настройки для подключения к LDAP"""

    BASE_DN: str
    LDAP_SERVER: str
    LDAP_USER: str
    LDAP_PASSWORD: str

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='/Users/khamzin/PycharmProjects/synchronization-ad/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


ldap_settings = LdapSettings()
