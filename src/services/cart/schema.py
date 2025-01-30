"""User Schema"""
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BIGINT, SMALLINT, JSONB, TIMESTAMP
from src.config.db_constants import DBConfig, DBTables
from src.db.session import Base

class CartSchema(Base):
    """Add/Remove from CartModel"""

    __tablename__  = DBTables.CARTS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    product_id                = Column(BIGINT, default=0)
    user_id                   = Column(BIGINT, default=0)
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
