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
    db_password: str = os.getenv("DB_PASSWORD", "root")


class BaseConfig(BaseSettings):
    """Base config"""
    env: str = os.getenv("APP_ENV", "local")
    db_app: DBConfig = AppDBConfig()
    redis_port: int = os.getenv("BROKER_PORT", 6379)
    redis_host: str = os.getenv("BROKER_HOST", "localhost")
    redis_db: int = 13
    default_email: str = os.getenv("DEFAULT_EMAIL", "anivesh.nishad@gmail.com")
    jwt_secret: str = os.getenv("JWT_SECRET", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-2")
    aws_s3_bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME", "e-commerce-application")
    sentry_dns: str = os.getenv("SENTRY_DNS", "")
    traces_sample_rate: float = os.getenv("TRACES_SAMPLE_RATE", 1.0)

@lru_cache()
def get_settings():
    """
    get env
    """
    return BaseConfig()
