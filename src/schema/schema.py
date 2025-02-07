"""Definition of all model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, UniqueConstraint, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    JSONB,
    SMALLINT,
    VARCHAR,
    DOUBLE_PRECISION,
    TEXT
)
from src.config.db_constants import DBConfig, DBTables

Base = declarative_base()

class UserModel(Base):
    """User Model"""

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
    UniqueConstraint('username', 'email', name="user_auth_unique_key")


class ProductModel(Base):
    """Product Model"""

    __tablename__  = DBTables.PRODUCTS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    name                      = Column(VARCHAR(100), nullable=False)
    description               = Column(VARCHAR(255))
    price                     = Column(DOUBLE_PRECISION, nullable=False)
    stock                     = Column(BIGINT, default=0)
    category_id               = Column(BIGINT, default=0)
    image_urls                = Column(JSONB, default= lambda: {})
    meta_data                 = Column(JSONB, default= lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)


class CategoryModel(Base):
    """Category Model"""

    __tablename__  = DBTables.CATEGORIES
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    name                      = Column(VARCHAR(100), nullable=False, unique=True)
    description               = Column(VARCHAR(255))
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)


class OrderModel(Base):
    """Order Model"""

    __tablename__  = DBTables.ORDERS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    user_id                   = Column(BIGINT, default=0)
    total                     = Column(DOUBLE_PRECISION, nullable=False)
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)


class OrderItemModel(Base):
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


class PaymentModel(Base):
    """Payment Model"""

    __tablename__  = DBTables.PAYMENTS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    order_id                  = Column(BIGINT, default=0)
    payment_method            = Column(BIGINT, nullable=False)
    amount                    = Column(DOUBLE_PRECISION, nullable=False)
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)


class ReviewModel(Base):
    """Review Model"""

    __tablename__  = DBTables.REVIEWS
    __table_args__ = DBConfig.BASE_ARGS

    id                        = Column(BIGINT, primary_key=True)
    product_id                = Column(BIGINT, default=0)
    user_id                   = Column(BIGINT, default=0)
    rating                    = Column(SMALLINT, nullable=False)
    comment                   = Column(TEXT)
    meta_data                 = Column(JSONB, default=lambda: {})
    created_at                = Column(TIMESTAMP)
    updated_at                = Column(TIMESTAMP)
    status                    = Column(SMALLINT, nullable=False, default=1)



# Indexing
Index(DBTables.USER + '_username_key', UserModel.username, unique=False)
Index(DBTables.USER + '_email_key', UserModel.email, unique=False)
Index(DBTables.USER + '_is_admin_key', UserModel.is_admin, unique=False)
Index(DBTables.PRODUCTS + "_name_key", ProductModel.name, unique=False)
Index(DBTables.PRODUCTS + '_category_id_key', ProductModel.category_id, unique=False)
Index(DBTables.CATEGORIES +  '_name_id_key',CategoryModel.name, unique=False)
Index(DBTables.ORDERS + '_user_id_key', OrderModel.user_id, unique=False)
Index(DBTables.ORDER_ITEMS + '_order_id_key', OrderItemModel.order_id, unique=False)
Index(DBTables.ORDER_ITEMS + '_product_id_key', OrderItemModel.product_id, unique=False)
Index(DBTables.PAYMENTS + '_order_id_key', PaymentModel.order_id, unique=False)
Index(DBTables.REVIEWS + '_product_id_key', ReviewModel.product_id, unique=False)
Index(DBTables.REVIEWS + '_user_id_key', ReviewModel.user_id, unique=False)
