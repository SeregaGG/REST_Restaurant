from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    PORT: int
    HOST: str


class DBSettings(BaseSettings):
    class Config:
        env_file = ".db_env"
        env_file_encoding = "utf-8"

    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
