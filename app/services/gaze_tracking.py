import numpy as np

def detect_gaze_direction(landmarks):

    left_eye = landmarks[33]
    right_eye = landmarks[263]

    nose = landmarks[1]

    dx = nose.x - (left_eye.x + right_eye.x)/2

    if dx > 0.02:
        return "right"

    if dx < -0.02:
        return "left"

    return "center"
