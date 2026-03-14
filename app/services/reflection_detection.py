import cv2
import numpy as np

def detect_screen_reflection(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect bright spots
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    reflection_ratio = np.sum(thresh == 255) / thresh.size

    if reflection_ratio > 0.01:
        return True

    return False