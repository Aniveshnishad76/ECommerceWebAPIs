from fastapi import APIRouter

from src.services.cart.controller import CartController
from src.services.cart.serializer import CartInBound

router = APIRouter()

@router.post("/add-to-cart", tags=["Cart POST"])
async def add_to_cart(payload: CartInBound):
    """add to cart route"""
    
    return await CartController.add_to_cart(payload=payload)

@router.get("/cart-items", tags=["Cart GET"])
async def read_all_items():
    """read all cart items route"""

    return await CartController.read_all_items()

@router.get("/remove-cart-item/{_id}", tags=["Cart DELETE"])
async def remove_items(_id):
    """remove cart from item route"""

    return await CartController.remove_cart_item(_id=_id)

