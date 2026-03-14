from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.model_loader import load_models
from app.api.websocket_stream import router as websocket_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    load_models()

# 🔥 MUST INCLUDE THIS
app.include_router(websocket_router)