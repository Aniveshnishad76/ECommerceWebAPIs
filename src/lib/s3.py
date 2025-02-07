"""S3 file"""
import time
import aioboto3
from io import BytesIO
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder
from src.config.env import get_settings
from src.config.error_constants import ErrorMessage
from src.utils.common_serializers import CommonMessageOutbound

config = get_settings()

class Boto:
    """Boto class"""
    def __init__(self):
        if config.env == 'local':
            self.session = aioboto3.Session(
                aws_access_key_id=config.aws_access_key_id,
                aws_secret_access_key=config.aws_secret_access_key,
                region_name=config.aws_region
            )
        else:
            self.session = aioboto3.Session(
                region_name=config.aws_region
            )

    async def upload_to_s3(self, attachment, path: str):
        """upload file to s3"""
        try:
            async with self.session.client('s3') as s3:
                await s3.upload_fileobj(
                    attachment,
                    config.aws_s3_bucket_name,
                    path
                )
                return f"https://{config.aws_s3_bucket_name}.s3.{config.aws_region}.amazonaws.com/{path}"
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(
                CommonMessageOutbound(message=ErrorMessage.CUSTOM_MESSAGE.format("File Does not exist or has been corrupted"))))


    async def delete_from_s3(self, path: str):
        """delete file from s3"""
        try:
            async with self.session.client('s3') as s3:
                await s3.delete_object(
                    Bucket=config.aws_s3_bucket_name,
                    Key=path
                )
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(
                CommonMessageOutbound(message=ErrorMessage.CUSTOM_MESSAGE.format("File Does not exist or has been corrupted"))))

    async def download_from_s3(self, path: str):
        """download file from s3"""
        try:
            async with self.session.client('s3') as s3:
                file_stream = BytesIO()
                await s3.download_fileobj(
                    Bucket=config.aws_s3_bucket_name,
                    Key=path,
                    Fileobj=file_stream
                )
                return file_stream
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(
                CommonMessageOutbound(message=ErrorMessage.CUSTOM_MESSAGE.format("File Does not exist or has been corrupted"))))

    async def download_file_from_s3(self, file_path: str, download_path: str):
        """download file from s3"""
        try:
            async with self.session.client('s3') as s3:
                file_name = str(time.time()).replace(".", "") + file_path.split('/')[-1]
                local_key = download_path + file_name
                await s3.download_fileobj(config.aws_s3_bucket_name, file_path, local_key)
                return local_key, file_name
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(
                CommonMessageOutbound(message=ErrorMessage.CUSTOM_MESSAGE.format("File Does not exist or has been corrupted"))))
