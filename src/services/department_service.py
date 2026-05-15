from database.department import (
    get_departments as get_departments_db,
    add_department as add_department_db,
    update_department as update_department_db,
    delete_department as delete_department_db
)

DEPARTMENTS = [
    { "id": 1, "tag": 'eng', "name": 'Engineering', "description": 'Software development and technical roles', "color": '#6366f1', "icon": 'code' },
    { "id": 2, "tag": 'design', "name": 'Design', "description": 'UI/UX, product, and visual design roles', "color": '#ec4899', "icon": 'pen' },
    { "id": 3, "tag": 'product', "name": 'Product', "description": 'Product management and strategy roles', "color": '#f59e0b', "icon": 'box' },
    { "id": 4, "tag": 'marketing', "name": 'Marketing', "description": 'Marketing, growth, and brand roles', "color": '#22c55e', "icon": 'megaphone' },
    { "id": 5, "tag": 'sales', "name": 'Sales', "description": 'Sales, account management, and BD roles', "color": '#38bdf8', "icon": 'chart' },
    { "id": 6, "tag": 'operations', "name": 'Operations', "description": 'Operations, HR, and admin roles', "color": '#f97316', "icon": 'settings' },
]

async def get_departments():
    return await get_departments_db()

async def add_department(department):
    return await add_department_db(department)

async def update_department(updated_department):
    return await update_department_db(updated_department)

async def delete_department(dept_id):
    return await delete_department_db(dept_id)

