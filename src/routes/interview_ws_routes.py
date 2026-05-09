from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import tempfile
import json
import os

from services.storage_service import (
    create_session,
    get_session,
    save_initial_analysis,
    save_answer,
    save_final_report
)

from services.ai_service import (
    analyze_jd_cv,
    analyze_answer,
    generate_final_report,
    get_topic_specific_questions
)

#from services.pdf_service import extract_text_from_pdf

#from services.speech_service import transcribe_audio_path

router = APIRouter()


@router.websocket("/ws/interview")
async def interview_ws(websocket: WebSocket):

    await websocket.accept()

    #audio_bytes = bytearray()
    #current_question = ""
    #current_topic = ""
    #current_session_id = None

    try:
        while True:

            message = await websocket.receive()            

            # =====================================================
            # JSON EVENTS
            # =====================================================

            if message.get("text"):

                data = json.loads(message["text"])
                event_type = data.get("type")

                # =================================================
                # CREATE SESSION
                # =================================================
                if event_type == "create_session":
                    session = create_session(
                        data.get("job_description"),
                        data.get("cv_path")
                    )

                    current_session_id = session["session_id"]

                    await websocket.send_json({
                        "type": "create_session",
                        "session_id": current_session_id
                    })

                # =================================================
                # ANALYZE JD + CV
                # =================================================

                elif event_type == "analyze_jd_cv":
                    session_id = data.get("session_id")
                    session = get_session(session_id)

                    analysis = await analyze_jd_cv(
                        session["job_description"],
                        session["cv_description"]
                    )

                    save_initial_analysis(session_id, analysis)

                    await websocket.send_json({
                        "type": "analyze_jd_cv",
                        "cv_based_cross_questions": analysis["cv_based_cross_questions"],
                        "match_score": analysis["overall_match_score"]
                    })

                # =================================================
                # Topic Questions
                # =================================================
                elif event_type == "topic_questions":
                    session_id = data.get("session_id")
                    topic = data.get("topic")

                    session = get_session(session_id)

                    if not session:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Session not found"
                        })
                        continue

                    if not transcript:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Transcript is required"
                        })
                        continue

                    await websocket.send_json({
                        "type": "status",
                        "message": "Analyzing transcript with OpenRouter..."
                    })

                    questions = await get_topic_specific_questions(
                        jd=session["job_description"],
                        cv=session["cv_description"],
                        topic=topic,
                        answers=session["answers"]
                    )

                    await websocket.send_json({
                        "type": "topic_questions",
                        "suggested_questions": questions["suggested_questions"]
                    })


                elif event_type == "analyze_transcript":
                    session_id = data.get("session_id")
                    question = data.get("question", "")
                    transcript = data.get("transcript", "")

                    session = get_session(session_id)

                    if not session:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Session not found"
                        })
                        continue

                    if not transcript:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Transcript is required"
                        })
                        continue

                    await websocket.send_json({
                        "type": "status",
                        "message": "Analyzing transcript with OpenRouter..."
                    })

                    analysis = await analyze_answer(
                        jd=session["job_description"],
                        cv=session["cv_description"],
                        question=question,
                        candidate_answer=transcript,
                    )

                    save_answer(
                        session_id=session_id,
                        question=question,
                        candidate_answer=transcript,
                        transcript=transcript,
                        analysis=analysis
                    )

                    await websocket.send_json({
                        "type": "analyze_transcript",
                        "transcript": transcript,
                        "score": analysis["score"],
                        "quality_rating": analysis["quality_rating"],
                        "suggested_follow_up_question": analysis["suggested_follow_up_question"],
                        "other_suggested_topics_to_cover": analysis["other_suggested_topics_to_cover_in_one_word"]
                    })
                
                elif event_type == "generate_report":
                    session_id = data.get("session_id")
                    session = get_session(session_id)
                    report = await generate_final_report(
                        jd=session["job_description"],
                        cv=session["cv_description"],
                        initial_analysis=session.get("analysis"),
                        answers=session.get("answers", [])
                    )

                    save_final_report(session_id, report)

                    await websocket.send_json({
                        "type": "generate_report",
                        "report": report
                    })

    except WebSocketDisconnect:

        print("WebSocket disconnected")