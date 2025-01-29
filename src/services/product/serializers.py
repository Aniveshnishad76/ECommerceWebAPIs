"""product serializer file"""
from pydantic import BaseModel, constr, confloat, conint
from src.services.category.serializers import CategoryAddOutBound


class ProductInBound(BaseModel):
    """product add inbound"""
    name: constr(strict=True, min_length=1, max_length=50)
    description: constr(strict=True, min_length=1, max_length=100)
    price: confloat(strict=True, gt=0)
    stock: confloat(strict=True, gt=0)
    category_id: conint(strict=True, gt=0)


class ProductOutBound(BaseModel):
    """product add outbound"""
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: CategoryAddOutBound


class ProductUpdateInBound(BaseModel):
    """category update inbound"""
    id: conint(strict=True, gt=0)
    name: constr(strict=True, min_length=1, max_length=50) = None
    description: constr(strict=True, min_length=1, max_length=50) = None
    price: confloat(strict=True, gt=0) = None
    stock: conint(strict=True, gt=0) = None
    category_id: conint(strict=True, gt=0) = None
