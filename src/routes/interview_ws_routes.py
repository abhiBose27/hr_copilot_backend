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
    generate_final_report
)

from services.pdf_service import extract_text_from_pdf

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
                        "type": "session_created",
                        "session_id": current_session_id
                    })

                # =================================================
                # ANALYZE JD + CV
                # =================================================

                elif event_type == "analyze_jd_cv":
                    session_id = data.get("session_id")
                    session = get_session(session_id)
                    cv_path = session["cv_path"]
                    extracted_text = extract_text_from_pdf(cv_path)
                    analysis = await analyze_jd_cv(
                        session["job_description"],
                        extracted_text
                    )

                    save_initial_analysis(session_id, analysis)

                    await websocket.send_json({
                        "type": "jd_cv_analysis",
                        "analysis": analysis
                    })

                # =================================================
                # START AUDIO
                # =================================================
                elif event_type == "analyze_transcript":
                    session_id = data.get("session_id")
                    question = data.get("question", "")
                    topic = data.get("topic", "")
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
                        cv=session["candidate_cv"],
                        question=question,
                        topic=topic,
                        candidate_answer=transcript,
                        interview_plan=session.get("analysis", {}).get("interview_plan", [])
                    )

                    save_answer(
                        session_id=session_id,
                        question=question,
                        topic=topic,
                        candidate_answer=transcript,
                        transcript=transcript,
                        analysis=analysis
                    )

                    await websocket.send_json({
                        "type": "answer_analysis",
                        "transcript": transcript,
                        "analysis": analysis
                    })
                
                elif event_type == "generate_report":
                    session_id = data.get("session_id")
                    session = get_session(session_id)
                    report = await generate_final_report(
                        jd=session["job_description"],
                        cv=session["candidate_cv"],
                        initial_analysis=session.get("analysis"),
                        answers=session.get("answers", [])
                    )

                    save_final_report(session_id, report)

                    await websocket.send_json({
                        "type": "final_report",
                        "report": report
                    })

                """  elif event_type == "start_audio":

                    current_question = data.get("question", "")
                    current_topic = data.get("topic", "")

                    audio_bytes = bytearray()

                    await websocket.send_json({
                        "type": "status",
                        "message": "Recording started"
                    })

                # =================================================
                # STOP AUDIO
                # =================================================

                elif event_type == "stop_audio":

                    if not current_session_id:
                        await websocket.send_json({
                            "type": "error",
                            "message": "No active session"
                        })
                        continue

                    session = get_session(current_session_id)

                    await websocket.send_json({
                        "type": "status",
                        "message": "Transcribing audio..."
                    })

                    temp_path = None

                    try:

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".webm"
                        ) as temp:

                            temp.write(audio_bytes)
                            temp_path = temp.name

                        transcript = await transcribe_audio_path(temp_path)

                        await websocket.send_json({
                            "type": "transcript",
                            "transcript": transcript
                        })

                        await websocket.send_json({
                            "type": "status",
                            "message": "Analyzing answer..."
                        })

                        analysis = await analyze_answer(
                            jd=session["job_description"],
                            cv=session["candidate_cv"],
                            question=current_question,
                            topic=current_topic,
                            candidate_answer=transcript,
                            interview_plan=session.get(
                                "analysis",
                                {}
                            ).get("interview_plan", [])
                        )

                        save_answer(
                            session_id=current_session_id,
                            question=current_question,
                            topic=current_topic,
                            candidate_answer=transcript,
                            transcript=transcript,
                            analysis=analysis
                        )

                        await websocket.send_json({
                            "type": "answer_analysis",
                            "transcript": transcript,
                            "analysis": analysis
                        })

                    finally:

                        if temp_path and os.path.exists(temp_path):
                            os.remove(temp_path) 
                 elif message.get("bytes"):

                audio_bytes.extend(message["bytes"])
                """

                # =================================================
                # FINAL REPORT
                # =================================================

            # =====================================================
            # AUDIO BYTES
            # =====================================================

    except WebSocketDisconnect:

        print("WebSocket disconnected")