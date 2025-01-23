from fastapi import APIRouter

from src.services.user.controller import UserController
from src.services.user.serializer import UserLoginInbound, UserRegisterInbound
from src.utils.auth import Auth

router = APIRouter()

@router.post("/login")
async def login(payload: UserLoginInbound):
    """login route"""
    return await UserController.login(payload=payload)

@router.post("/register")
async def register(payload: UserRegisterInbound):
    """login route"""
    return await UserController.register(payload=payload)
