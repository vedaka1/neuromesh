import os
from typing import Any


def get_env_var(key: str, to_cast: Any, default: Any | None = None) -> Any:
    """
    Converting environment variable types
    Args:
        key (str): environment variable
        to_cast (Any): type to convert
        default (Any, optional): default value
    Raises:
        RuntimeError: occurs if such a variable is not found in .env
    Returns:
        Any: an environment variable with a converted type
    """
    value = os.getenv(key)

    if not value and not default:
        raise RuntimeError(f"{key} environment variable not set")
    if not value:
        return default
    return to_cast(value)


class DatabaseSettings:
    POSTGRES_HOST: str = get_env_var("POSTGRES_HOST", to_cast=str, default="postgres")
    POSTGRES_PORT: int = get_env_var("POSTGRES_PORT", to_cast=int, default=5432)
    POSTGRES_USER: str = get_env_var("POSTGRES_USER", to_cast=str)
    POSTGRES_PASSWORD: str = get_env_var("POSTGRES_PASSWORD", to_cast=str)
    POSTGRES_DB: str = get_env_var("POSTGRES_DB", to_cast=str)

    @property
    def DB_URL(self) -> str:
        return "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )


class SberSettings:
    API_KEY_KADINSKY: str = get_env_var("API_KEY_KADINSKY", to_cast=str)
    API_SECRET_KEY_KADINSKY: str = get_env_var("API_SECRET_KEY_KADINSKY", to_cast=str)
    AUTH_DATA_SBER: str = get_env_var("AUTH_DATA_SBER", to_cast=str)
    CLIENT_ID_SBER: str = get_env_var("CLIENT_ID_SBER", to_cast=str)
    CLIENT_SECRET_SBER: str = get_env_var("CLIENT_SECRET_SBER", to_cast=str)


class TelegramSettings:
    BOT_TOKEN: str = get_env_var("BOT_TOKEN", to_cast=str)

    @property
    def TG_API(self):
        return f"https://api.telegram.org/bot{self.BOT_TOKEN}/"


class ChatGPTSettings:
    API_KEY_CHATGPT: str = get_env_var("API_KEY_CHATGPT", to_cast=str)


class Settings:
    db: DatabaseSettings = DatabaseSettings()
    sber: SberSettings = SberSettings()
    tg: TelegramSettings = TelegramSettings()
    chatgpt: ChatGPTSettings = ChatGPTSettings()

    BROKER_URL_ENV: str = get_env_var("BROKER_URL", to_cast=str)
    API_KEY_GEMINI: str = get_env_var("API_KEY_GEMINI", to_cast=str)

    @property
    def BROKER_URL(self):
        return self.BROKER_URL_ENV


settings = Settings()
