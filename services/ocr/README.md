# OCR Service

## Overview
This service provides an OCR API for extracting text and bounding boxes from prescription images or PDFs using Tesseract.

## Endpoints
- `POST /ocr/upload`: Upload a prescription image or PDF. Returns extracted text and bounding boxes.

## Environment Variables
- `TESSDATA_PREFIX`: Path to Tesseract language data (optional, for custom languages).

## Running Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing
```bash
pytest test_ocr.py
```

## File Storage
- Uploaded and processed files are saved under `data/uploads/<uuid>/`.
