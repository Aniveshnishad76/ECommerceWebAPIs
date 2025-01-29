"""common serializers"""
from typing import Union
from pydantic import BaseModel
from fastapi import status


class CommonMessageOutbound(BaseModel):
    """success message outbound"""
    message: str = "success"
    data: Union[list, dict] = None
