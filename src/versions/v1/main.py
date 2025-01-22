"""main file contains all the routes for the api"""
from fastapi import APIRouter
from src.versions.v1.routes import user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/v1/user", tags=["User"])