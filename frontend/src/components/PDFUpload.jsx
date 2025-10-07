import React, { useState } from 'react';
import { uploadPdfForOcr } from '../services/ocrService';

export default function PDFUpload({ onResult }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleFileChange(e) {
    setError(null);
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    try {
      const resultJson = await uploadPdfForOcr(file);
      onResult(resultJson);
    } catch (err) {
      setError('Failed to process PDF.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="my-6 p-4 bg-white rounded shadow border">
      <label className="block font-semibold mb-2">Upload PDF Report for OCR</label>
      <input type="file" accept="application/pdf" onChange={handleFileChange} disabled={loading} />
      {loading && <div className="mt-2 text-blue-600">Processing...</div>}
      {error && <div className="mt-2 text-red-600">{error}</div>}
    </div>
  );
}
