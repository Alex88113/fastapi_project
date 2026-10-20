from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hi, Shurik!"}

@router.get("/hello/{name}")
async def greeting_with_home(name: str) -> dict[str, str | datetime]:
    return {"message": f"hello, {name}!", "date": datetime.now()}