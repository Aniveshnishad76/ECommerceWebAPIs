"""admin controller file"""
from src.config.constants import UserStatusConstant
from src.services.admin.serializers import AdminLoginInbound, AdminLoginOutBound
from src.services.user.controller import user_details_context, UserController
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

    @classmethod
    async def delete_user(cls, user_id):
        """delete user function"""
        user = UserModel.get_user(_id=user_id)
        if not user:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        UserModel.delete(_id=user_id)
        return CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)

    @classmethod
    async def get_profile(cls):
        """get profile function"""
        user_data = user_details_context.get()
        return await UserController.get_by_id(_id=user_data.id)

    @classmethod
    async def activate_user(cls, user_id):
        """activate user function"""
        user = UserModel.get_user(_id=user_id)
        if not user:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        UserModel.patch(_id=user_id, **{"status": UserStatusConstant.Active})
        return CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY)
