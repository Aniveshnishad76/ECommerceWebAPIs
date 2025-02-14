"""product controller file"""
from typing import List
from fastapi.responses import JSONResponse
from fastapi import status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from src.config.constants import ProductStatusConstant, S3Constants
from src.config.error_constants import ErrorMessage
from src.lib.s3 import Boto
from src.services.category.model import CategoryModel
from src.services.category.serializers import CategoryAddOutBound
from src.services.product.model import ProductModel
from src.services.product.serializers import ProductOutBound, ProductInBound, ProductUpdateInBound
from src.utils.common import generate_attachment_name_and_format
from src.utils.common_serializers import CommonMessageOutbound

class ProductController:

    """product controller class"""

    @classmethod
    async def get_product(cls, _id: int = None, category_id: int = None, page: int = 1, size: int = 10):
        """category get by id function"""
        data = ProductModel.get(_id=_id, category_id=category_id, page=page, size=size)
        if not data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
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
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=result.__dict__)))
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
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=response)))

    @classmethod
    async def create_product(cls, payload: ProductInBound, image: List[UploadFile] = File(...)):
        """product create function"""

        category = None
        if payload.category_id:
            category = CategoryModel.get(_id=payload.category_id)
            if not category:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("category"))))
        if category:
            category = CategoryAddOutBound(
                id=category.id,
                name=category.name,
                description=category.description
            )
        boto_client = Boto()
        image_url_list = []
        for file in image:
            attachment_name, attachment_format = generate_attachment_name_and_format(file)
            path = f"{S3Constants.Product_Image}/{attachment_name}.{attachment_format}"
            image_url = await boto_client.upload_to_s3(attachment=file, path=path)
            image_url_list.append(image_url)

        payload = payload.__dict__
        payload["image_urls"] = {"urls": image_url_list}
        product = ProductModel.create(**payload)
        data = ProductOutBound(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=category,
            image_urls=product.image_urls.get("urls", []) if product.image_urls else [],
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.CREATED_SUCCESSFULLY, data=data.__dict__)))

    @classmethod
    async def product_update(cls, payload: ProductUpdateInBound, image: List[UploadFile] = File(None)):
        """product update function"""
        category = None
        if payload.category_id:
            category = CategoryModel.get(_id=payload.category_id)
            if not category:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.INVALID_ID.format("category"))))
        product = ProductModel.get(_id=payload.id)
        if not product:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        payload_dict = payload.dict(exclude_unset=True, exclude_none=True)
        if image:
            boto_client = Boto()
            image_url_list = []
            for file in image or []:
                attachment_name, attachment_format = generate_attachment_name_and_format(file)
                path = f"{S3Constants.Product_Image}/{attachment_name}.{attachment_format}"
                image_url = await boto_client.upload_to_s3(attachment=file, path=path)
                image_url_list.append(image_url)
            payload_dict["image_urls"] = {"urls": image_url_list}
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
            category=category,
            image_urls=product.image_urls.get("urls", []) if product.image_urls else [],
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_UPDATED_SUCCESSFULLY, data=data.__dict__)))

    @classmethod
    async def delete_product(cls, _id: int):
        """product delete function"""

        product = ProductModel.get(_id=_id)
        if not product:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_NOT_FOUND)))
        ProductModel.patch(_id=_id, **{"status": ProductStatusConstant.Inactive})
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.RECORD_DELETED_SUCCESSFULLY)))
