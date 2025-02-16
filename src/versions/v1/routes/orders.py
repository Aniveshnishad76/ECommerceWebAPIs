"""orders route file"""
from fastapi import APIRouter, Request, Depends
from src.lib.sentry import sentry_wrapper
from src.services.order.controller import OrdersController
from src.services.order.serializers import OrderInbound, UpdateOrderInbound
from src.utils.auth import Auth

router = APIRouter()

order_post                      = sentry_wrapper("Order - post")
order_update                    = sentry_wrapper("Order - update")
order_delete                    = sentry_wrapper("Order - delete")
order_get                       = sentry_wrapper("Order - get")


@router.post("/", tags=["Orders POST"], dependencies=[Depends(order_post)])
@Auth.authenticate_user
async def save(request: Request, payload: OrderInbound):

    """route for fetch category"""

    return await OrdersController.save(payload=payload)


@router.patch("/", tags=["Orders PATCH"], dependencies=[Depends(order_update)])
@Auth.authenticate_user
async def update(request: Request, payload: UpdateOrderInbound):

    """route for fetch category"""

    return await OrdersController.update_orders(payload=payload)

@router.get("/", tags=["Orders GET"], dependencies=[Depends(order_get)])
@Auth.authenticate_user
async def get(request: Request, _id: int = None):

    """route for fetch orders"""

    return await OrdersController.get(_id=_id)

@router.delete("/", tags=["Orders DELETE"], dependencies=[Depends(order_delete)])
@Auth.authenticate_user
async def delete(request: Request, _id: int):

    """route for fetch orders"""

    return await OrdersController.delete(_id=_id)
