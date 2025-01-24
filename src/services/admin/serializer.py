from pydantic import BaseModel

class UserSchema(BaseModel):
    """Admin Login"""
    email: str
    password: str

class AddProductSchema(BaseModel):
    """Add product payload"""

    name: str
    description: str
    price: float
    stock: int

class AddCategorySchema(BaseModel):

    name: str
    description: str