"""order serializers file"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, conint, constr, confloat, conlist
from src.services.order_items.serializers import OrderItemInbound, OrderItemOutbound, UpdateOrderItemOutbound
from src.services.user.serializer import UserAppOutBound


class OrderSaveInbound(BaseModel):
    """order save inbound"""
    user_id: conint(strict=True, gt=0)
    total: confloat(strict=True, ge=0)


class OrderInbound(BaseModel):
    """order """
    items: conlist(item_type=OrderItemInbound, min_length=1)


class OrderSaveOutbound(BaseModel):
    """order save outbound"""
    id: int
    user: UserAppOutBound
    total_amount: float
    created_at: datetime
    updated_at: datetime
    status: int
    items: List[OrderItemOutbound]


class UpdateOrderInbound(BaseModel):
    """order update inbound"""
    id: conint(strict=True, gt=0)
    items: conlist(item_type=UpdateOrderItemOutbound, min_length=1)


class OrderOutbound(BaseModel):
    """order outbound"""
    id: int
    user: UserAppOutBound
    total_amount: float
    created_at: datetime
    updated_at: datetime
    status: int