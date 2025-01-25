"""category controller file"""
from src.config.constants import CategoriesStatusConstant
from src.config.error_constants import ErrorMessage
from src.services.category.model import CategoryModel
from src.services.category.serializers import CategoryAddInBound, CategoryAddOutBound, CategoryUpdateInBound
from src.utils.common_serializers import CommonMessageOutbound


class CategoryController:
    """category controller class"""
    @classmethod
    async def create_category(cls, payload: CategoryAddInBound):
        """category create function"""
        if payload.name:
            data = CategoryModel.get(name=payload.name)
            if data:
                return CommonMessageOutbound(message=ErrorMessage.RECORD_ALREADY_EXISTS.format("Category"))
        category = CategoryModel.create(**payload.__dict__)
        data = CategoryAddOutBound(**category.__dict__)
        response = CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)
        return response

    @classmethod
    async def get_category(cls, _id: int = None):
        """category get by id function"""

        data = CategoryModel.get(_id=_id)
        if not data:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        if _id:
            result = CategoryAddOutBound(**data.__dict__)
        else:
            result = [CategoryAddOutBound(**category.__dict__) for category in data]

        return CommonMessageOutbound(data=result)

    @classmethod
    async def delete_category(cls, _id: int):
        """category delete function"""

        category = CategoryModel.get(_id=_id)
        if not category:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        CategoryModel.patch(_id=_id, **{"status": CategoriesStatusConstant.Inactive})
        return CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)

    @classmethod
    async def category_update(cls, payload: CategoryUpdateInBound):
        """category update function"""

        category = CategoryModel.get(_id=payload.id)
        if not category:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)

        data = CategoryModel.patch(_id=payload.id, **payload.__dict__)
        return CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=data.__dict__)
