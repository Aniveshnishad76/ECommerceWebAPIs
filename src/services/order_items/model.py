
"""order items model file"""

from datetime import datetime
from typing import List
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.config.constants import OrderStatusConstant
from src.services.order_items.schema import OrderItemSchema

db = get_db()


class OrderItemsModel:
    """class to query order table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new category"""
        obj = OrderItemSchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update order items"""
        obj = db.query(OrderItemSchema).filter(OrderItemSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        obj.updated_at = datetime.now()
        update_old_row(obj)
        return cls.get(_id=_id)

    @classmethod
    def get(cls, _id: int = None, ids: List[int] = None, status: List[int] = None, order_id: int = None):
        """method to get order items"""
        rows = db.query(OrderItemSchema)
        if _id:
            rows = rows.filter(OrderItemSchema.id == _id)
        if ids:
            rows = rows.filter(OrderItemSchema.id.in_(ids))
        if status:
            rows = rows.filter(OrderItemSchema.id.in_(status))
        if order_id:
            rows = rows.filter(OrderItemSchema.order_id == order_id)
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows

    @classmethod
    def delete(cls, _id: int):
        """method to delete"""
        rows = db.query(OrderItemSchema).filter(OrderItemSchema.status == OrderStatusConstant.Placed)
        if _id:
            rows = rows.filter(OrderItemSchema.id == _id)
        return delete(rows)
