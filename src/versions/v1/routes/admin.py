"""Admin Routes File"""
from typing import List
from fastapi import APIRouter, Request, UploadFile, File, Depends
from src.lib.sentry import sentry_wrapper
from src.services.admin.controller import AdminController
from src.services.admin.serializers import AdminLoginInbound
from src.services.category.controller import CategoryController
from src.services.category.serializers import CategoryAddInBound, CategoryUpdateInBound
from src.services.product.controller import ProductController
from src.services.product.serializers import ProductInBound, ProductUpdateInBound
from src.utils.auth import Auth

router = APIRouter()

post_login                  = sentry_wrapper("Login - Admin post")
category_list               = sentry_wrapper("Category - Admin get")
product_list                = sentry_wrapper("Product - Admin get")
profile_get                 = sentry_wrapper("Profile - Admin get")
category_post               = sentry_wrapper("Category - Admin post")
product_post                = sentry_wrapper("Product - Admin post")
category_delete             = sentry_wrapper("Category - Admin delete")
product_delete              = sentry_wrapper("Product - Admin delete")
category_update             = sentry_wrapper("Category - Admin update")
product_update              = sentry_wrapper("Product - Admin update")
user_block                  = sentry_wrapper("User - Admin block")
user_unblock                = sentry_wrapper("User - Admin unblock")
logout                      = sentry_wrapper("Logout - Admin logout")


@router.get("/profile", dependencies=[Depends(profile_get)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_profile(request: Request):
    """route for get profile"""
    return await AdminController.get_profile()

@router.get("/category", dependencies=[Depends(category_list)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_category(request: Request, _id: int = None, page: int = 1, size: int = 10):
    """route for fetch category"""
    return await CategoryController.get_category(_id=_id, page=page, size=size)

@router.get("/product", dependencies=[Depends(product_list)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_product(request: Request, product_id: int = None, page: int = 1, size: int = 10):
    """route for fetch product"""
    return await ProductController.get_product(_id=product_id, page=page, size=size)

@router.post("/login", dependencies=[Depends(post_login)])
async def admin_login(request: Request, payload: AdminLoginInbound):
    """route for admin login"""
    return await AdminController.login(payload=payload)

@router.post("/category", dependencies=[Depends(category_post)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def create_category(request: Request, payload: CategoryAddInBound):
    """route for create category route"""
    return await CategoryController.create_category(payload=payload)

@router.post("/product", dependencies=[Depends(product_post)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def create_product(
        request: Request,
        payload: ProductInBound = Depends(ProductInBound.as_form),
        image: List[UploadFile] = File(...)
):
    """route for create product"""
    return await ProductController.create_product(payload=payload, image=image)

@router.post("/logout", dependencies=[Depends(logout)])
@Auth.authenticate_admin
@Auth.authorize_admin
@Auth.authenticate_user_logout
async def logout(request: Request):
    """route for logout"""
    return await AdminController.logout()

@router.patch("/category", dependencies=[Depends(category_update)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def update_category(request: Request, payload: CategoryUpdateInBound):
    """route for update category"""
    return await CategoryController.category_update(payload=payload)

@router.patch("/product", dependencies=[Depends(product_update)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def update_product(
        request: Request,
        payload: ProductUpdateInBound = Depends(ProductUpdateInBound.as_form),
        image: List[UploadFile] = File(None)
):
    """route for update product"""
    return await ProductController.product_update(payload=payload, image=image)

@router.patch("/user", dependencies=[Depends(user_unblock)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def activate_user(request: Request, user_id: int):
    """route for activate user"""
    return await AdminController.activate_user(user_id=user_id)

@router.delete("/user", dependencies=[Depends(user_block)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_user(request: Request, user_id: int):
    """route for delete user"""
    return await AdminController.delete_user(user_id=user_id)

@router.delete("/category", dependencies=[Depends(category_delete)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_category(request: Request, _id: int):
    """route for delete category"""
    return await CategoryController.delete_category(_id=_id)

@router.delete("/product", dependencies=[Depends(product_delete)])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_product(request: Request, _id: int):
    """route for delete product"""
    return await ProductController.delete_product(_id=_id)
