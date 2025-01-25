"""order serializers file"""
from datetime import datetime
from typing import List
from pydantic import BaseModel
from src.services.order_items.serializers import OrderItemInbound, OrderItemOutbound, UpdateOrderItemOutbound


class OrderSaveInbound(BaseModel):
    """order save inbound"""
    user_id: int
    total: float


class OrderInbound(OrderSaveInbound):
    """order """
    items: List[OrderItemInbound]


class OrderSaveOutbound(BaseModel):
    """order save outbound"""
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    status: int
    items: List[OrderItemOutbound]


class UpdateOrderInbound(BaseModel):
    """order update inbound"""
    id: int
    user_id: int
    items: List[UpdateOrderItemOutbound]
