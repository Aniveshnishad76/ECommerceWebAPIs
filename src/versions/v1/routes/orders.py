"""orders route file"""
from fastapi import APIRouter, Request
from src.services.order.controller import OrdersController
from src.services.order.serializers import OrderInbound, UpdateOrderInbound
from src.utils.auth import Auth

router = APIRouter()

@router.post("/", tags=["Orders POST"])
@Auth.authenticate_user
async def save(request: Request, payload: OrderInbound):

    """route for fetch category"""

    return await OrdersController.save(payload=payload)


@router.patch("/", tags=["Orders PATCH"])
@Auth.authenticate_user
async def update(request: Request, payload: UpdateOrderInbound):

    """route for fetch category"""

    return await OrdersController.update_orders(payload=payload)

@router.get("/", tags=["Orders GET"])
@Auth.authenticate_user
async def get(request: Request, _id: int = None):

    """route for fetch orders"""

    return await OrdersController.get(_id=_id)

@router.delete("/", tags=["Orders DELETE"])
@Auth.authenticate_user
async def delete(request: Request, _id: int):

    """route for fetch orders"""

    return await OrdersController.delete(_id=_id)
