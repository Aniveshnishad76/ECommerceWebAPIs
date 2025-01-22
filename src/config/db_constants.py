"""Database constants module"""


class DBTables:
    """Database tables class"""
    USER                   = "user"
    ADMIN                  = "admin"


class DBConfig:
    """Database configuration class"""
    SCHEMA_NAME = "ecommerce"
    BASE_ARGS = {"schema": SCHEMA_NAME}