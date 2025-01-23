"""user controller file"""
from src.exceptions.errors.generic import EntityException
from src.services.user.model import UserModel
from src.services.user.serializer import UserLoginInbound, UserLoginOutBound
from src.utils.common import generate_jwt_token, encode_jwt_token


class UserController:
    """user controller class"""
    @classmethod
    def login(cls, payload: UserLoginInbound):
        """login function"""
        if payload.password:
            payload.password = encode_jwt_token(password=payload.password)
        user = UserModel.get_user(email=payload.email, password=payload.password)
        if not user:
            raise EntityException(message="Invalid credentials")
        token = generate_jwt_token(email=payload.email)
        data = UserLoginOutBound(username=user.username, email=user.email, token=token)
        return data
