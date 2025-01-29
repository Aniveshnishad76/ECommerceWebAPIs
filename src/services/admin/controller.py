"""admin controller file"""
from src.config.constants import UserStatusConstant
from src.services.admin.serializers import AdminLoginInbound, AdminLoginOutBound
from src.services.user.controller import user_details_context, UserController
from src.services.user.model import UserModel
from src.utils.common import generate_jwt_token, verify_password, hash_password
from src.config.error_constants import ErrorMessage
from fastapi import status
from fastapi.responses import JSONResponse
from src.utils.common_serializers import CommonMessageOutbound


class AdminController:
    """user controller class"""
    @classmethod
    async def login(cls, payload: AdminLoginInbound):
        """login function"""
        user = UserModel.get_user(email=payload.email, is_admin=True)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_CREDENTIAL).__dict__)
        if not verify_password(password=payload.password, hashed_password=user.password_hash):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.PASSWORD_DO_NOT_MATCH).__dict__)
        token = generate_jwt_token(email=payload.email)
        data = AdminLoginOutBound(username=user.username, email=user.email, token=token)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.LOGIN_SUCCESSFULLY, data=data.__dict__).__dict__)
        return response

    @classmethod
    async def delete_user(cls, user_id):
        """delete user function"""
        user = UserModel.get_user(_id=user_id)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND).__dict__)
        UserModel.delete(_id=user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY).__dict__)

    @classmethod
    async def get_profile(cls):
        """get profile function"""
        user_data = user_details_context.get()
        data = await UserController.get_by_id(_id=user_data.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.FETCH_SUCCESSFULLY, data=data.data.__dict__).__dict__)

    @classmethod
    async def activate_user(cls, user_id):
        """activate user function"""
        user = UserModel.get_user(_id=user_id)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND).__dict__)
        UserModel.patch(_id=user_id, **{"status": UserStatusConstant.Active})
        return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY).__dict__)
