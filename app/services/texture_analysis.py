import cv2
import numpy as np
from skimage.feature import local_binary_pattern

def detect_texture_spoof(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lbp = local_binary_pattern(gray, 8, 1, method="uniform")

    score = lbp.var()

    if score < 5:
        return True   # spoof likely

    return False
