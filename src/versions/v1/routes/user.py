from fastapi import APIRouter

router = APIRouter()

@router.get("/login", tags=["User GET Methods"])
async def login():
    """login route"""
    return {"message": "Hello World"}

