# app/core/model_loader.py

import mediapipe as mp
import torch

face_mesh = None
depth_model = None

def load_models():
    global face_mesh, depth_model

    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )

    depth_model = torch.hub.load(
        "intel-isl/MiDaS",
        "MiDaS_small",
        trust_repo=True
    )
    depth_model.eval()

    print("All AI models loaded")