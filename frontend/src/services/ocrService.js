// ocrService.js
// Handles PDF upload and OCR API integration
import axios from 'axios';

// Example mock OCR JSON that matches the expected frontend schema
const MOCK_OCR_JSON = {
  risk_score: 42,
  level: 'MOD',
  ddi_summary: [
    { drug1: 'Aspirin', drug2: 'Warfarin', interaction: 'Increased bleeding risk', severity: 'HIGH' }
  ],
  adr_flags: ['Gastrointestinal bleeding'],
  dfi_cautions: [],
  home_remedies: [
    { name: 'Ginger Tea', indication: 'Nausea and digestive upset', preparation: 'Steep 1-2g fresh ginger in hot water for 10 minutes', precautions: 'Avoid if taking blood thinners', evidence_level: 'Moderate' },
    { name: 'Chamomile Tea', indication: 'Anxiety and sleep disorders', preparation: 'Steep 2-3g dried flowers in hot water for 5-10 minutes', precautions: 'May interact with warfarin', evidence_level: 'Limited' }
  ],
  evidence_paths: [],
  contributors: ['OCR pipeline'],
  history: []
};

export async function uploadPdfForOcr(file) {
  // Support mock mode driven by Vite env
  const useMock = import.meta.env.VITE_ENABLE_MOCK_DATA === 'true';
  if (useMock) {
    console.log('ocrService: running in mock mode, returning sample OCR JSON');
    // Simulate async behavior
    return new Promise((res) => setTimeout(() => res(MOCK_OCR_JSON), 700));
  }

  const formData = new FormData();
  formData.append('pdf', file);
  const response = await axios.post('/api/ocr/pdf-to-json', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data; // Should be the supported JSON format
}
