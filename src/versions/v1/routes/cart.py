from fastapi import APIRouter, Request, Depends
from src.lib.sentry import sentry_wrapper
from src.services.cart.controller import CartController
from src.services.cart.serializers import CartInBound, CartUpdateInBound
from src.utils.auth import Auth


router = APIRouter()
cart_post                      = sentry_wrapper("Cart - Post")
cart_get                       = sentry_wrapper("Cart - Get")
cart_delete                    = sentry_wrapper("Cart - Delete")
cart_update                    = sentry_wrapper("Cart - Patch")


@router.get("/", dependencies=[Depends(cart_get)])
@Auth.authenticate_user
async def get(request: Request):
    """read all cart items route"""
    return await CartController.get()

@router.post("/", dependencies=[Depends(cart_post)])
@Auth.authenticate_user
async def post(request: Request, payload: CartInBound):
    """add to cart route"""
    return await CartController.post(payload=payload)

@router.patch("/", dependencies=[Depends(cart_update)])
@Auth.authenticate_user
async def patch(request: Request, payload: CartUpdateInBound):
    """update cart route"""
    return await CartController.patch(payload=payload)

@router.delete("/", dependencies=[Depends(cart_delete)])
@Auth.authenticate_user
async def delete(request: Request, _id: int):
    """remove cart from item route"""
    return await CartController.delete(_id=_id)
