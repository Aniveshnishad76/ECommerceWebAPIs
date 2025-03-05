"""Cart controller file"""
from src.config.error_constants import ErrorMessage
from src.services.cart.models import CartModel
from src.services.cart.serializers import CartInBound, CartOutBound, CartUpdateInBound
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound
from src.services.category.serializers import CategoryAddOutBound
from src.utils.common_serializers import CommonMessageOutbound
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.services.user.controller import user_details_context

class CartController:
    """user controller class"""

    @classmethod
    async def post(cls, payload: CartInBound):
        """Add to Cart function"""
        user_data = user_details_context.get()
        product = ProductModel.get(_id=payload.product_id)
        if not product:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product"))))

        cart = CartModel.get(user_id=user_data.id, product_id=payload.product_id)
        if cart:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_ALREADY_EXISTS.format("product"))))
        payload = payload.__dict__
        payload["user_id"] = user_data.id
        cart = CartModel.create(**payload)
        data = CartOutBound(
            id=cart.id,
            quantity=cart.quantity,
            product=ProductOutBound(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                category=CategoryAddOutBound(
                    id=product.category_id,
                    name=product.category_name,
                    description=product.category_description
                ),
                image_urls=product.image_urls.get("urls", [])
            )
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(CommonMessageOutbound(data=jsonable_encoder(data))))

    @classmethod
    async def get(cls):
        """read all items from the cart"""
        user_data = user_details_context.get()
        cart_items = CartModel.get(user_id=user_data.id)
        response = []
        for cart_item in cart_items:
            data = CartOutBound(
                id=cart_item.id,
                quantity=cart_item.quantity,
                product=ProductOutBound(
                    id=cart_item.product_id,
                    name=cart_item.product_name,
                    description=cart_item.product_description,
                    price=cart_item.product_price,
                    stock=cart_item.product_stock,
                    category=CategoryAddOutBound(
                        id=cart_item.category_id,
                        name=cart_item.category_name,
                        description=cart_item.category_description
                    ),
                    image_urls=cart_item.product_image.get("urls", [])
                )
            )
            response.append(data.__dict__)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=response)))

    @classmethod
    async def delete(cls, _id: int):
        """remove item from the cart"""
        user = user_details_context.get()
        cart = CartModel.get(_id =_id, user_id=user.id)
        if not cart:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("cart"))))
        CartModel.delete(_id =_id, user_id=user.id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)))

    @classmethod
    async def patch(cls, payload: CartUpdateInBound):
        """update cart item"""
        user_data = user_details_context.get()
        cart = CartModel.get(_id=payload.id, user_id=user_data.id, product_id=payload.product_id)
        if not cart:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("cart"))))

        product = ProductModel.get(_id=payload.product_id)
        if not product:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("product"))))

        cart_item = CartModel.patch(_id=payload.id, **{"quantity": payload.quantity})
        data = CartOutBound(
            id=cart_item.id,
            quantity=cart_item.quantity,
            product=ProductOutBound(
                id=cart_item.product_id,
                name=cart_item.product_name,
                description=cart_item.product_description,
                price=cart_item.product_price,
                stock=cart_item.product_stock,
                category=CategoryAddOutBound(
                    id=cart_item.category_id,
                    name=cart_item.category_name,
                    description=cart_item.category_description
                ),
                image_urls=cart_item.product_image.get("urls", [])
            )
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=jsonable_encoder(data))))
