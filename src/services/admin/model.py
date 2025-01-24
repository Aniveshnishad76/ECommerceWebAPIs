"""admin model file"""
from typing import List

from src.config.env import get_settings
from src.db.session import get_db, save_new_row, update_old_row, select_all, select_first
from src.services.admin.schema import CategorySchema, ProductSchema
from src.config.constants import CategoriesStatusConstant

db = get_db()
config = get_settings()


class CategoryModel:
    """class to query category table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new category"""
        obj = CategorySchema(**kw)
        save_new_row(obj)
        return obj

    # @classmethod
    # def patch(cls, _id: int, **kw):
    #     """method to Update Category"""
    #     obj = db.query(UserSchema).filter(UserSchema.id == _id).first()
    #     for key, value in kw.items():
    #         setattr(obj, key, value)
    #     update_old_row(obj)
    #     return cls.get_user(_id=_id)

    @classmethod
    def get_category(cls, _id: int = None, ids: List[int] = None):
        """get category by id"""
        rows = db.query(CategorySchema).filter(CategorySchema.status == CategoriesStatusConstant.Active)
        if _id:
            rows = rows.filter(CategorySchema.id == _id)
        if ids:
            rows = rows.filter(CategorySchema.id.in_(ids))
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows
    

    # @classmethod
    # def get_user(cls, _id: int = None, email: str = None, ids: List[int] = None, password: str = None, is_admin: bool = False):
    #     """get user by id"""
    #     rows = db.query(UserSchema).filter(UserSchema.status == UserStatusConstant.Active)
    #     if _id:
    #         rows = rows.filter(UserSchema.id == _id)
    #     if email:
    #         rows = rows.filter(UserSchema.email == email)
    #     if ids:
    #         rows = rows.filter(UserSchema.id.in_(ids))
    #     if password:
    #         rows = rows.filter(UserSchema.password_hash == password)
    #     if is_admin:
    #         rows = rows.filter(UserSchema.is_admin == is_admin)
    #     if not _id and not email:
    #         rows = select_all(rows)
    #     else:
    #         rows = select_first(rows)
    #     return rows


class ProductModel:
    """class to query product table schema"""

    @classmethod
    def create(cls, **kw):
        """method to save new produvt"""
        obj = ProductSchema(**kw)
        save_new_row(obj)
        return obj
    

    @classmethod
    def get_product(cls, _id: int = None, ids: List[int] = None):
        """get product by id"""
        rows = db.query(ProductSchema).filter(CategorySchema.status == CategoriesStatusConstant.Active)
        if _id:
            rows = rows.filter(ProductSchema.id == _id)
        if ids:
            rows = rows.filter(ProductSchema.id.in_(ids))
        if not _id:
            rows = select_all(rows)
        else:
            rows = select_first(rows)
        return rows
    