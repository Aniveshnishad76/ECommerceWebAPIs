"""common serializers"""
from typing import Union
from pydantic import BaseModel


class CommonMessageOutbound(BaseModel):
    """success message outbound"""
    message: str = "success"
    data: Union[list, dict] = None
