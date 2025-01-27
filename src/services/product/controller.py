"""product controller file"""
from src.config.constants import ProductStatusConstant
from src.config.error_constants import ErrorMessage
from src.services.category.model import CategoryModel
from src.services.category.serializers import CategoryAddOutBound
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound, ProductInBound, ProductUpdateInBound
from src.utils.common_serializers import CommonMessageOutbound


class ProductController:

    """product controller class"""

    @classmethod
    async def get_product(cls, _id: int = None, category_id: int = None, page: int = 1, size: int = 10):
        """category get by id function"""
        data = ProductModel.get(_id=_id, category_id=category_id, page=page, size=size)
        if not data:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        if _id:
            result = ProductOutBound(
                id=data.id,
                name=data.name,
                price=data.price,
                description=data.description,
                stock=data.stock,
                category=CategoryAddOutBound(
                    id=data.category_id,
                    name=data.category_name,
                    description=data.category_description
                ),
            )
            return CommonMessageOutbound(data=result.__dict__)
        else:
            response = []
            for product in data or []:
                result = ProductOutBound(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    stock=product.stock,
                    category=CategoryAddOutBound(
                        id=product.category_id,
                        name=product.category_name,
                        description=product.category_description
                    ),
                )
                response.append(result.__dict__)
            return CommonMessageOutbound(data=response)

    @classmethod
    async def create_product(cls, payload: ProductInBound):
        """product create function"""

        category = None
        if payload.category_id:
            category = CategoryModel.get(_id=payload.category_id)
            if not category:
                return CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("category"))
        if category:
            category = CategoryAddOutBound(
                id=category.id,
                name=category.name,
                description=category.description
            )
        product = ProductModel.create(**payload.__dict__)
        data = ProductOutBound(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=category
        )
        return CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)

    @classmethod
    async def product_update(cls, payload: ProductUpdateInBound):
        """product update function"""
        category = None
        if payload.category_id:
            category = CategoryModel.get(_id=payload.category_id)
            if not category:
                return CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("category"))
        product = ProductModel.get(_id=payload.id)
        if not product:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        product = ProductModel.patch(_id=payload.id, **payload_dict)
        if category:
            category = CategoryAddOutBound(
                id=category.id,
                name=category.name,
                description=category.description
            )
        data = ProductOutBound(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=category
        )
        return CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=data.__dict__)

    @classmethod
    async def delete_product(cls, _id: int):
        """product delete function"""

        product = ProductModel.get(_id=_id)
        if not product:
            return CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)
        ProductModel.patch(_id=_id, **{"status": ProductStatusConstant.Inactive})
        return CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)
