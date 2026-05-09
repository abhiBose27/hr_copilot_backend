from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

""" from routes.session_routes import router as session_router
#from routes.analysis_routes import router as analysis_router
from routes.audio_routes import router as audio_router
from routes.report_routes import router as report_router
from routes.audio_ws_routes import router as ws_audio_router """
from routes.interview_ws_routes import router as ws_router


app = FastAPI(title="HR Interview Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

""" app.include_router(session_router, prefix="/api")
app.include_router(ws_audio_router, prefix="/api")
#app.include_router(analysis_router, prefix="/api")
app.include_router(audio_router, prefix="/api")
app.include_router(report_router, prefix="/api") """
app.include_router(ws_router, prefix="/api")