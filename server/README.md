OCR Server
==========

Lightweight Express server for PDF OCR endpoint.

Install & Run

```bash
cd server
npm install
ENABLE_MOCK_OCR=true node index.js
```

This will start the server on port 8000 and the endpoint will return mock JSON when `ENABLE_MOCK_OCR=true`.

Endpoint

- POST /api/ocr/pdf-to-json (multipart form field: `pdf`)
