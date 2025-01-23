from fastapi import APIRouter

from src.services.user.controller import UserController
from src.services.user.serializer import UserLoginInbound

router = APIRouter()

@router.get("/login")
async def login(payload: UserLoginInbound):
    """login route"""
    return await UserController.login(payload=payload)

