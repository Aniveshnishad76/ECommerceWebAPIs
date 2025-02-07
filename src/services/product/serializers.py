"""product serializer file"""
from typing import List
from fastapi import Form, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, constr, confloat, conint
from src.config.error_constants import ErrorMessage
from src.services.category.serializers import CategoryAddOutBound
from src.utils.common_serializers import CommonMessageOutbound


class ProductInBound(BaseModel):
    """product add inbound"""
    name: constr(strict=True, min_length=1, max_length=50)
    description: constr(strict=True, min_length=1, max_length=100)
    price: confloat(strict=True, gt=0)
    stock: confloat(strict=True, gt=0)
    category_id: conint(strict=True, gt=0)

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            description: str = Form(...),
            price: float = Form(...),
            stock: int = Form(...),
            category_id: int = Form(...)
    ):
        """product add inbound"""
        try:
            return cls(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_id
            )
        except ValueError as e:
            error = str(e).split(":")[-1]
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.FAILED_TO_PARSE_VALUE.format(error))))



class ProductOutBound(BaseModel):
    """product add outbound"""
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: CategoryAddOutBound
    image_urls: List[str] = None


class ProductUpdateInBound(BaseModel):
    """product update inbound"""
    id: conint(strict=True, gt=0)
    name: constr(strict=True, min_length=1, max_length=50) = None
    description: constr(strict=True, min_length=1, max_length=50) = None
    price: confloat(strict=True, gt=0) = None
    stock: conint(strict=True, gt=0) = None
    category_id: conint(strict=True, gt=0) = None

    @classmethod
    def as_form(
            cls,
            id: int = Form(...),
            name: str = Form(...),
            description: str = Form(...),
            price: float = Form(...),
            stock: int = Form(...),
            category_id: int = Form(...)
    ):
        """product update inbound"""
        try:
            return cls(
                id=id,
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_id
            )
        except ValueError as e:
            error = str(e).split(":")[-1]
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.FAILED_TO_PARSE_VALUE.format(error))))
