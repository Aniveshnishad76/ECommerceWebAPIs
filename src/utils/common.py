"""common functions file"""
import time
import jwt
from src.config.env import BaseConfig


def generate_jwt_token(email: str):
    """Generate a JWT token"""
    payload = {
        "email": email,
        "exp": int(time.time()) + 3600,
    }
    token = jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)
    return {"email": token}

def encode_jwt_token(password: str):
    """Encode JWT token"""
    password = jwt.encode(payload=password, key=BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGORITHM)
    return {"password": password}