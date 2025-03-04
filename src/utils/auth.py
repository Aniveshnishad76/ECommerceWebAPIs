"""Auth"""
from functools import wraps
import jwt
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.config.error_constants import ErrorMessage
from src.config.constants import UserStatusConstant
from src.exceptions.errors.generic import UnauthenticatedException
from src.lib.redis import redis_cache
from src.services.user.controller import UserController, user_details_context
from src.config.redis_constants import RedisKey, RedisExp
# from src.lib.redis import redis_cache
from src.config.env import get_settings
from src.utils.common import decode_jwt_token

config = get_settings()


class Auth:
    """Auth"""
    @classmethod
    def authenticate_user_logout(cls, func):
        """Authenticate user logout"""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if config.env != 'local' and "authorization" not in request.headers or not request.headers["authorization"]:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.AUTH_HEADER_ERROR)))
            try:
                if config.env != 'local':
                    token = request.headers["authorization"]
                    # Set Temp Expire Token
                    await redis_cache.set(
                        key=RedisKey.USER_EXPIRE_SESSION_TOKEN.format(token=token),
                        value=1,
                        ex=RedisExp.USER_EXPIRE_SESSION_TOKEN,
                    )
            except Exception as e:
                pass
            return await func(request, *args, **kwargs)
        return wrapper

    @classmethod
    def authenticate_user(cls, func):
        """Authenticate user"""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if config.env != "local" and (
                    "authorization" not in request.headers
                    or not request.headers["authorization"]
            ):
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.AUTH_HEADER_ERROR)))
            if config.env != "local":
                # Temp Expire Token Check
                token = request.headers["authorization"]
                exp_token = await redis_cache.get(key=RedisKey.USER_EXPIRE_SESSION_TOKEN.format(token=token))
                if exp_token:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.INVALID_TOKEN)))
                try:
                    email = decode_jwt_token(token)["email"]
                    email = email.lower()
                except Exception as e:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.INVALID_TOKEN)))

            else:
                email = config.default_email

            user_details = await UserController.get_user_by_email(email=email)
            if not user_details.data or user_details.data.status != UserStatusConstant.Active:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.USER_ONBOARDING_ERROR)))

            user_details_context.set(user_details.data)
            return await func(request, *args, **kwargs)
        return wrapper

    # @classmethod
    # def authorize_user(cls, func):
    #     """Authorize user"""
    #     @wraps(func)
    #     async def wrapper(request: Request, *args, **kwargs):
    #         # user_details = user_details_context.get()
    #         # if not user_details.is_admin:
    #             return await func(request, *args, **kwargs)
    #         return UnauthenticatedException(message=ErrorMessage.UNAUTHORIZED_REQUEST)
    #
    #     return wrapper

    @classmethod
    def authorize_admin(cls, func):
        """Authorize admin"""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user_details = user_details_context.get()
            if not user_details.is_admin:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.UNAUTHORIZED_REQUEST)))
            return await func(request, *args, **kwargs)

        return wrapper

    @classmethod
    def authenticate_admin(cls, func):
        """Authenticate admin"""

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if config.env != "local" and (
                    "authorization" not in request.headers
                    or not request.headers["authorization"]
            ):
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.AUTH_HEADER_ERROR)))
            if config.env != "local":
                # Temp Expire Token Check
                token = request.headers["authorization"]
                exp_token = await redis_cache.get(key=RedisKey.USER_EXPIRE_SESSION_TOKEN.format(token=token))
                if exp_token:
                    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.INVALID_TOKEN)))
                try:
                    email = decode_jwt_token(token)["email"]
                    email = email.lower()
                except Exception as e:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.INVALID_TOKEN)))
            else:
                email = config.default_email
            user_details = await UserController.get_user_by_email(email=email)

            if not user_details.data or user_details.data.status != UserStatusConstant.Active:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.USER_ONBOARDING_ERROR)))
            if not user_details.data.is_admin:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=jsonable_encoder(UnauthenticatedException(message=ErrorMessage.USER_ONBOARDING_ERROR)))
            user_details_context.set(user_details.data)
            return await func(request, *args, **kwargs)

        return wrapper
