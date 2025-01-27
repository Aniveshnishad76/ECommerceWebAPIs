"""user controller file"""
from src.config.error_constants import ErrorMessage
from src.exceptions.errors.generic import EntityException
from src.services.cart.model import CartModel
from src.services.user.model import UserModel
from src.services.cart.serializer import (
    CartInBound,
    CartOutBound,
    CartMultiFinalOutBound,

)


class CartController:
    """user controller class"""

    @classmethod
    async def add_to_cart(cls, payload: CartInBound):
        """Add to Cart function"""

        user = UserModel.get_user(id=payload.user_id)
        if not user:
            raise EntityException(message=ErrorMessage.INVALID_USER)
        
        product = ProductModel.get_product(_id=payload.product_id)
        if not product:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("product"))
        
        cart = CartModel.create(**payload.__dict__)
        return CartOutBound(id=cart.id, user_id=user.id, product=product.__dict__)

    @classmethod
    async def read_all_items(cls):
        """read all items from the cart"""
        cart_items = CartModel.read_items()
        response = []
        for cart_item in cart_items:
            product = ProductModel.get_product(_id=cart_item.product_id)
            response.append(CartOutBound(id=cart.id, user_id=cart_item.user_id, product=product.__dict__))

        return CartMultiFinalOutBound(data=response)

    @classmethod
    async def remove_cart_item(cls, _id: int):
        """remove item from the cart"""
        try:
            CartModel.delete_item(_id=_id)
        except:
            raise EntityException(message=ErrorMessage.INVALID_ID.format("product")) 
        return {"message": "itme removed", "success": True}