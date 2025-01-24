import jwt

def jwt_encode(payload):
    return jwt.encode(payload, "ecommerceweb", algorithm="HS256")