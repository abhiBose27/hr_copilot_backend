import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost:3000"),
        "X-OpenRouter-Title": os.getenv("APP_NAME", "HR Interview Copilot"),
    },
)

TEXT_MODEL = os.getenv("OPENROUTER_TEXT_MODEL", "openai/gpt-4o-transcribe")

async def ask_llm_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Generic OpenRouter JSON response helper
    """

    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except Exception:
        return {
            "error": True,
            "message": "Failed to parse LLM JSON response",
            "raw_response": content
        }


# =========================================================
# JD + CV ANALYSIS
# =========================================================

async def analyze_jd_cv(jd: str, cv: str):

    system_prompt = """
You are an expert technical recruiter assistant.

Your role is to help HR recruiters conduct structured and fair technical screening interviews.

You DO NOT make hiring decisions.

Return ONLY valid JSON.
"""

    user_prompt = f"""
Job Description:
{jd}

Candidate CV:
{cv}

Tasks:
1. Identify required skills from the JD
2. Identify matching skills in the CV
3. Identify missing skills
4. Generate skill match summary
5. Generate CV-based cross questions
6. Identify risk areas

Make sure every score is out of 100.

Return JSON in this structure:

{{
  "overall_match_score": 0,
  "summary": "",
  "matched_skills": [],
  "missing_skills": [],
  "partially_matched_skills": [],
  "risk_areas": [],
  "recommended_focus": [],
  "cv_based_cross_questions": [],
}}
"""

    return await ask_llm_json(system_prompt, user_prompt)

# =========================================================
# GET TOPIC SPECIFIC QUESTIONS
# =========================================================

async def get_topic_specific_questions(
    jd: str,
    cv: str,
    topic: str,
    answers: list
):
    system_prompt = """
You are a real-time HR Interview Copilot.

You DO NOT make hiring decisions.

Return ONLY valid JSON.
"""


    user_prompt = f"""
Job Description:
{jd}

Candidate CV:
{cv}

Previous questions and answers:
{answers}

Topic:
{topic}

Suggest 3 different questions based on the given topic that hasnt been covered. 

Return JSON in this structure:

{{
  "suggested_questions: []
}}
"""

    return await ask_llm_json(system_prompt, user_prompt)

# =========================================================
# ANSWER ANALYSIS
# =========================================================

async def analyze_answer(
    jd: str,
    cv: str,
    question: str,
    candidate_answer: str,
):

    system_prompt = """
You are a real-time HR Interview Copilot.

You help non-technical recruiters understand whether candidate answers are:
- strong
- weak
- generic
- vague
- technically correct
- suspicious

You DO NOT make hiring decisions.

Return ONLY valid JSON.
"""

    user_prompt = f"""
Job Description:
{jd}

Candidate CV:
{cv}

Current Question:
{question}

Candidate Answer:
{candidate_answer}

Analyze the answer. Mark the score out of 100

Return JSON in this structure:

{{
  "quality_rating": "",
  "score": 0,
  "summary": "",
  "what_was_correct": [],
  "what_was_missing": [],
  "expected_answer_should_include": [],
  "suggested_follow_up_question": "",
  "other_suggested_topics_to_cover_in_one_word": [],
  "red_flag": {{
      "is_red_flag": false,
      "reason": ""
  }},
  "hr_guidance": ""
}}
"""

    return await ask_llm_json(system_prompt, user_prompt)


# =========================================================
# FINAL REPORT
# =========================================================

async def generate_final_report(
    jd: str,
    cv: str,
    initial_analysis: dict,
    answers: list
):

    system_prompt = """
You are an HR interview report assistant.

You summarize interview evidence fairly and professionally.

You DO NOT make final hiring decisions.

Return ONLY valid JSON.
"""

    user_prompt = f"""
Job Description:
{jd}

Candidate CV:
{cv}

Initial Analysis:
{json.dumps(initial_analysis, indent=2)}

Interview Answers:
{json.dumps(answers, indent=2)}

Generate a final structured interview report.

Return JSON in this structure:

{{
  "candidate_summary": "",
  "overall_interview_signal": "",
  "skill_evaluation": [],
  "strengths": [],
  "weaknesses": [],
  "red_flags": [],
  "recommended_next_step": "",
  "human_decision_note": ""
}}
"""

    return await ask_llm_json(system_prompt, user_prompt)