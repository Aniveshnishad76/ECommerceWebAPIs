"""Admin Routes File"""
from fastapi import APIRouter
from src.services.admin.controller import AdminController
from src.services.admin.serializer import AdminLoginInbound, CategoryAddInBound, ProductInBound


router = APIRouter()


@router.get("/category", tags=["Admin GET Methods"])
async def get_category(category_id: int ):

    """route for fetch category"""

    return await AdminController.get_category(_id=category_id)


@router.get("/category/all", tags=["Admin GET Methods"])
async def get_all_category():

    """route for fetch all categories"""

    return await AdminController.get_all_category()


@router.get("/product", tags=["Admin GET Methods"])
async def get_product(product_id: int ):

    """route for fetch product"""

    return await AdminController.get_product(_id=product_id)


@router.get("/products/all", tags=["Admin GET Methods"])
async def get_all_products():

    """route for fetch all products"""

    return await AdminController.get_all_products()


@router.post("/login", tags=["Admin POST Methods"])
async def admin_login(payload: AdminLoginInbound):
    
    """route for admi login"""

    return await AdminController.admin_login(payload=payload)


@router.post("/category", tags=["Admin POST Methods"])
async def create_category(payload: CategoryAddInBound):

    """route for create category route"""

    return await AdminController.create_category(payload=payload)


@router.post("/product", tags=["Admin POST Methods"])
async def create_product(payload: ProductInBound):

    """route for create product"""

    return await AdminController.create_product(payload=payload)
