from app.core import model_loader
import torch
import cv2

def check_face_depth(frame):

    midas = model_loader.depth_model
    transform = model_loader.depth_transform

    if midas is None:
        return True

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    input_batch = transform(img).unsqueeze(0)

    with torch.no_grad():
        prediction = midas(input_batch)

    depth_map = prediction.squeeze().cpu().numpy()

    return depth_map.var() > 0.02
