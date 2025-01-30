"""user controller file"""
from src.config.error_constants import ErrorMessage
from src.services.cart.model import CartModel
from src.services.category.model import CategoryModel
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound
from src.services.category.serializers import CategoryAddOutBound
from src.services.user.model import UserModel
from src.services.cart.serializer import (
    CartInBound,
    CartOutBound,
    CartMultiFinalOutBound,
)
from src.utils.common_serializers import CommonMessageOutbound
from fastapi import status
from fastapi.responses import JSONResponse
from src.services.user.controller import user_details_context

class CartController:
    """user controller class"""

    @classmethod
    async def add_to_cart(cls, payload: CartInBound):
        """Add to Cart function"""

        user = UserModel.get_user(_id=payload.user_id)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_USER).__dict__)
        
        product = ProductModel.get(_id=payload.product_id)
        if not product:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product")).__dict__)
        
        cart = CartModel.read_items(user_id=payload.user_id, product_id=payload.product_id)
        if cart:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message="Product already exists in the cart").__dict__)
        cart = CartModel.create(**payload.__dict__)
        category = CategoryModel.get(_id=product.category_id)
        product_data = ProductOutBound(
            id = product.id,
            name = product.name,
            description = product.description,
            price = product.price,
            stock = product.stock,
            category = CategoryAddOutBound(
                id = category.id,
                name = category.name,
                description = category.description
            )
        )
        cartitem = CartOutBound(id=cart.id, user_id=user.id, product=product_data.__dict__)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=CommonMessageOutbound(data=cartitem.__dict__).dict())

    @classmethod
    async def read_all_items(cls):
        """read all items from the cart"""
        user_data = user_details_context.get()
        cart_items = CartModel.read_items(user_id=user_data.id)
        response = []
        for cart_item in cart_items:
            product = ProductModel.get(_id=cart_item.product_id)
            category = CategoryModel.get(_id=product.category_id)
            product_data = ProductOutBound(
                id = product.id,
                name = product.name,
                description = product.description,
                price = product.price,
                stock = product.stock,
                category = CategoryAddOutBound(
                    id = category.id,
                    name = category.name,
                    description = category.description
                )
            )

            response.append(CartOutBound(id=cart_item.id, user_id=cart_item.user_id, product=product_data.dict()))

        return JSONResponse(status_code=status.HTTP_200_OK, content=CartMultiFinalOutBound(data=response).dict())

    @classmethod
    async def remove_cart_item(cls, _id: int):
        """remove item from the cart"""
        cart = CartModel.read_items(_id =_id)
        print(cart)
        if not cart:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("cart")).__dict__) 
        CartModel.delete_item(_id =_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message="Item successfully removed").dict()) 