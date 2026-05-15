from database.candidate import (
    get_candidates as get_candidates_db,
    add_candidate as add_candidate_db,
    get_candidate_by_dept_id as get_candidate_by_dept_id_db,
    get_candidate_by_id as get_candidate_by_id_db,
    get_candidate_by_email as get_candidate_by_email_db,
    delete_candidate as delete_candidate_db,
    update_candidate as update_candidate_db
)

CANDIDATES = [{
    "id": 1, "full_name": '', "email": '', "phone": '', "position": '', "department_id": '',
    "experience": '', "location": '', "githubUrl": '', "linkedin_url": '',
    "portfolio_url": '', "othe_url": '', "resume_file": None, "resume_name": '', "resume_path": '',
    "status": 'pending', "interview_date": '', "interview_mode": 'virtual',
    "meeting_link": '', "meeting_platform": 'Google Meet',
    "hr_remarks": '', "skills": '', "notice_period": '', "expected_ctc": '', "job_description": '',
    "added_by": '', "created_at": None
}]

async def get_candidates():
    return await get_candidates_db()

async def add_candidate(candidate):
    """ for c in CANDIDATES:
        if c["email"] == candidate["email"]:
            return False
    CANDIDATES.append(candidate)
    return True """
    return await add_candidate_db(candidate)

async def get_candidate_by_dept_id(dept_id):
    """ for c in CANDIDATES:
        if c["dept_id"] == dept_id:
            return c
    return {} """
    return await get_candidate_by_dept_id_db(dept_id)

async def get_candidate_by_id(candidate_id):
    """ for c in CANDIDATES:
        if c["id"] == candidate_id:
            return c
    return {} """
    return await get_candidate_by_id_db(candidate_id)

async def get_candidate_by_email(email):
    """ for c in CANDIDATES:
        if c["id"] == candidate_id:
            return c
    return {} """
    return await get_candidate_by_email_db(email)

async def delete_candidate(candidate_id):
    """ new_candidates = []
    is_deleted = False
    for c in CANDIDATES:
        if c["id"] != candidate_id:
            new_candidates.append(c)
        else:
            is_deleted = True
    CANDIDATES = new_candidates
    return is_deleted """
    return await delete_candidate_db(candidate_id)

async def update_candidate(updated_candidate):
    """ new_candidates = []
    is_updated = False
    for c in CANDIDATES:
        if c["id"] != updated_candidate["id"]:
            new_candidates.append(c)
        else:
            is_updated = True
    new_candidates.append(updated_candidate)
    CANDIDATES = new_candidates
    return is_updated """
    return await update_candidate_db(updated_candidate)
    


