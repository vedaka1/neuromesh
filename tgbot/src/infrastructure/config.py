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
        raise RuntimeError(f'{key} environment variable not set')
    if not value:
        return default
    return to_cast(value)


class TelegramConfig:
    BOT_TOKEN: str = get_env_var(key='BOT_TOKEN', to_cast=str)
    HEAD_ADMIN_TG_ID: int = get_env_var(key='HEAD_ADMIN_TG_ID', to_cast=int)


class AppConfig:
    telegram: TelegramConfig = TelegramConfig()


config = AppConfig()
