from io import BytesIO

import cv2
import qrcode
import numpy as np
from fastapi import HTTPException


async def generate_qr_code(data: str) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer


async def recognize_qr_code(file_content: bytes) -> str:
    nparr = np.frombuffer(file_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    detector = cv2.QRCodeDetector()
    data, *_ = detector.detectAndDecode(img)

    if not data:
        raise HTTPException(status_code=400, detail="QR code not found or invalid")
    return data
