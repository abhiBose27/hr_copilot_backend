from fastapi import APIRouter

from services.user_service import (
    get_users as get_users_service, 
    get_user_by_id as get_user_by_id_service,
    get_user_by_email as get_user_by_email_service,
    add_user as add_user_service,
    update_password as update_password_service
)

router = APIRouter()

@router.get("/user")
async def get_users(email: str | None = None):
    if not email:
        return {
            "status": True,
            "users": await get_users_service()
        }
    user = await get_user_by_email_service(email)
    return {
        "status": True if user != {} else False,
        "user": user
    }

@router.get("/user/{user_id}")
async def get_user(user_id):
    user = await get_user_by_id_service(user_id)
    return {
        "status": True if user != {} else False,
        "user": user
    }

@router.post("/user")
async def add_user(user: dict):
    response = { "status": await add_user_service(user) }
    return response

@router.put("/user")
async def update_password(data: dict):
    return { "status": await update_password_service(data["id"], data["password"]) }