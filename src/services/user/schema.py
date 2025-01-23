"""User Schema"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, SMALLINT, JSONB, BOOLEAN, TIMESTAMP
from src.config.db_constants import DBConfig, DBTables
from src.db.session import Base


class UserSchema(Base):
    """User Schema"""

    __tablename__  = DBTables.USER
    __table_args__ = DBConfig.BASE_ARGS

    id                       = Column(BIGINT, primary_key=True)
    username                 = Column(VARCHAR(50), nullable=False, unique=True)
    email                    = Column(VARCHAR(100), nullable=False, unique=True)
    password_hash            = Column(VARCHAR(255), nullable=False)
    full_name                = Column(VARCHAR(100))
    phone_number             = Column(VARCHAR(20))
    address                  = Column(VARCHAR(255))
    is_admin                 = Column(BOOLEAN, default=False)
    status                   = Column(SMALLINT, nullable=False, default=1)
    meta_data                = Column(JSONB, default= lambda: {})
    created_on               = Column(TIMESTAMP)
    updated_on               = Column(TIMESTAMP)
