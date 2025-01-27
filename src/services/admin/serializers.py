"""serializers file """
from pydantic import BaseModel, constr
from src.config.constants import ValidationRegexConstants


class AdminLoginInbound(BaseModel):
    """user login inbound"""
    email: constr(strip_whitespace=True, max_length=100, pattern=ValidationRegexConstants.email_regex)
    password: constr(strip_whitespace=True, min_length=1, max_length=50)


class AdminLoginOutBound(BaseModel):
    """user login outbound"""
    username: str
    email: str
    token: str
