"""common functions file"""
import time
import jwt
from src.config.env import get_settings

BaseConfig = get_settings()

def generate_jwt_token(email: str):
    """Generate a JWT token"""
    payload = {
        "email": email,
        "exp": int(time.time()) + 3600,
    }

    token = jwt.encode(payload, BaseConfig.jwt_secret, algorithm=BaseConfig.jwt_algorithm)
    return token

def encode_jwt_token(password: str):
    """Encode JWT token"""
    password = jwt.encode(payload=password, key=BaseConfig.jwt_secret, algorithm=BaseConfig.jwt_algorithm)
    return password