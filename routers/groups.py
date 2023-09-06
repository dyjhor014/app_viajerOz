from fastapi import APIRouter

router = APIRouter()

@router.get("/groups")
async def groups():
    return "hello groups"