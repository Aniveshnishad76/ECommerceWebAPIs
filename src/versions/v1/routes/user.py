from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def login():
    """login route"""
    return {"message": "Hello World"}

