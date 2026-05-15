from database.db_client import db


async def get_departments():
    departments = await db.departments.find().to_list()
    for d in departments:
        d.pop("_id")
    return departments

async def add_department(department):
    exisiting_department = await db.departments.find_one({"tag": department["tag"]})
    if exisiting_department:
        return False
    await db.departments.insert_one(department)
    return True

async def update_department(updated_department):
    result = await db.departments.replace_one(
        {
            "id": updated_department["id"]
        },
        updated_department
    )
    return result.matched_count != 0

async def delete_department(dept_id):
    result = await db.departments.delete_one({"id": dept_id})
    return result.deleted_count != 0