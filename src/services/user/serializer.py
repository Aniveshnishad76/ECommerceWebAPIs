"""serializers file """
from pydantic import BaseModel, constr
from src.config.constants import ValidationRegexConstants
from src.utils.common_serializers import CommonMessageOutbound


class UserAppOutBound(BaseModel):
    """user app bound model"""
    id: int
    username: str
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
    password: constr(strict=True, min_length=1, max_length=15)


class UserLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str


class UserRegisterInbound(BaseModel):
    """user register inbound"""
    username: constr(strict=True, min_length=1, max_length=15)
    email: constr(strip_whitespace=True, max_length=100, pattern=ValidationRegexConstants.email_regex)
    password: constr(strict=True, min_length=1, max_length=15)
    full_name: constr(strict=True, min_length=1, max_length=30)
    phone_number: constr(strict=True, min_length=1, max_length=15)
    address: constr(strict=True, min_length=1, max_length=50) = None

class UserDetailsOutBound(BaseModel):
    """user details outbound"""
    id: int
    username: str
    email: str
    full_name: str
    phone_number: str
    address: str = ''
    status: int = None
    is_admin: bool = None


class UserFinalOutbound(CommonMessageOutbound):
    """user final outbound"""
    data: UserDetailsOutBound = None


class UserProfileInbound(BaseModel):
    """user profile inbound"""
    username: constr(strict=True, min_length=1, max_length=50) = None
    full_name: constr(strict=True, min_length=1, max_length=50) = None
    phone_number: constr(strict=True, min_length=1, max_length=50) = None
    address: constr(strict=True, min_length=1, max_length=50) = None
