import cv2
import numpy as np

def background_plain(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    variance = np.var(gray)

    # allow normal rooms
    if variance < 6000:
        return True

    return False