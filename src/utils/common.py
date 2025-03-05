"""common functions file"""
import os
import time
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

import bcrypt
import jwt
from src.config.env import get_settings
from src.config.error_constants import ErrorMessage
from src.utils.common_serializers import CommonMessageOutbound

BaseConfig = get_settings()

def generate_jwt_token(email: str, is_admin: bool = False):
    """Generate a JWT token"""
    payload = {
        "email": email,
        "is_admin": is_admin,
        "exp": int(time.time()) + 86400,
    }
    token = jwt.encode(payload, BaseConfig.jwt_secret, algorithm=BaseConfig.jwt_algorithm)
    return token

def decode_jwt_token(token: str):
    """Decode JWT token"""
    try:
        email = jwt.decode(token, BaseConfig.jwt_secret, algorithms=[BaseConfig.jwt_algorithm])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_TOKEN)))
    return email

def hash_password(password: str):
    """hash password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str):
    """varify password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_attachment_name_and_format(image):
    """Generate attachment name and format"""
    split = os.path.splitext(image.filename)
    attachment_name = split[0]
    attachment_format = split[1]
    attachment_name += f"@{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    return attachment_name, attachment_format
