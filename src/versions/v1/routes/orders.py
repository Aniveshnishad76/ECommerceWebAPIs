"""orders route file"""
from fastapi import APIRouter
from src.services.order.controller import OrdersController
from src.services.order.serializers import OrderInbound

router = APIRouter()

@router.post("/", tags=["Orders POST"])
async def order(user_id: int):

    """route for fetch category"""

    return await OrdersController.create_orders(user_id)

