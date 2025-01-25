"""Product model file """
from datetime import datetime
from typing import List
from src.config.constants import ProductStatusConstant
from src.db.session import save_new_row, get_db, select_all, select_first, delete, update_old_row
from src.services.product.schema import ProductSchema

db = get_db()

class ProductModel:
    """class to query product table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new produvt"""
        obj = ProductSchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update product"""
        obj = db.query(ProductSchema).filter(ProductSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get(_id=_id)

    @classmethod
    def get(cls, _id: int = None, ids: List[int] = None):
        """get product by id"""
        rows = db.query(ProductSchema).filter(ProductSchema.status == ProductStatusConstant.Active)
        if _id:
            rows = rows.filter(ProductSchema.id == _id)
        if ids:
            rows = rows.filter(ProductSchema.id.in_(ids))
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows

    @classmethod
    def delete(cls, _id: int):
        """method to delete category by id"""
        rows = db.query(ProductSchema).filter(ProductSchema.status == ProductStatusConstant.Active)
        if _id:
            rows = rows.filter(ProductSchema.id == _id)
        return delete(rows)
