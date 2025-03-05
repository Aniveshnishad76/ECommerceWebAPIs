"""user routes file"""

from fastapi import APIRouter, Request, Depends
from src.lib.sentry import sentry_wrapper
from src.services.category.controller import CategoryController
from src.services.product.controller import ProductController
from src.services.user.controller import UserController
from src.services.user.serializer import UserLoginInbound, UserRegisterInbound, UserProfileInbound
from src.utils.auth import Auth

router = APIRouter()

user_login                      = sentry_wrapper("User - login")
user_register                   = sentry_wrapper("User - register")
user_profile                    = sentry_wrapper("User - profile")
user_change_password            = sentry_wrapper("User - change password")
user_update                     = sentry_wrapper("User - update")
user_category_get               = sentry_wrapper("User - category get")
user_product_get                = sentry_wrapper("User - product get")
user_logout                     = sentry_wrapper("User - logout")


@router.get("/profile", dependencies=[Depends(user_profile)])
@Auth.authenticate_user
async def profile(request: Request):
    """profile route"""
    return await UserController.get_profile()

@router.get("/category", dependencies=[Depends(user_category_get)])
@Auth.authenticate_user
async def get_category(request: Request, _id: int = None, page: int = 1, size: int = 10):
    """route for fetch category"""
    return await CategoryController.get_category(_id=_id, page=page, size=size)

@router.get("/product", dependencies=[Depends(user_product_get)])
@Auth.authenticate_user
async def get_product(request: Request, product_id: int = None, category_id: int = None, page: int = 1, size: int = 10):
    """route for fetch product"""
    return await ProductController.get_product(_id=product_id, category_id=category_id, page=page, size=size)

@router.post("/login", dependencies=[Depends(user_login)])
async def login(request: Request, payload: UserLoginInbound):
    """login route"""
    return await UserController.login(payload=payload)

@router.post("/register", dependencies=[Depends(user_register)])
async def register(request: Request, payload: UserRegisterInbound):
    """login route"""
    return await UserController.register(payload=payload)

@router.post("/change-password", dependencies=[Depends(user_change_password)])
@Auth.authenticate_user
async def change_password(request: Request, old_password: str, new_password: str):
    """change password route"""
    return await UserController.change_password(old_password=old_password, new_password=new_password)

@router.post("/logout", dependencies=[Depends(user_logout)])
@Auth.authenticate_user
@Auth.authenticate_user_logout
async def logout(request: Request):
    """logout route"""
    return await UserController.logout()

@router.patch("/", dependencies=[Depends(user_update)])
@Auth.authenticate_user
async def profile_update(request: Request, payload: UserProfileInbound):
    """profile update route"""
    return await UserController.profile(payload=payload)
