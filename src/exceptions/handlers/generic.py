"""Centralized exception handeling"""
from fastapi import Request, status
from starlette.responses import JSONResponse
from main import app
from src.exceptions.errors.generic import EntityException


@app.exception_handler(EntityException)
async def entity_not_found_exception_handler(request: Request, exc: EntityException):
    """Entity not found exception handler"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "failure",
            "code": status.HTTP_400_BAD_REQUEST,
            "message": exc.message,
        },
    )