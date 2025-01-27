"""user routes file"""

from fastapi import APIRouter, Request
from src.services.category.controller import CategoryController
from src.services.product.controller import ProductController
from src.services.user.controller import UserController
from src.services.user.serializer import UserLoginInbound, UserRegisterInbound, UserProfileInbound
from src.utils.auth import Auth

router = APIRouter()

@router.post("/login", tags=["User POST"])
async def login(payload: UserLoginInbound):
    """login route"""
    return await UserController.login(payload=payload)

@router.post("/register", tags=["User POST"])
async def register(payload: UserRegisterInbound):
    """login route"""
    return await UserController.register(payload=payload)

@router.get("/profile", tags=["User GET"])
@Auth.authenticate_user
async def profile(request: Request):
    """profile route"""
    return await UserController.get_profile()

@router.post("/change-password", tags=["User POST"])
@Auth.authenticate_user
async def change_password(request: Request, old_password: str, new_password: str):

    """change password route"""

    return await UserController.change_password(old_password=old_password, new_password=new_password)

@router.patch("/", tags=["User PATCH"])
@Auth.authenticate_user
async def profile_update(request: Request, payload: UserProfileInbound):
    """profile update route"""
    return await UserController.profile(payload=payload)

@router.get("/category", tags=["User GET"])
@Auth.authenticate_user
async def get_category(request: Request, _id: int = None, page: int = 1, size: int = 10):

    """route for fetch category"""

    return await CategoryController.get_category(_id=_id, page=page, size=size)

@router.get("/product", tags=["User GET"])
@Auth.authenticate_user
async def get_product(request: Request, product_id: int = None, category_id: int = None, page: int = 1, size: int = 10):

    """route for fetch product"""

    return await ProductController.get_product(_id=product_id, category_id=category_id, page=page, size=size)
