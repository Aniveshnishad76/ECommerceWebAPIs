from fastapi import APIRouter
from src.db.session import get_db
from src.service.admin.controllers import *

router = APIRouter()

@router.post("/login")
async def login():
    """login route"""

    data = await admin_login(payload)
    return data

@router.post("/product")
async def add_new_product():
    """add new product"""

    data = add_product(payload)
    return data

@router.get("/product/{id}")
async def read_new_product():
    """get a single product"""

    data = read_product(id)
    return data

@router.patch("/product/{id}")
async def update_exist_product():
    """update a single product"""

    data = update_product(id, payload)
    return data

@router.patch("/product/")
async def read_all_products():
    """update a single product"""

    data = update_product(id, payload)
    return data

@router.patch("/product/{id}")
async def update_exist_product():
    """update a single product"""

    data = update_product(id, payload)
    return data
