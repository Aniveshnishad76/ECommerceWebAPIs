"""common serializers"""
from pydantic import BaseModel
from fastapi import status


class SuccessMessageOutbound(BaseModel):
    """success message outbound"""
    status_code: int = status.HTTP_200_OK
    message: str = "success"
    data: dict = {}
