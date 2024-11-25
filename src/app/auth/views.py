from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("")
async def refresh_token():
    return
