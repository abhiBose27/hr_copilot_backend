from fastapi import APIRouter

from services.department_service import (
    get_departments as get_departments_service,
    delete_department as delete_department_service,
    update_department as update_department_service,
    add_department as add_department_service
)

router = APIRouter()

@router.get("/department")
async def get_departments():
    return {
        "status": True,
        "departments": await get_departments_service()
    }

@router.delete("/department/{dept_id}")
async def delete_department(dept_id):
    return { "status": await delete_department_service(dept_id) }

@router.put("/department")
async def update_department(data: dict):
    return { "status": await update_department_service(data) }

@router.post("/department")
async def add_department(department: dict):
    return { "status": await add_department_service(department) }