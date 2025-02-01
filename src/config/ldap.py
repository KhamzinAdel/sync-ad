from pydantic_settings import BaseSettings, SettingsConfigDict


class LdapSettings(BaseSettings):
    """Настройки для подключения к LDAP"""

    BASE_DN: str
    LDAP_SERVER: str
    LDAP_USER: str
    LDAP_PASSWORD: str

    model_config = SettingsConfigDict(env_file='../../.env', extra='ignore')
