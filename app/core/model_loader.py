# app/core/model_loader.py

import mediapipe as mp
import torch
import onnxruntime as ort
import os

# -------------------------------------------------
# Global model variables
# -------------------------------------------------

face_mesh = None
depth_model = None
depth_transform = None
antispoof_model = None


# -------------------------------------------------
# Load all AI models
# -------------------------------------------------

def load_models():

    global face_mesh
    global depth_model
    global depth_transform
    global antispoof_model

    print("Loading AI models...")

    # ---------------------------------------------
    # Face Mesh Model
    # ---------------------------------------------
    face_mesh = mp.solutions.face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )

    # ---------------------------------------------
    # MiDaS Depth Model
    # ---------------------------------------------
    try:

        depth_model = torch.hub.load(
            "intel-isl/MiDaS",
            "MiDaS_small",
            trust_repo=True
        )

        depth_model.eval()

        transforms = torch.hub.load(
            "intel-isl/MiDaS",
            "transforms",
            trust_repo=True
        )

        depth_transform = transforms.small_transform

        print("MiDaS depth model loaded")

    except Exception as e:

        print("Depth model failed:", e)
        depth_model = None
        depth_transform = None


    # ---------------------------------------------
    # CNN Anti-Spoof Model
    # ---------------------------------------------
    model_path = "models/antispoof.onnx"

    if os.path.exists(model_path):

        antispoof_model = ort.InferenceSession(model_path)

        print("Anti-spoof model loaded")

    else:

        print("Warning: antispoof.onnx not found")
        antispoof_model = None


    print("All AI models loaded successfully")
