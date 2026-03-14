import uuid

class SessionState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.blink_count = 0
        self.head_movement = False
        self.depth_valid = False
        self.background_valid = False
        self.last_eye_state = "open"


sessions = {}


def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = SessionState()
    return session_id


def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = SessionState()
    return sessions[session_id]


def reset_session(session_id):
    if session_id in sessions:
        sessions[session_id].reset()