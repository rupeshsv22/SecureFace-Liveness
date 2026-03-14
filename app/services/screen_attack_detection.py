# app/services/screen_attack_detection.py

import cv2
import numpy as np


def detect_screen_artifacts(frame):
    """
    Detect mobile screen / replay attacks with multiple heuristics
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -------------------------
    # 1️⃣ Reflection detection
    # -------------------------
    bright_pixels = np.sum(gray > 245)
    bright_ratio = bright_pixels / gray.size

    reflection_flag = bright_ratio > 0.03


    # -------------------------
    # 2️⃣ Grid / Moire pattern
    # -------------------------
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

    texture_strength = np.mean(np.abs(sobelx) + np.abs(sobely))

    grid_flag = texture_strength > 60


    # -------------------------
    # 3️⃣ Rectangle detection
    # -------------------------
    edges = cv2.Canny(gray, 80, 120)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=100,
        minLineLength=200,
        maxLineGap=10
    )

    rectangle_flag = lines is not None and len(lines) > 8


    # -------------------------
    # Final decision
    # -------------------------
    score = sum([reflection_flag, grid_flag, rectangle_flag])

    if score >= 2:
        return False, "Screen replay detected"

    return True, "No screen artifact"