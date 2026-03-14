# app/services/motion_service.py

import numpy as np

previous_nose_x = None

def detect_head_movement(landmarks):
    global previous_nose_x

    nose = landmarks[1]
    current_x = nose.x

    if previous_nose_x is None:
        previous_nose_x = current_x
        return False

    movement = abs(current_x - previous_nose_x)
    previous_nose_x = current_x

    return movement > 0.02