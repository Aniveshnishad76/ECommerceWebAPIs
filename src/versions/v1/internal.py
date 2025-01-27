"""Route for internal"""
from fastapi import APIRouter
from src.versions.v1.routes import ping, car_item

api_router = APIRouter()

api_router.include_router(ping.router, prefix="/v1/ping", tags=["Ping"])
api_router.include_router(car_item.router, prefix="/v1/cart_item", tags=["Cart"])