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
from fastapi.responses import JSONResponse
from fastapi import status
from src.services.user.controller import user_details_context

class CartController:
    """user controller class"""

    @classmethod
    async def add_to_cart(cls, payload: CartInBound):
        """Add to Cart function"""

        user = UserModel.get_user(_id=payload.user_id)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_USER).__dict__)
        
        product = ProductModel.get_product(_id=payload.product_id)
        if not product:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product")).__dict__)
        
        cart = CartModel.create(**payload.__dict__)
        cartitem = CartOutBound(id=cart.id, user_id=user.id, product=product.__dict__)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=SuccessMessageOutbound(data=cartitem).__dict__)

    @classmethod
    async def read_all_items(cls):
        """read all items from the cart"""
        user_data = user_details_context.get()
        cart_items = CartModel.read_items(user_id=user_data.id)
        response = []
        for cart_item in cart_items:
            product = ProductModel.get_product(_id=cart_item.product_id)
            response.append(CartOutBound(id=cart.id, user_id=cart_item.user_id, product=product.__dict__))

        return JSONResponse(status_code=status.HTTP_200_OK, content=CartMultiFinalOutBound(data=response).dict())

    @classmethod
    async def remove_cart_item(cls, _id: int):
        """remove item from the cart"""
        try:
            CartModel.delete_item(_id=_id)
        except:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product")).__dict__) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=SuccessMessageOutbound(message="Item successfully removed").dict()) 