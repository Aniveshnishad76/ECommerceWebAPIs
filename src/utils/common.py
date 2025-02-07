"""common functions file"""
import os
import time
from datetime import datetime
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

def generate_attachment_name_and_format(image):
    """Generate attachment name and format"""
    split = os.path.splitext(image.filename)
    attachment_name = split[0]
    attachment_format = split[1]
    attachment_name += f"@{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    return attachment_name, attachment_format
