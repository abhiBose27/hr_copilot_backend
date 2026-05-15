from fastapi import APIRouter

from services.candidate_service import (
    get_candidates as get_candidates_service,
    get_candidate_by_id as get_candidate_by_id_service,
    get_candidate_by_dept_id as get_candidate_by_dept_id_service,
    update_candidate as update_candidate_service,
    delete_candidate as delete_candidate_service,
    add_candidate as add_candidate_service
)
router = APIRouter()

@router.get("/candidate")
async def get_candidates():
    return {
        "status": True,
        "candidates": await get_candidates_service()
    }

@router.get("/candidate/candidate_id/{candidate_id}")
async def get_candidate(candidate_id):
    candidate = await get_candidate_by_id_service(candidate_id)
    return {
        "status": True if candidate != {} else False,
        "candidate": candidate
    }

@router.get("/candidate/dept_id/{dept_id}")
async def get_candidate(dept_id):
    candidate = await get_candidate_by_dept_id_service(dept_id)
    return {
        "status": True if candidate != {} else False,
        "candidate": candidate
    }

@router.post("/candidate")
async def add_candidate(candidate: dict):
    return { "status": await add_candidate_service(candidate) }

@router.put("/candidate")
async def update_candidate(data: dict):
    return { "status": await update_candidate_service(data) }

@router.delete("/candidate")
async def delete_candidate(candidate_id):
    return {
        "status": await delete_candidate_service(candidate_id)
    }