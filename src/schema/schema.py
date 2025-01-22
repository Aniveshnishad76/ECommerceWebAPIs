"""Definition of all model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    JSONB,
    SMALLINT,
    VARCHAR,
)
from src.config.db_constants import DBConfig, DBTables

Base = declarative_base()

class UserModel(Base):
    """User Model"""

    __tablename__  = DBTables.USER
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    first_name                = Column(VARCHAR(100), nullable=False)
    last_name                 = Column(VARCHAR(100), nullable=False)
    email                     = Column(VARCHAR(100), nullable=False)
    mobile_number             = Column(VARCHAR(100))
    status                    = Column(SMALLINT, nullable=False, default=1)
    meta_data                 = Column(JSONB, default=lambda: {})
    UniqueConstraint(email, name="user_auth_email_key")
