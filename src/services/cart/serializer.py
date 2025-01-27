"""serializers file """
from pydantic import BaseModel
from fastapi import status


class ProductOutBound(BaseModel):
    """Product details out bound"""

    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class CartOutBound(BaseModel):
    """user app bound model"""

    id: int
    user_id: int
    product: ProductOutBound

    class Config:
        from_attributes = True

class CartInBound(BaseModel):
    """Add to Cart details of product"""

    product_id: int
    user_id: int

    class Config:
        from_attributes = True

class CartMultiFinalOutBound(BaseModel):
    """Products in cart list"""
    status: int = status.HTTP_200_OK
    data: list[CartOutBound]