
"""order model file"""
from datetime import datetime
from typing import List
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.config.constants import OrderStatusConstant
from src.services.order.schema import OrderSchema
from src.services.order_items.model import OrderItemsModel

db = get_db()


class OrderModel:
    """class to query order table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new category"""
        obj = OrderSchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update order"""
        obj = db.query(OrderSchema).filter(OrderSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        obj.updated_at = datetime.now()
        update_old_row(obj)
        return cls.get(_id=_id)

    @classmethod
    def get(cls, _id: int = None, ids: List[int] = None):
        """method to get orders"""
        rows = db.query(OrderSchema).filter(OrderSchema.status == OrderStatusConstant.Placed)
        if _id:
            rows = rows.filter(OrderSchema.id == _id)
        if ids:
            rows = rows.filter(OrderSchema.id.in_(ids))
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows

    @classmethod
    def delete(cls, _id: int):
        """method to delete category by id"""
        rows = db.query(OrderSchema).filter(OrderSchema.status == OrderStatusConstant.Placed)
        if _id:
            rows = rows.filter(OrderSchema.id == _id)
        return delete(rows)
