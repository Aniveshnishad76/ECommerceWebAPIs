from fastapi import APIRouter, Request
from src.utils.auth import Auth
from src.services.cart.controller import CartController
from src.services.cart.serializer import CartInBound

router = APIRouter()

@router.post("/cart", tags=["Cart POST"])
@Auth.authenticate_user
async def add_to_cart(request: Request, payload: CartInBound):
    """add to cart route"""
    
    return await CartController.add_to_cart(payload=payload)

@router.get("/cart", tags=["Cart GET"])
@Auth.authenticate_user
async def read_all_items(request: Request):
    """read all cart items route"""

    return await CartController.read_all_items()

@router.delete("/cart/{_id}", tags=["Cart DELETE"])
@Auth.authenticate_user
async def remove_items(request: Request, _id: int):
    """remove cart from item route"""

    return await CartController.remove_cart_item(_id=_id)

