from uuid import uuid4

SESSIONS = {}

def create_session(job_description: str, cv_path: str):
    session_id = str(uuid4())

    SESSIONS[session_id] = {
        "session_id": session_id,
        "job_description": job_description,
        "cv_path": cv_path,
        "analysis": None,
        "answers": [],
        "final_report": None
    }
    return SESSIONS[session_id]


def get_session(session_id: str):
    return SESSIONS.get(session_id)


def save_initial_analysis(session_id: str, analysis: dict):
    SESSIONS[session_id]["analysis"] = analysis


def save_answer(
    session_id: str,
    question: str,
    topic: str,
    candidate_answer: str,
    transcript: str,
    analysis: dict
):
    SESSIONS[session_id]["answers"].append({
        "question": question,
        "topic": topic,
        "candidate_answer": candidate_answer,
        "transcript": transcript,
        "analysis": analysis
    })


def save_final_report(session_id: str, report: dict):
    SESSIONS[session_id]["final_report"] = report