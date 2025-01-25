"""order items serializers"""
from pydantic import BaseModel


class OrderItemInbound(BaseModel):
    """order item inbound"""
    order_id: int
    product_id: int
    quantity: int
    price: float


class OrderItemOutbound(OrderItemInbound):
    """order item outbound"""
    id: int


class UpdateOrderItemOutbound(BaseModel):
    """update order item outbound"""
    id: int
    product_id: int
    quantity: int