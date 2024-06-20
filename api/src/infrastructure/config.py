from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MODE: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    API_KEY_KADINSKY: str
    API_SECRET_KEY_KADINSKY: str

    AUTH_DATA_SBER: str
    CLIENT_ID_SBER: str
    CLIENT_SECRET_SBER: str

    API_KEY_CHATGPT: str
    BOT_TOKEN: str
    BROKER_URL: str
    # SECRET_KEY: str
    # ALGORITHM: str

    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    # REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def TG_API(self):
        return f"https://api.telegram.org/bot{self.BOT_TOKEN}/"

    @property
    def BROKER_URL(self):
        return self.BROKER_URL

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
