"""category controller file"""
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder
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
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_ALREADY_EXISTS.format("Category"))))
        category = CategoryModel.create(**jsonable_encoder(payload))
        data = CategoryAddOutBound(**jsonable_encoder(category))
        response = JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=jsonable_encoder(data))))
        return response

    @classmethod
    async def get_category(cls, _id: int = None, page: int = 1, size: int = 10):
        """category get by id function"""

        data = CategoryModel.get(_id=_id, page=page, size=size)
        if not data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        if _id:
            result = CategoryAddOutBound(**jsonable_encoder(data))
        else:
            result = [CategoryAddOutBound(**jsonable_encoder(category)) for category in data]

        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=result)))

    @classmethod
    async def delete_category(cls, _id: int):
        """category delete function"""

        category = CategoryModel.get(_id=_id)
        if not category:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        CategoryModel.patch(_id=_id, **{"status": CategoriesStatusConstant.Inactive})
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)))

    @classmethod
    async def category_update(cls, payload: CategoryUpdateInBound):
        """category update function"""
        if not payload.name and not payload.description:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.MISSING_FILED_TO_UPDATE)))
        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        category = CategoryModel.get(_id=payload.id)
        if not category:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))

        data = CategoryModel.patch(_id=payload.id, **payload_dict)
        data = CategoryAddOutBound(**jsonable_encoder(data))
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=jsonable_encoder(data))))
