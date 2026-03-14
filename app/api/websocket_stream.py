from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import base64
from app.services.liveness_engine import process_frame
from app.core.session_manager import get_session, reset_session, create_session

router = APIRouter()


@router.websocket("/ws/liveness/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):

    # 🔥 Explicitly accept connection FIRST
    await websocket.accept()

    session = get_session(session_id)

    try:
        while True:
            data = await websocket.receive_text()

            img_bytes = base64.b64decode(data)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            result = process_frame(frame, session)

            await websocket.send_json(result)

    except WebSocketDisconnect:
        print("Client disconnected")


@router.post("/session/reset/{session_id}")
def reset(session_id: str):
    reset_session(session_id)
    return {"status": "session reset"}


@router.get("/session/new")
def new_session():
    session_id = create_session()
    return {"session_id": session_id}
