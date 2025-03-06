"""aws secret manager file"""
import json
import boto3
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

from src.config.error_constants import ErrorMessage
from src.utils.common_serializers import CommonMessageOutbound


def get_secret():
    """aws secret manager"""
    try:
        client = boto3.client(service_name='secretsmanager', region_name='us-east-2')
        get_secret_value_response = client.get_secret_value(SecretId="")
        secret = get_secret_value_response['SecretString']
        secret = json.loads(secret)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(CommonMessageOutbound(data=secret)))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(CommonMessageOutbound(message=ErrorMessage.CUSTOM_MESSAGE.format(str(e)))))
