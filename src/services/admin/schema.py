"""User Schema"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, SMALLINT, JSONB, BOOLEAN, TIMESTAMP,DOUBLE_PRECISION
from src.config.db_constants import DBConfig, DBTables
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


class ProductSchema(Base):
    """Product Schema"""

    __tablename__  = DBTables.PRODUCTS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    name                      = Column(VARCHAR(100), nullable=False)
    description               = Column(VARCHAR(255))
    price                     = Column(DOUBLE_PRECISION, nullable=False)
    stock                     = Column(BIGINT, default=0)
    category_id               = Column(BIGINT, default=0)
    meta_data                 = Column(JSONB, default= lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)