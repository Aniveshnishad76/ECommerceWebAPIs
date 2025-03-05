"""serializers file """
from pydantic import BaseModel, conint
from src.services.product.serializers import ProductOutBound


class CartOutBound(BaseModel):
    """user app bound model"""
    id: int
    product: ProductOutBound
    quantity: int


class CartInBound(BaseModel):
    """Add to Cart details of product"""
    product_id: conint(strict=True, gt=0)
    quantity: conint(strict=True, ge=0)


class CartUpdateInBound(BaseModel):
    """update to Cart details of product"""
    id: conint(strict=True, ge=0)
    product_id: conint(strict=True, gt=0)
    quantity: conint(strict=True, ge=0)
