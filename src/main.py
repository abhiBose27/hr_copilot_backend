from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.ws_interview_route import router as ws_interview_router
from routes.user_route import router as user_router
from routes.department_route import router as department_router
from routes.candidate_route import router as candidate_router


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

app.include_router(ws_interview_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(candidate_router, prefix="/api")
app.include_router(department_router, prefix="/api")