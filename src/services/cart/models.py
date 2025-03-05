"""cart model file"""
from src.config.constants import ProductStatusConstant
from src.config.env import get_settings
from src.db.session import get_db, save_new_row, select_all, select_first, delete, update_old_row
from src.services.cart.schema import CartSchema
from datetime import datetime

from src.services.category.schema import CategorySchema
from src.services.product.schema import ProductSchema

db = get_db()
config = get_settings()


class CartModel:
    """cart item table models"""

    @classmethod
    def create(cls, **kw):
        """method to save new item to cart"""
        obj = CartSchema(**kw)
        obj.created_at = datetime.now()
        obj.updated_at = datetime.now()
        save_new_row(obj)
        return obj

    @classmethod
    def patch(cls, _id: int, **kw):
        """method to Update product"""
        obj = db.query(CartSchema).filter(CartSchema.id == _id).first()
        for key, value in kw.items():
            setattr(obj, key, value)
        update_old_row(obj)
        return cls.get(_id=_id)

    @classmethod
    def get(cls, _id: int = None, product_id: int = None, user_id: int = None):
        """method to get all cart items"""
        rows = (db.query(
            CartSchema.id,
            CartSchema.quantity,
            CartSchema.product_id,
            CartSchema.user_id,
            CartSchema.created_at,
            CartSchema.updated_at,
            ProductSchema.id.label("product_id"),
            ProductSchema.name.label("product_name"),
            ProductSchema.description.label("product_description"),
            ProductSchema.price.label("product_price"),
            ProductSchema.stock.label("product_stock"),
            ProductSchema.image_urls.label("product_image"),
            CategorySchema.id.label("category_id"),
            CategorySchema.name.label("category_name"),
            CategorySchema.description.label("category_description"),
        ).join(
            ProductSchema,
            CartSchema.product_id == ProductSchema.id,
        ).join(
            CategorySchema,
            ProductSchema.category_id == CategorySchema.id
        ).filter(
            ProductSchema.status == ProductStatusConstant.Active,
        ))
        if product_id and user_id:
            rows = rows.filter(CartSchema.product_id == product_id, CartSchema.user_id == user_id)
        if _id:
            rows = rows.filter(CartSchema.id == _id)
        if user_id and not product_id:
            rows = rows.filter(CartSchema.user_id == user_id)
        rows = rows.order_by(CartSchema.id.asc())
        if _id:
            rows = select_first(rows)
        else:
            rows = select_all(rows)
        return rows

    @classmethod
    def delete(cls, _id: int, user_id: int):
        """method to delete item from cart"""
        obj = db.query(
            CartSchema
        ).filter(
            CartSchema.id == _id,
            CartSchema.user_id == user_id
        )
        return delete(obj)
