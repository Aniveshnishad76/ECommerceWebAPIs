"""User Schema"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, SMALLINT, JSONB
from src.config.db_constants import DBConfig, DBTables
from src.db.session import Base


class UserSchema(Base):
    """User model schema for performing CRUD operations"""

    __tablename__  = DBTables.USER
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    name                      = Column(VARCHAR(250), nullable=False)
    email                     = Column(VARCHAR(100), nullable=False)
    mobile_number             = Column(VARCHAR(100))
    status                    = Column(SMALLINT, nullable=False, default=1)
    meta_data                 = Column(JSONB, default=lambda: {})