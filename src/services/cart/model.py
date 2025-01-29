"""user model file"""
from typing import List

from src.config.constants import UserStatusConstant
from src.config.env import get_settings
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.services.cart.schema import CartSchema

db = get_db()
config = get_settings()


class CartModel:
    """class to query cart item table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new item to cart"""

        obj = CartSchema(**kw)
        save_new_row(obj)
        return obj

    @classmethod
    def read_items(cls, _id: int = None, user_id: int = None, page: int = 1, size: int = 10):
        """method to get all cart items"""
        rows = db.query(UserSchema).filter(UserSchema.status == UserStatusConstant.Active)
        if _id:
            rows = db.query(CartSchema).filter(id == _id)
        if user_id:
            rows = db.query(CartSchema).filter(CartSchema.user_id == user_id)
        else:
            rows = db.query(CartSchema)
            rows = select_all(rows)
        return rows

    @classmethod
    def delete_item(cls, _id: int = None):
        """method to delete item from cart"""

        obj = db.query(CartSchema).filter(CartSchema.id == _id).first()
        delete(obj)
        return obj
