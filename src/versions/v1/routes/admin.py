"""Admin Routes File"""
from fastapi import APIRouter
from src.services.admin.controller import AdminController
from src.services.admin.serializers import AdminLoginInbound
from src.services.category.controller import CategoryController
from src.services.category.serializers import CategoryAddInBound, CategoryUpdateInBound
from src.services.product.controller import ProductController
from src.services.product.serializers import ProductInBound, ProductUpdateInBound

router = APIRouter()

@router.get("/category", tags=["Admin GET"])
async def get_category(_id: int = None):

    """route for fetch category"""

    return await CategoryController.get_category(_id=_id)


@router.get("/product", tags=["Admin GET"])
async def get_product(product_id: int = None):

    """route for fetch product"""

    return await ProductController.get_product(_id=product_id)


@router.post("/login", tags=["Admin POST"])
async def admin_login(payload: AdminLoginInbound):

    """route for admin login"""

    return await AdminController.login(payload=payload)


@router.post("/category", tags=["Admin POST"])
async def create_category(payload: CategoryAddInBound):

    """route for create category route"""

    return await CategoryController.create_category(payload=payload)


@router.post("/product", tags=["Admin POST"])
async def create_product(payload: ProductInBound):

    """route for create product"""

    return await ProductController.create_product(payload=payload)

@router.delete("/category", tags=["Admin DELETE"])
async def delete_category(_id: int = None):

    """route for delete category"""
    return await CategoryController.delete_category(_id=_id)

@router.delete("/product", tags=["Admin DELETE"])
async def delete_product(_id: int = None):

    """route for delete product"""
    return await ProductController.delete_product(_id=_id)

@router.patch("/category", tags=["Admin PATCH"])
async def update_category(payload: CategoryUpdateInBound):

    """route for update category"""

    return await CategoryController.category_update(payload=payload)

@router.patch("/product", tags=["Admin PATCH"])
async def update_product(payload: ProductUpdateInBound):

    """route for update product"""

    return await ProductController.product_update(payload=payload)
