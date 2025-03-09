import asyncio
from datetime import datetime
import os
from io import BytesIO

import cv2
import pytz as pytz
import qrcode
import numpy as np
from docxtpl import DocxTemplate
from fastapi import HTTPException

from app.patients.schemas import SPatientAdd


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


async def generate_consent(patient: SPatientAdd):
    template_path = os.path.join("data", "consent.docx")
    output_path = os.path.join("data", "consent2.docx")

    doc = DocxTemplate(template_path)
    context = {
        'fio': f"{patient.last_name} {patient.first_name} {patient.middle_name or ''}".strip(),
        "passport": patient.passport,
        "date": datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y"),
        "address": patient.address
    }
    doc.render(context)
    doc.save(output_path)
    return output_path


async def generate_contract(patient: SPatientAdd):
    template_path = os.path.join("data", "contract.docx")
    output_path = os.path.join("data", "contract2.docx")

    doc = DocxTemplate(template_path)
    context = {
        'fio': f"{patient.last_name} {patient.first_name} {patient.middle_name or ''}".strip(),
        "passport": patient.passport,
        "date": datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d.%m.%Y"),
        "address": patient.address,
        "phone": patient.phone_number,
        "email": patient.email
    }
    doc.render(context)
    doc.save(output_path)
    return output_path
