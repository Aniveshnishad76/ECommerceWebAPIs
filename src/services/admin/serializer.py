"""serializers file """
from pydantic import BaseModel
from fastapi import status


class AdminLoginInbound(BaseModel):
    """user login inbound"""
    email: str
    password: str


class AdminLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str


class CommonResponseOutBound(BaseModel):
    """common response outbound"""
    status: int = status.HTTP_200_OK
    message: str = ''
    data: dict = {}


class CategoryAddInBound(BaseModel):
    """category add inbound"""
    name: str
    description: str


class CategoryAddOutBound(BaseModel):
    """category added outbound"""
    id: int
    name: str
    description: str


class CategoryMultiFinalOutBound(BaseModel):
    """multi categories list outbound"""
    status: int = status.HTTP_200_OK
    data: list[CategoryAddOutBound]


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


class ProductMultiFinalOutBound(BaseModel):
    """multi categories list outbound"""
    status: int = status.HTTP_200_OK
    data: list[ProductOutBound]
