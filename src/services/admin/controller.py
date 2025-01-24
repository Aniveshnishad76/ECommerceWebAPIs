from .serializer import UserSchema
from src.db.session import get_db
from src.schema import UserModel, ProductModel, CategoryModel
from src.exceptions.errors.generic import EntityException, UnauthorizedException
from src.utils.common import jwt_encode

async def admin_login(payload: UserSchema, db: get_db()):
    """Admin login with creds"""

    if not (payload.email or payload.password):
        return EntityException("required fields to be filled")
    
    user = db.query(UserModel).get(email=payload.email, password=payload.password, is_admin=True)
    if not user:
        return UnauthorizedException("Invalid user credentials")
    if not user.is_admin:
        return UnauthorizedException("You're not authorize to access this panel")

    token = jwt_encode({"email": payload.email})
    return {"token": token}


async def add_product(payload: AddProductSchema, db: get_db()):
    """Adding product to inventory"""

    product = create_obj(db, payload)
    return product

async def read_product(product_id:int, db: get_db()):
    """getting product from id"""

    product = read_obj(db, product_id)
    if not product:
       return UnauthorizedException("Invalid product id")
    return product

async def update_product(product_id:int, payload: AddProductSchema, db: get_db()):
    """getting product from id"""

    product = update_product(db, product_id, payload)
    if not product:
       return UnauthorizedException("Invalid product id")
    return product


async def read_products(db:get_db()):
    """getting product from id"""

    product = read_all_objs(db)
    return product

async def remove_product(db:get_db()):
    """getting product from id"""

    product = db.query(ProductModel).filter(ProductModel.id=product_id).first()
    if not product:
       return UnauthorizedException("Invalid id")
    product.delete()
    return  {"success": True}

async def add_category(payload: AddCategorySchema, db: get_db()):
    """Adding product to inventory"""

    category = create_obj(db, payload)
    return category

async def read_categories(db:get_db()):
    """getting product from id"""

    product = read_all_category(db)
    return product
