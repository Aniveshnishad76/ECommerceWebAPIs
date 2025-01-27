"""order items serializers"""
from pydantic import BaseModel, conint, confloat
from src.services.product.serializers import ProductOutBound


class OrderItemInbound(BaseModel):
    """order item inbound"""
    product_id: conint(strict=True, gt=0)
    quantity: conint(strict=True, gt=0)

class OrderItemFinalInbound(BaseModel):
    """order item final inbound"""
    order_id: conint(strict=True, gt=0)
    product_id: conint(strict=True, gt=0)
    quantity: conint(strict=True, gt=0)
    price: confloat(strict=True, gt=0)


class OrderItemOutbound(BaseModel):
    """order item outbound"""
    id: int
    product: ProductOutBound
    quantity: int


class UpdateOrderItemOutbound(BaseModel):
    """update order item outbound"""
    id: int
    quantity: int