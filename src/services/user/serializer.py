"""serializers file """
from pydantic import BaseModel


class UserLoginInbound(BaseModel):
    """user login inbound"""
    email: str
    password: str


class UserLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str

