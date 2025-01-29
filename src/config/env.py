"""file to contain the env specific configs"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class DBConfig:
    """
    db config
    """
    db_name: str
    db_host: str
    db_username: str
    db_password: str


class AppDBConfig(DBConfig):
    """
    App Db config
    """

    db_host: str = os.getenv("DB_HOST", "localhost:5432")
    db_name: str = os.getenv("DB_NAME", "app-web")
    db_username: str = os.getenv("DB_USERNAME", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "admin")


class BaseConfig(BaseSettings):
    """Base config"""
    env: str = os.getenv("APP_ENV", "")
    db_app: DBConfig = AppDBConfig()
    redis_port: int = os.getenv("BROKER_PORT", 6379)
    redis_host: str = os.getenv("BROKER_HOST", "localhost")
    redis_db: int = 13
    default_email: str = os.getenv("DEFAULT_EMAIL", "anivesh.nishad@gmail.com")
    jwt_secret: str = os.getenv("JWT_SECRET", "5cbd8f1a156a0551a3fa035b978c7ff142fd945576f0436df17408b5d470a0d8")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")


@lru_cache()
def get_settings():
    """
    get env
    """
    return BaseConfig()
