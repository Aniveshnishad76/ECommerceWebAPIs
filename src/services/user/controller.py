"""user controller file"""
from contextvars import ContextVar
from src.config.error_constants import ErrorMessage
from src.services.user.model import UserModel
from src.services.user.serializer import (
    UserLoginInbound,
    UserLoginOutBound,
    UserRegisterInbound,
    UserFinalOutbound,
    UserDetailsOutBound,
    UserAppOutBound, UserProfileInbound
)
from fastapi import status
from fastapi.responses import JSONResponse
from src.utils.common import generate_jwt_token, verify_password, hash_password
from src.utils.common_serializers import CommonMessageOutbound

user_details_context: ContextVar[UserAppOutBound] = ContextVar("user_details")


class UserController:
    """user controller class"""
    @classmethod
    async def login(cls, payload: UserLoginInbound):
        """login function"""
        user = UserModel.get_user(email=payload.email)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.INVALID_USER).__dict__)
        if not verify_password(password=payload.password, hashed_password=user.password_hash):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=CommonMessageOutbound(message=ErrorMessage.PASSWORD_DO_NOT_MATCH).__dict__)
        token = generate_jwt_token(email=payload.email)
        data = UserLoginOutBound(username=user.username, email=user.email, token=token)
        data = CommonMessageOutbound(data=data.__dict__)
        return JSONResponse(status_code=status.HTTP_200_OK, content=data.__dict__)

    @classmethod
    async def register(cls, payload: UserRegisterInbound):
        """register function"""
        if payload.email:
            user = UserModel.get_user(email=payload.email)
            if user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.USER_ALREADY_EXISTS).__dict__)
        if payload.username:
            user = UserModel.get_user(user_name=payload.username)
            if user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.USER_ALREADY_EXISTS).__dict__)
        payload.password  = hash_password(payload.password)
        payload = payload.dict()
        if payload.get('password') and payload['password']:
            payload["password_hash"] = payload.pop("password")
        user = UserModel.create(**payload)
        return await cls.get_by_id(_id=user.id)

    @classmethod
    async def get_profile(cls):
        """get profile function"""
        user_data = user_details_context.get()
        return await cls.get_by_id(_id=user_data.id)

    @classmethod
    async def change_password(cls, old_password: str, new_password: str):
        """change password function"""
        user_data = user_details_context.get()
        user = UserModel.get_user(_id=user_data.id)
        if user.password_hash and verify_password(old_password, user.password_hash):
            password = hash_password(new_password)
            UserModel.patch(_id=user.id, **{"password_hash": password})
            updated_data = await cls.get_by_id(_id=user.id)
            return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=updated_data.__dict__).__dict__)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.PASSWORD_DO_NOT_MATCH).__dict__)

    @classmethod
    async def profile(cls, payload: UserProfileInbound):
        """profile function"""
        user_data = user_details_context.get()
        if payload.username:
            user = UserModel.get_user(user_name=payload.username)
            if user:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.USERNAME_ALREADY_EXISTS).__dict__)
        payload_dict = payload.dict(exclude_none=True, exclude_unset=True)
        UserModel.patch(_id=user_data.id, **payload_dict)
        updated_data = await cls.get_by_id(_id=user_data.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=updated_data.data.__dict__).__dict__)

    @classmethod
    async def get_by_id(cls, _id: int):
        """Get user by id"""
        user = UserModel.get_user(_id=_id)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND).__dict__)
        return UserFinalOutbound(
            data=UserDetailsOutBound(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name if user.full_name else None,
                phone_number=user.phone_number if user.phone_number else None,
                address=user.address if user.address else '',
                status=user.status,
                is_admin=user.is_admin,
            )
        )

    @classmethod
    async def get_user_by_email(cls, email):
        """Get user by email"""
        user = UserModel.get_user(email=email)
        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND).__dict__)
        return UserFinalOutbound(
            data=UserDetailsOutBound(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name if user.full_name else None,
                phone_number=user.phone_number if user.phone_number else None,
                address=user.address if user.address else '',
                status=user.status,
                is_admin=user.is_admin,
            )
        )
