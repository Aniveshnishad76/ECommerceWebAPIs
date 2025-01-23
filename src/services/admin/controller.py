"""amdin controller file"""
from src.exceptions.errors.generic import EntityException
from src.services.user.model import UserModel
from src.services.admin.model import CategoryModel, ProductModel
from src.services.admin.serializer import *
from src.utils.common import generate_jwt_token
from src.config.error_constants import ErrorMessage
from fastapi import status


class AdminController:
    """user controller class"""
    @classmethod
    async def admin_login(cls, payload: AdminLoginInbound):
        """login function"""
        user = UserModel.get_user(email=payload.email, password=payload.password, is_admin=True)
        if not user:
            data = CommonResponseOutBound(status=status.HTTP_401_UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIAL)
            return data
        # if not user:
        #     raise EntityException(message=ErrorMessage.INVALID_CREDENTIAL)
        token = generate_jwt_token(email=payload.email)
        data = AdminLoginOutBound(username=user.username, email=user.email, token=token)
        response = CommonResponseOutBound(message=ErrorMessage.LOGIN_SUCCESSFULL, data=data.__dict__)
        return response


    @classmethod
    async def create_category(cls, payload: CategoryAddInBound):
        """category create function"""
        category = CategoryModel.create(**payload.__dict__)
        data = CategoryAddOutBound(id=category.id,name=category.name, description=category.description)
        response = CommonResponseOutBound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)
        return response
    

    @classmethod
    async def get_category(cls, _id: int):
        """category get by id function"""
        category = CategoryModel.get_category(_id = _id)
        data = CategoryAddOutBound(id=category.id,name=category.name, description=category.description)
        response = CommonResponseOutBound(message=ErrorMessage.FETCH_SUCCESSFULLY, data=data.__dict__)
        return response

    @classmethod
    async def get_all_category(cls):
        """get all category function"""
        categories = CategoryModel.get_category()
        response = [CategoryAddOutBound(**category.__dict__) for category in categories] if categories else []
        return CategoryMultiFinalOutBound(data=response)
    

    @classmethod
    async def create_product(cls, payload: ProductInBound):
        """product create function"""
        product = ProductModel.create(**payload.__dict__)
        data = ProductOutBound(id=product.id,name=product.name,description=product.description,price=product.price,stock=product.stock,category_id=product.category_id)
        response = CommonResponseOutBound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)
        return response
    

    @classmethod
    async def get_product(cls, _id: int):
        """category get by id function"""
        product = ProductModel.get_product(_id = _id)
        data = ProductOutBound(id=product.id,name=product.name,description=product.description,price=product.price,stock=product.stock,category_id=product.category_id)
        response = CommonResponseOutBound(message=ErrorMessage.FETCH_SUCCESSFULLY, data=data.__dict__)
        return response
    

    @classmethod
    async def get_all_products(cls):
        """get all category function"""
        categories = ProductModel.get_product()
        response = [ProductOutBound(**category.__dict__) for category in categories] if categories else []
        return ProductMultiFinalOutBound(data=response)
    