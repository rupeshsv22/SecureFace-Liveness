import numpy as np

previous_frame = None


def check_micro_motion(frame):
    global previous_frame

    gray = frame.mean(axis=2)

    if previous_frame is None:
        previous_frame = gray
        return True

    diff = np.mean(np.abs(gray - previous_frame))

    previous_frame = gray

    if diff < 1.2:
        return False

    return True