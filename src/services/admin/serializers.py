"""serializers file """
from pydantic import BaseModel


class AdminLoginInbound(BaseModel):
    """user login inbound"""
    email: str
    password: str


class AdminLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str
