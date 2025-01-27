"""Product model file """
from datetime import datetime
from typing import List
from src.config.constants import ProductStatusConstant, CategoriesStatusConstant
from src.db.session import save_new_row, get_db, select_all, select_first, delete, update_old_row
from src.services.category.schema import CategorySchema
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
    def get(cls, _id: int = None, ids: List[int] = None, category_id: int = None, page: int = 1, size: int = 10):
        """get product by id"""
        offset = (page - 1) * size
        rows = db.query(
            ProductSchema.id,
            ProductSchema.name,
            ProductSchema.description,
            ProductSchema.price,
            ProductSchema.stock,
            ProductSchema.status,
            ProductSchema.updated_at,
            ProductSchema.created_at,
            CategorySchema.id.label("category_id"),
            CategorySchema.name.label("category_name"),
            CategorySchema.status.label("category_status"),
            CategorySchema.description.label("category_description"),
            CategorySchema.created_at.label("category_created_at"),
            CategorySchema.updated_at.label("category_updated_at"),
        ).join(
            CategorySchema,
            ProductSchema.category_id == CategorySchema.id,
        ).filter(
            ProductSchema.status == ProductStatusConstant.Active,
            CategorySchema.status == CategoriesStatusConstant.Active,
        )
        if _id:
            rows = rows.filter(ProductSchema.id == _id)
        if ids:
            rows = rows.filter(ProductSchema.id.in_(ids))
        if category_id:
            rows = rows.filter(ProductSchema.category_id == category_id)
        rows = rows.offset(offset).limit(size)
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
