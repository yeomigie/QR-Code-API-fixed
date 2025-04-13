from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import qrcode
import os
from fastapi.responses import FileResponse
from hashlib import md5

app = FastAPI()

class QRInput(BaseModel):
    content: str

# Directory to store QR images
QR_STORAGE = "qr_images"

@app.post("/generate-qr/")
async def generate_qr(input_data: QRInput):
    if not input_data.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    # Create QR code
    qr_generator = qrcode.QRCode(version=2, box_size=8, border=4)
    qr_generator.add_data(input_data.content)
    qr_generator.make(fit=True)
    qr_image = qr_generator.make_image(fill_color="black", back_color="white")
    
    # Save with hashed filename
    qr_name = f"{md5(input_data.content.encode()).hexdigest()}.png"
    qr_path = os.path.join(QR_STORAGE, qr_name)
    qr_image.save(qr_path)
    
    return {"qr_id": qr_name, "status": "QR code generated"}

@app.get("/fetch-qr/{qr_id}")
async def fetch_qr(qr_id: str):
    qr_path = os.path.join(QR_STORAGE, qr_id)
    if not os.path.isfile(qr_path):
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(qr_path, media_type="image/png")

@app.delete("/remove-qr/{qr_id}")
async def remove_qr(qr_id: str):
    qr_path = os.path.join(QR_STORAGE, qr_id)
    if not os.path.isfile(qr_path):
        raise HTTPException(status_code=404, detail="QR code not found")
    os.unlink(qr_path)
    return {"status": "QR code removed"}
