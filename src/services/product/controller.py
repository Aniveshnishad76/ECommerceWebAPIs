"""product controller file"""
from src.config.constants import ProductStatusConstant
from src.config.error_constants import ErrorMessage
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound, ProductInBound, ProductUpdateInBound
from src.utils.common_serializers import CommonMessageOutbound


class ProductController:

    """product controller class"""

    @classmethod
    async def get_product(cls, _id: int = None):
        """category get by id function"""
        data = ProductModel.get(_id=_id)
        if not data:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        if _id:
            result = ProductOutBound(**data.__dict__)
        else:
            categories = ProductModel.get()
            result = [ProductOutBound(**category.__dict__) for category in categories]
        return CommonMessageOutbound(data=result)

    @classmethod
    async def create_product(cls, payload: ProductInBound):
        """product create function"""
        product = ProductModel.create(**payload.__dict__)
        data = ProductOutBound(**product.__dict__)
        response = CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)
        return response

    @classmethod
    async def product_update(cls, payload: ProductUpdateInBound):
        """product update function"""

        product = ProductModel.get(_id=payload.id)
        if not product:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)

        data = ProductModel.patch(_id=payload.id, **payload.__dict__)
        return CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=data.__dict__)

    @classmethod
    async def delete_product(cls, _id: int):
        """product delete function"""

        product = ProductModel.get(_id=_id)
        if not product:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        ProductModel.patch(_id=_id, **{"status": ProductStatusConstant.Inactive})
        return CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)
