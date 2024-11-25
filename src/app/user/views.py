from fastapi import APIRouter

user_router = APIRouter()


@user_router.post("")
async def create_user():
    return


@user_router.post("/login")
async def login():
    return


@user_router.put("/{user_id}/password")
async def update_password():
    return
