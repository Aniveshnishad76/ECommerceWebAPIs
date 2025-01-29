"""main file contains all the routes for the api"""
from fastapi import APIRouter
from src.versions.v1.routes import user, admin, orders

api_router = APIRouter()

api_router.include_router(user.router, prefix="/v1/user")
api_router.include_router(admin.router, prefix="/v1/admin")
api_router.include_router(orders.router, prefix="/v1/order")
