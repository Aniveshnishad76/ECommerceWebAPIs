"""common functions file"""
import time
import bcrypt
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

def decode_jwt_token(token: str):
    """Decode JWT token"""
    email = jwt.decode(token, BaseConfig.jwt_secret, algorithms=[BaseConfig.jwt_algorithm])
    return email

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
