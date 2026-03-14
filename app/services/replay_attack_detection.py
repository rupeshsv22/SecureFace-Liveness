import cv2
import numpy as np

def replay_attack_score(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    magnitude = np.log(np.abs(fshift) + 1)

    h, w = gray.shape

    center = magnitude[h//4:3*h//4, w//4:3*w//4]

    score = np.mean(center)

    return score