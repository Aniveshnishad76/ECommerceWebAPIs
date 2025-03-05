"""main file contains all the routes for the api"""
from fastapi import APIRouter
from src.versions.v1.routes import user, admin, orders, cart

api_router = APIRouter()

api_router.include_router(user.router, prefix="/v1/user", tags=["User"])
api_router.include_router(admin.router, prefix="/v1/admin", tags=["Admin"])
api_router.include_router(orders.router, prefix="/v1/order", tags=["Order"])
api_router.include_router(cart.router, prefix="/v1/cart", tags=["Cart"])
