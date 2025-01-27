"""Admin Routes File"""

from fastapi import APIRouter, Request
from src.services.admin.controller import AdminController
from src.services.admin.serializers import AdminLoginInbound
from src.services.category.controller import CategoryController
from src.services.category.serializers import CategoryAddInBound, CategoryUpdateInBound
from src.services.product.controller import ProductController
from src.services.product.serializers import ProductInBound, ProductUpdateInBound
from src.utils.auth import Auth

router = APIRouter()


@router.get("/category", tags=["Admin GET"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_category(request: Request, _id: int = None, page: int = 1, size: int = 10):

    """route for fetch category"""

    return await CategoryController.get_category(_id=_id, page=page, size=size)

@router.get("/product", tags=["Admin GET"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_product(request: Request, product_id: int = None, page: int = 1, size: int = 10):

    """route for fetch product"""

    return await ProductController.get_product(_id=product_id, page=page, size=size)


@router.post("/login", tags=["Admin POST"])
async def admin_login(request: Request, payload: AdminLoginInbound):

    """route for admin login"""

    return await AdminController.login(payload=payload)

@router.get("/profile", tags=["Admin GET"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def get_profile(request: Request):

    """route for get profile"""

    return await AdminController.get_profile()

@router.post("/category", tags=["Admin POST"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def create_category(request: Request, payload: CategoryAddInBound):

    """route for create category route"""

    return await CategoryController.create_category(payload=payload)

@router.post("/product", tags=["Admin POST"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def create_product(request: Request, payload: ProductInBound):

    """route for create product"""

    return await ProductController.create_product(payload=payload)

@router.delete("/category", tags=["Admin DELETE"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_category(request: Request, _id: int = None):

    """route for delete category"""
    return await CategoryController.delete_category(_id=_id)

@router.delete("/product", tags=["Admin DELETE"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_product(request: Request, _id: int = None):

    """route for delete product"""
    return await ProductController.delete_product(_id=_id)

@router.patch("/category", tags=["Admin PATCH"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def update_category(request: Request, payload: CategoryUpdateInBound):

    """route for update category"""

    return await CategoryController.category_update(payload=payload)

@router.patch("/product", tags=["Admin PATCH"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def update_product(request: Request, payload: ProductUpdateInBound):

    """route for update product"""

    return await ProductController.product_update(payload=payload)

@router.delete("/user", tags=["Admin DELETE"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def delete_user(request: Request, user_id: int):

    """route for delete user"""

    return await AdminController.delete_user(user_id=user_id)

@router.patch("/user", tags=["Admin PATCH"])
@Auth.authenticate_admin
@Auth.authorize_admin
async def activate_user(request: Request, user_id: int):
    """route for activate user"""
    return await AdminController.activate_user(user_id=user_id)
