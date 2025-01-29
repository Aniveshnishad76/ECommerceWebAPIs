"""category serializer file"""
from pydantic import BaseModel, constr, conint


class CategoryAddInBound(BaseModel):
    """category add inbound"""
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    description: constr(strip_whitespace=True, min_length=1, max_length=100)


class CategoryAddOutBound(BaseModel):
    """category added outbound"""
    id: int
    name: str
    description: str


class CategoryUpdateInBound(BaseModel):
    """category update inbound"""
    id: conint(strict=True, gt=0)
    name: constr(strip_whitespace=True, min_length=1, max_length=50) = None
    description: constr(strip_whitespace=True, min_length=1, max_length=50) = None
