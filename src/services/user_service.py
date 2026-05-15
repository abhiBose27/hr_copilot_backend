from database.user import (
    get_users as get_users_db,
    get_user_by_id as get_user_by_id_db,
    get_user_by_email as get_user_by_email_db,
    update_password as update_password_db,
    add_user as add_user_db,
)

REGISTERED_USERS = [
    {
        "id": 1,
        "email": "hr@company.com",
        "password": "hr123",
        "name": "Sarah Mitchell",
        "role": "HR Manager",
        "avatar": "SM"
    },
    {
        "id": 2,
        "email": "admin@company.com",
        "password": "admin123",
        "name": "Alex Johnson",
        "role": "HR Admin",
        "avatar": "AJ"
    }
]

async def get_users():
    return await get_users_db()

async def get_user_by_id(user_id):
    return await get_user_by_id_db(user_id)

async def get_user_by_email(email):
    return await get_user_by_email_db(email)

async def update_password(user_id, new_password):
    return await update_password_db(user_id, new_password)

async def add_user(user):
    return await add_user_db(user)
