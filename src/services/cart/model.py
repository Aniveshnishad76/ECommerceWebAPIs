"""user model file"""
from typing import List

from src.config.constants import UserStatusConstant
from src.config.env import get_settings
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.services.cart.schema import CartSchema
from datetime import datetime

db = get_db()
config = get_settings()


class CartModel:
    """class to query cart item table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new item to cart"""

        obj = CartSchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def read_items(cls, _id: int = None, product_id: int = None, user_id: int = None, page: int = 1, size: int = 10):
        """method to get all cart items"""
        if product_id and user_id:
            rows = db.query(CartSchema).filter(CartSchema.product_id == product_id, CartSchema.user_id == user_id)
        if _id:
            rows = db.query(CartSchema).filter(CartSchema.id == _id)
        if user_id and not product_id:
            rows = db.query(CartSchema).filter(CartSchema.user_id == user_id)
        if _id:
            rows = select_first(rows)
        else:
            rows = select_all(rows)
        return rows

    @classmethod
    def delete_item(cls, _id: int):
        """method to delete item from cart"""

        obj = db.query(CartSchema).filter(CartSchema.id == _id)
        return delete(obj)
