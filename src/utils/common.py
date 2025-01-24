"""common functions file"""
import time
import jwt
from src.config.env import get_settings

BaseConfig = get_settings()
import bcrypt
from src.config.env import BaseConfig


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

def decode_jwt_token(token: str):
    """Decode JWT token"""
    email = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM])
    return email

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
