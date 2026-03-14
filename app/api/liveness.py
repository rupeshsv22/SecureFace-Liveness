# app/api/liveness.py

from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from app.services.liveness_service import check_liveness

router = APIRouter(prefix="/liveness")

@router.post("/check")
async def liveness_check(file: UploadFile = File(...)):
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    result = check_liveness(frame)

    return result