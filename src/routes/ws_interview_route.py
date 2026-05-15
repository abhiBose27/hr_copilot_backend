from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

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
router = APIRouter()


@router.websocket("/ws/interview")
async def interview_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message_raw = await websocket.receive()
            if not message_raw.get("text"):
                continue
            message = json.loads(message_raw["text"])
            event_type = message.get("type")
            print("Message Type: {event_type}")
            if event_type == "create_session":
                session = create_session(
                    message.get("job_description"),
                    message.get("cv_data")
                )
                current_session_id = session["session_id"]
                await websocket.send_json({
                    "type": "create_session",
                    "session_id": current_session_id
                })

            elif event_type == "start_session":
                session_id = message.get("session_id")
                session = get_session(session_id)

                analysis = await analyze_jd_cv(
                    session["job_description"],
                    session["cv_description"]
                )

                save_initial_analysis(session_id, analysis)

                await websocket.send_json({
                    "type": "start_session",
                    "session_id": session_id,
                    "cv_based_cross_questions": analysis["cv_based_cross_questions"],
                    "match_score": analysis["overall_match_score"]
                })

            elif event_type == "topic_questions":
                session_id = message.get("session_id")
                topic = message.get("topic")

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

                questions = await get_topic_specific_questions(
                    jd=session["job_description"],
                    cv=session["cv_description"],
                    topic=topic,
                    answers=session["answers"]
                )

                await websocket.send_json({
                    "type": "topic_questions",
                    "session_id": session_id,
                    "suggested_questions": questions["suggested_questions"]
                })


            elif event_type == "analyze_transcript":
                session_id = message.get("session_id")
                question = message.get("question", "")
                transcript = message.get("transcript", "")

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
                session_id = message.get("session_id")
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