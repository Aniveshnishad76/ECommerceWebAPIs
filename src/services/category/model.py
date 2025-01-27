"""admin model file"""
from datetime import datetime
from typing import List
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first, delete
from src.config.constants import CategoriesStatusConstant
from src.services.category.schema import CategorySchema

db = get_db()


class CategoryModel:
    """class to query category table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new category"""
        obj = CategorySchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update Category"""
        obj = db.query(CategorySchema).filter(CategorySchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        obj.updated_at = datetime.now()
        update_old_row(obj)
        return cls.get(_id=_id)

    @classmethod
    def get(cls, _id: int = None, ids: List[int] = None, name: str = None, page: int = 1, size: int = 10):
        """method to get category by id"""
        offset = (page - 1) * size
        rows = db.query(CategorySchema).filter(CategorySchema.status == CategoriesStatusConstant.Active)
        if _id:
            rows = rows.filter(CategorySchema.id == _id)
        if ids:
            rows = rows.filter(CategorySchema.id.in_(ids))
        if name:
            rows = rows.filter(CategorySchema.name == name)
        rows = rows.offset(offset).limit(size)
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows

    @classmethod
    def delete(cls, _id: int):
        """method to delete category by id"""
        rows = db.query(CategorySchema).filter(CategorySchema.status == CategoriesStatusConstant.Active)
        if _id:
            rows = rows.filter(CategorySchema.id == _id)
        return delete(rows)
