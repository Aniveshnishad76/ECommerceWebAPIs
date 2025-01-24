"""Database constants module"""


class DBTables:
    """Database tables class"""
    USER                   = 'user'
    PRODUCTS               = 'products'
    CATEGORIES             = 'categories'
    ORDERS                 = 'orders'
    ORDER_ITEMS            = 'order_items'
    PAYMENTS               = 'payments'
    REVIEWS                = 'reviews'
    CARTS                  = 'carts'


class DBConfig:
    """Database configuration class"""
    SCHEMA_NAME = 'public'
    BASE_ARGS = {"schema": SCHEMA_NAME}