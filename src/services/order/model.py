
"""order model file"""
from datetime import datetime
from typing import List
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.config.constants import OrderStatusConstant
from src.services.order.schema import OrderSchema

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
    def get(cls, _id: int = None, ids: List[int] = None, status: List[int] = None,
            user_id: int = None, page: int = 1, size: int = 10):
        """method to get orders"""
        offset = (page - 1) * size
        rows = db.query(OrderSchema)
        if status:
            rows = rows.filter(OrderSchema.status.in_(status))
        if _id:
            rows = rows.filter(OrderSchema.id == _id)
        if ids:
            rows = rows.filter(OrderSchema.id.in_(ids))
        if user_id:
            rows = rows.filter(OrderSchema.user_id == user_id)
        rows = rows.order_by(OrderSchema.id.desc()).offset(offset).limit(size)
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
