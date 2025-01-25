"""category serializer file"""
from pydantic import BaseModel


class CategoryAddInBound(BaseModel):
    """category add inbound"""
    name: str
    description: str


class CategoryAddOutBound(BaseModel):
    """category added outbound"""
    id: int
    name: str
    description: str


class CategoryUpdateInBound(BaseModel):
    """category update inbound"""
    id: int
    name: str = None
    description: str = None
