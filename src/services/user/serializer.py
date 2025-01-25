"""serializers file """
from pydantic import BaseModel, constr

from src.config.constants import ValidationRegexConstants
from src.utils.common_serializers import CommonMessageOutbound


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
    email: constr(strip_whitespace=True, max_length=100, pattern=ValidationRegexConstants.email_regex)
    password: constr(min_length=1, max_length=15)


class UserLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str


class UserRegisterInbound(BaseModel):
    """user register inbound"""
    username: constr(min_length=1, max_length=15)
    email: constr(strip_whitespace=True, max_length=100, pattern=ValidationRegexConstants.email_regex)
    password: constr(min_length=1, max_length=15)
    full_name: constr(min_length=1, max_length=30)
    phone_number: constr(min_length=1, max_length=15)
    address: constr(min_length=1, max_length=50) = None

class UserDetailsOutBound(BaseModel):
    """user details outbound"""
    username: str
    email: str
    full_name: str
    phone_number: str
    address: str = None


class UserFinalOutbound(CommonMessageOutbound):
    """user final outbound"""
    data: UserDetailsOutBound = None
