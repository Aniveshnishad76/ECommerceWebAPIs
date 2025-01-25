"""product serializer file"""
from pydantic import BaseModel


class ProductInBound(BaseModel):
    """product add inbound"""
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductOutBound(BaseModel):
    """product add outbound"""
    id: int
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductUpdateInBound(BaseModel):
    """category update inbound"""
    id: int
    name: str = None
    description: str = None
    price: float = None
    stock: int = None
    category_id: int = None
