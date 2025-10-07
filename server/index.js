const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const { handlePdfOcr } = require('./ocr');
const axios = require('axios');

const upload = multer({ dest: path.join(__dirname, 'uploads/') });
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/ocr/pdf-to-json', upload.single('pdf'), async (req, res) => {
  try {
    const file = req.file;
    const mock = process.env.ENABLE_MOCK_OCR === 'true';
    const result = await handlePdfOcr(file, { mock });

    // Optionally forward the OCR JSON to an analysis service and return its response
    const forwardUrl = process.env.FORWARD_ANALYSIS_URL;
    if (forwardUrl) {
      try {
        const resp = await axios.post(forwardUrl, result, { timeout: 20000 });
        // if the analysis service returns JSON, pass it through
        return res.json(resp.data);
      } catch (err) {
        console.warn('Forward to analysis service failed:', err.message || err);
        // fallthrough to return the OCR result
      }
    }

    return res.json(result);
  } catch (err) {
    console.error('OCR error', err);
    res.status(500).json({ error: 'Failed to process PDF' });
  }
});

const port = process.env.PORT || 8000;
app.listen(port, () => {
  console.log(`OCR server listening on port ${port}`);
});
