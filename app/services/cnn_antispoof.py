import cv2
import numpy as np
from app.core import model_loader


def cnn_antispoof(frame):

    session = model_loader.antispoof_model

    if session is None:
        return 1.0

    img = cv2.resize(frame, (128, 128))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    input_name = session.get_inputs()[0].name

    result = session.run(None, {input_name: img})[0]

    return float(result[0][0])
