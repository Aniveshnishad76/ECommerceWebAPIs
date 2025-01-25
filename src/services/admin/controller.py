"""admin controller file"""
from src.services.admin.serializers import AdminLoginInbound, AdminLoginOutBound
from src.services.user.model import UserModel
from src.utils.common import generate_jwt_token
from src.config.error_constants import ErrorMessage
from fastapi import status
from src.utils.common_serializers import CommonMessageOutbound


class AdminController:
    """user controller class"""
    @classmethod
    async def login(cls, payload: AdminLoginInbound):
        """login function"""
        user = UserModel.get_user(email=payload.email, password=payload.password, is_admin=True)
        if not user:
            return CommonMessageOutbound(status_code=status.HTTP_401_UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIAL)
        token = generate_jwt_token(email=payload.email)
        data = AdminLoginOutBound(username=user.username, email=user.email, token=token)
        response = CommonMessageOutbound(message=ErrorMessage.LOGIN_SUCCESSFULLY, data=data.__dict__)
        return response
