from database.db_client import db


async def get_users():
    users = await db.users.find().to_list()
    for u in users:
        u.pop("_id")
    return users

async def get_user_by_id(user_id):
    user = await db.users.find_one({"id": user_id})
    if user:
        user.pop("_id")
    return user

async def get_user_by_email(email):
    user = await db.users.find_one({"email": email})
    if user:
       user.pop("_id")
    return user

async def update_password(user_id, new_password):
    user = await get_user_by_id(user_id)
    if user["password"] != new_password:
        await db.users.update_one(
            {
                "id": user_id
            },
            {
                "$set": {
                    "password": new_password
                }
            }
        )
        return True
    return False

async def add_user(user):
    existing_user = await get_user_by_email(user["email"])
    if existing_user:
        return False
    await db.users.insert_one(user)
    return True