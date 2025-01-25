"""Category schema file"""
from sqlalchemy import Column
from src.config.db_constants import DBTables, DBConfig
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, SMALLINT, JSONB, TIMESTAMP

from src.db.session import Base


class CategorySchema(Base):
    """Category Schema"""

    __tablename__  = DBTables.CATEGORIES
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    name                      = Column(VARCHAR(100), nullable=False, unique=True)
    description               = Column(VARCHAR(255))
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)
