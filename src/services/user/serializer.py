"""serializers file """
from pydantic import BaseModel
from src.utils.common_serializers import SuccessMessageOutbound


class UserAppOutBound(BaseModel):
    """user app bound model"""
    id: int
    name: str
    email: str
    full_name: str
    address: str
    phone_number: str
    is_admin: bool

    class Config:
        from_attributes = True


class UserLoginInbound(BaseModel):
    """user login inbound"""
    email: str
    password: str


class UserLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str


class UserRegisterInbound(BaseModel):
    """user register inbound"""
    username: str
    email: str
    password: str
    full_name: str
    phone_number: str
    address: str = None

class UserDetailsOutBound(BaseModel):
    """user details outbound"""
    username: str
    email: str
    password: str
    full_name: str
    phone_number: str
    address: str = None
    status: int = None


class UserFinalOutbound(SuccessMessageOutbound):
    """user final outbound"""
    data: UserDetailsOutBound = None

