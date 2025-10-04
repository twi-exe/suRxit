# OCR Service main.py
import os
import uuid
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image

app = FastAPI(title="OCR Service", description="Extracts text and bounding boxes from prescription images or PDFs.")

UPLOAD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/uploads'))
os.makedirs(UPLOAD_ROOT, exist_ok=True)

class OCRResponse(BaseModel):
	ingest_id: str
	raw_text: str
	blocks: list
	timestamp: str

@app.post("/ocr/upload", response_model=OCRResponse)
async def upload_ocr(file: UploadFile = File(...)):
	# Generate unique ingest_id
	ingest_id = str(uuid.uuid4())
	upload_dir = os.path.join(UPLOAD_ROOT, ingest_id)
	os.makedirs(upload_dir, exist_ok=True)
	file_path = os.path.join(upload_dir, file.filename)
	# Save uploaded file
	with open(file_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	# Open image (handle PDF/image)
	try:
		if file.filename.lower().endswith(".pdf"):
			from pdf2image import convert_from_path
			images = convert_from_path(file_path)
			image = images[0]  # Only first page for now
		else:
			image = Image.open(file_path)
	except Exception as e:
		raise HTTPException(status_code=400, detail=f"Invalid image/PDF: {e}")

	# OCR with bounding boxes
	ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
	blocks = []
	for i in range(len(ocr_data['text'])):
		if ocr_data['text'][i].strip():
			blocks.append({
				'text': ocr_data['text'][i],
				'left': ocr_data['left'][i],
				'top': ocr_data['top'][i],
				'width': ocr_data['width'][i],
				'height': ocr_data['height'][i],
				'conf': ocr_data['conf'][i]
			})
	raw_text = " ".join([b['text'] for b in blocks])
	timestamp = datetime.utcnow().isoformat()

	# Save OCR result as JSON
	import json
	result = {
		'ingest_id': ingest_id,
		'raw_text': raw_text,
		'blocks': blocks,
		'timestamp': timestamp
	}
	with open(os.path.join(upload_dir, "ocr_result.json"), "w") as f:
		json.dump(result, f, indent=2)

	return result
