# app/services/liveness_engine.py

import cv2
import numpy as np
from app.core import model_loader
from app.services.depth_service import depth_variance_from_landmarks
from app.services.motion_service import detect_head_movement
from app.services.background_service import background_plain
from app.services.screen_attack_detection import detect_screen_artifacts
from app.services.micro_motion_check import check_micro_motion
from app.services.replay_attack_detection import replay_attack_score
from app.services.reflection_detection import detect_screen_reflection

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def eye_aspect_ratio(landmarks, eye_points):
    p = [np.array([landmarks[i].x, landmarks[i].y]) for i in eye_points]

    vertical = np.linalg.norm(p[1] - p[5]) + np.linalg.norm(p[2] - p[4])
    horizontal = np.linalg.norm(p[0] - p[3])

    return vertical / (2.0 * horizontal)


def process_frame(frame, session):

    # Convert frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ---------------------------------
    # 1️⃣ Screen Artifact Detection
    # ---------------------------------
    screen_ok, screen_msg = detect_screen_artifacts(frame)

    if not screen_ok:
        return {"status": screen_msg, "liveness": False}

    # ---------------------------------
    # 2️⃣ Reflection Detection
    # ---------------------------------
    if detect_screen_reflection(frame):
        return {"status": "Screen reflection detected", "liveness": False}

    # ---------------------------------
    # 3️⃣ Replay Attack Detection
    # ---------------------------------
    replay_score = replay_attack_score(frame)

    if replay_score > 8:
        return {"status": "Replay attack detected", "liveness": False}

    # ---------------------------------
    # 4️⃣ Micro Motion Detection
    # ---------------------------------
    motion_ok = check_micro_motion(frame)

    if not motion_ok:
        return {"status": "Static image detected", "liveness": False}

    # ---------------------------------
    # 5️⃣ Face Detection
    # ---------------------------------
    results = model_loader.face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return {"status": "No face detected", "liveness": False}

    landmarks = results.multi_face_landmarks[0].landmark

    # ---------------------------------
    # 6️⃣ Blink Detection
    # ---------------------------------
    left = eye_aspect_ratio(landmarks, LEFT_EYE)
    right = eye_aspect_ratio(landmarks, RIGHT_EYE)

    ear = (left + right) / 2

    if ear < 0.20 and session.last_eye_state == "open":
        session.blink_count += 1
        session.last_eye_state = "closed"

    elif ear >= 0.20:
        session.last_eye_state = "open"

    # ---------------------------------
    # 7️⃣ Head Movement
    # ---------------------------------
    if detect_head_movement(landmarks):
        session.head_movement = True

    # ---------------------------------
    # 8️⃣ Depth Validation
    # ---------------------------------
    session.depth_valid = depth_variance_from_landmarks(landmarks)

    # ---------------------------------
    # 9️⃣ Background Validation
    # ---------------------------------
    session.background_valid = background_plain(frame)

    # ---------------------------------
    # 🔟 Final Decision
    # ---------------------------------

    if session.blink_count == 0:
        return {"status": "Please blink your eyes", "liveness": False}

    if not session.head_movement:
        return {"status": "Move your head slightly", "liveness": False}

    if not session.depth_valid:
        return {"status": "Depth validation failed", "liveness": False}

    if (
        session.blink_count >= 3
        and session.head_movement
        and session.depth_valid
        and session.background_valid
    ):
        return {
            "status": "LIVE_VERIFIED",
            "blink_count": int(session.blink_count),
            "liveness": True
        }

    return {
        "status": "Perform blink and slight head movement",
        "blink_count": int(session.blink_count),
        "head_movement": bool(session.head_movement),
        "depth_valid": bool(session.depth_valid),
        "background_valid": bool(session.background_valid),
        "liveness": False
    }
