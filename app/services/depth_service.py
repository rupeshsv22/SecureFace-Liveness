import numpy as np

def depth_variance_from_landmarks(landmarks):

    depth_points = [
        landmarks[1].z,    # nose
        landmarks[234].z,  # left cheek
        landmarks[454].z,  # right cheek
        landmarks[152].z,  # chin
        landmarks[10].z    # forehead
    ]

    depth_var = np.var(depth_points)

    if depth_var > 0.0003:
        return True

    return False
