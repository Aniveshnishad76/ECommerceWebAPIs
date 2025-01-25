"""order schema file"""
from src.config.db_constants import DBTables, DBConfig
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    JSONB,
    SMALLINT,
    DOUBLE_PRECISION
)
from src.db.session import Base


class OrderItemSchema(Base):

    """Order Item Model"""

    __tablename__  = DBTables.ORDER_ITEMS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    order_id                  = Column(BIGINT, default=0)
    product_id                = Column(BIGINT, default=0)
    quantity                  = Column(SMALLINT, nullable=False)
    price                     = Column(DOUBLE_PRECISION, nullable=False)
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)

