from database.db_client import db


async def get_candidates():
    candidates = await db.candidates.find().to_list()
    for c in candidates:
        c.pop("_id")
    return candidates

async def get_candidate_by_dept_id(dept_id):
    candidate = await db.candidates.find_one({"dept_id": dept_id})
    if candidate:
        candidate.pop("_id")
    return candidate

async def get_candidate_by_id(candidate_id):
    candidate = await db.candidates.find_one({"id": candidate_id})
    if candidate:
       candidate.pop("_id")
    return candidate

async def get_candidate_by_email(email):
    candidate = await db.candidates.find_one({"email": email})
    if candidate:
       candidate.pop("_id")
    return candidate

async def add_candidate(candidate):
    existing_candidate = await get_candidate_by_email(candidate["email"])
    if existing_candidate:
        return False
    await db.candidates.insert_one(candidate)
    return True

async def update_candidate(updated_candidate):
    result = await db.candidates.replace_one(
        {
            "id": updated_candidate["id"]
        },
        updated_candidate
    )
    return result.matched_count != 0

async def delete_candidate(candidate_id):
    result = await db.candidates.delete_one({"id": candidate_id})
    return result.deleted_count != 0
    