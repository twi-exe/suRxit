const fs = require('fs');
const pdf = require('pdf-parse');
const axios = require('axios');
const FormData = require('form-data');

async function extractTextFromPdf(file) {
  // If the uploaded file is plain text, return its contents directly (useful for testing)
  const lowerName = (file.originalname || '').toLowerCase();
  if ((file.mimetype && file.mimetype.startsWith('text')) || lowerName.endsWith('.txt')) {
    return fs.readFileSync(file.path, 'utf8');
  }

  const dataBuffer = fs.readFileSync(file.path);
  const data = await pdf(dataBuffer);
  return data.text;
}

async function callOcrSpace(file) {
  const apiKey = process.env.OCR_SPACE_API_KEY || ''; // set in env if available
  const form = new FormData();
  form.append('file', fs.createReadStream(file.path));
  form.append('language', 'eng');
  form.append('isOverlayRequired', 'false');

  const headers = Object.assign({ apikey: apiKey }, form.getHeaders());
  const res = await axios.post('https://api.ocr.space/parse/image', form, { headers });
  if (res.data && res.data.ParsedResults && res.data.ParsedResults[0]) {
    return res.data.ParsedResults.map(r => r.ParsedText).join('\n');
  }
  return '';
}

function parseTextToJson(text) {
  text = (text || '').replace(/\r/g, '\n');
  const lower = text.toLowerCase();

  // Medication detection using a small vocab + dosage patterns to avoid headings
  const medsVocab = [
    'Warfarin','Aspirin','Metformin','Lisinopril','Ibuprofen','Naproxen','Simvastatin','Atorvastatin','Metoprolol','Insulin'
  ];
  const meds = new Set();
  const vocabLower = new Set(medsVocab.map(s => s.toLowerCase()));

  // detect tokens followed by dosage (e.g., Warfarin 5mg)
  const dosageRegex = /\b([A-Za-z][A-Za-z0-9\-]{2,})\s+\d+\s?(?:mg|mcg|g)\b/gi;
  let m;
  while ((m = dosageRegex.exec(text)) !== null) {
    meds.add(capitalize(m[1]));
  }

  // detect vocabulary mentions
  for (const v of medsVocab) {
    const re = new RegExp('\\b' + v + '\\b', 'i');
    if (re.test(text)) meds.add(v);
  }

  // helper
  function capitalize(s) {
    if (!s) return s;
    return s[0].toUpperCase() + s.slice(1).toLowerCase();
  }

  // Also pick up explicit "A + B" or "A and B" patterns, but only keep pairs that are detected meds
  const pairRegex = /([A-Za-z][A-Za-z0-9\-]+)\s*(?:\+|and)\s*([A-Za-z][A-Za-z0-9\-]+)/g;
  const interactions = [];
  while ((m = pairRegex.exec(text)) !== null) {
    const a = capitalize(m[1]);
    const b = capitalize(m[2]);
    if (meds.has(a) && meds.has(b)) {
      interactions.push({ drug1: a, drug2: b, interaction: 'Possible interaction mentioned in report', severity: 'MOD' });
    }
  }

  // Look for explicit interaction phrases
  const explicitRegex = /interaction(?: between)?\s+([A-Z][A-Za-z0-9\-]+)\s*(?:and|\+)\s*([A-Z][A-Za-z0-9\-]+)/gi;
  while ((m = explicitRegex.exec(text)) !== null) {
    interactions.push({ drug1: m[1], drug2: m[2], interaction: 'Interaction reported', severity: 'HIGH' });
  }

  // ADR flags: keywords
  const adrKeywords = ['bleeding', 'hypoglycemia', 'renal', 'kidney', 'bruising', 'rash', 'anaphylaxis'];
  const adr_flags = adrKeywords.filter(k => lower.includes(k));

  // Home remedies detection - look for a short list
  const knownRemedies = [
    { name: 'Ginger Tea', keywords: ['ginger', 'ginger tea'] },
    { name: 'Chamomile Tea', keywords: ['chamomile', 'chamomile tea'] },
    { name: 'Turmeric', keywords: ['turmeric', 'curcumin'] }
  ];
  const home_remedies = [];
  for (const r of knownRemedies) {
    for (const kw of r.keywords) {
      if (lower.includes(kw)) {
        home_remedies.push({ name: r.name, indication: '', preparation: '', precautions: '', evidence_level: 'Unknown' });
        break;
      }
    }
  }

  // If no explicit interactions found, try to synthesize interactions from medication list (pairwise)
  if (interactions.length === 0 && meds.size > 1) {
    const medsArr = Array.from(meds);
    for (let i = 0; i < medsArr.length; i++) {
      for (let j = i + 1; j < medsArr.length; j++) {
        interactions.push({ drug1: medsArr[i], drug2: medsArr[j], interaction: 'Potential interaction (inferred from report)', severity: 'MOD' });
      }
    }
  }

  // Risk scoring heuristic
  let risk = 20;
  if (adr_flags.length > 0) risk += 30;
  risk += Math.min(30, interactions.length * 10);
  if (lower.includes('critical') || lower.includes('severe')) risk = Math.max(risk, 80);

  return {
    risk_score: Math.min(100, risk),
    level: risk >= 70 ? 'HIGH' : risk >= 40 ? 'MOD' : 'LOW',
    ddi_summary: interactions,
    adr_flags,
    dfi_cautions: [],
    home_remedies,
    evidence_paths: [],
    contributors: ['ocr-rules-parser'],
    history: []
  };
}

function validateAndNormalize(json) {
  // Ensure top-level fields exist and are in expected shapes
  const out = Object.assign({}, json);

  // helper: clean up free-text fields so terminals/logs don't display broken lines
  function sanitizeString(v) {
    if (v === undefined || v === null) return v;
    if (typeof v !== 'string') return v;
    // replace newlines with space, collapse multiple whitespace, trim ends
    return v.replace(/\r?\n+/g, ' ').replace(/\s+/g, ' ').trim();
  }

  out.risk_score = Number.isFinite(json.risk_score) ? json.risk_score : (json.risk || 0);
  out.level = json.level || (out.risk_score >= 70 ? 'HIGH' : out.risk_score >= 40 ? 'MOD' : 'LOW');

  // Normalize and sanitize ddi_summary entries
  const rawDdi = Array.isArray(json.ddi_summary) ? json.ddi_summary : (Array.isArray(json.interactions) ? json.interactions : []);
  out.ddi_summary = rawDdi.map((d) => {
    if (!d) return null;
    if (typeof d === 'string') return { drug1: null, drug2: null, interaction: sanitizeString(d), severity: null };
    return {
      drug1: d.drug1 || d.drug || d.a || null,
      drug2: d.drug2 || d.other || d.b || null,
      interaction: sanitizeString(d.interaction || d.description || ''),
      severity: d.severity || d.level || null
    };
  }).filter(Boolean);

  out.adr_flags = Array.isArray(json.adr_flags) ? json.adr_flags : (Array.isArray(json.adverse_flags) ? json.adverse_flags : []);

  // Normalize home_remedies: support both {drug,remedy,caution} and {name,indication,preparation,precautions}
  out.home_remedies = (json.home_remedies || json.remedies || []).map((r) => {
    if (!r) return null;
    if (typeof r === 'string') return { drug: sanitizeString(r), remedy: null, caution: null };
    return {
      drug: sanitizeString(r.drug || r.name || r.title || null),
      remedy: sanitizeString(r.remedy || (r.preparation ? r.preparation : r.indication) || null),
      caution: sanitizeString(r.caution || r.precautions || null),
      evidence_level: sanitizeString(r.evidence_level || r.evidence || null)
    };
  }).filter(Boolean);

  // sanitize contributors/evidence paths if present
  if (Array.isArray(out.evidence_paths)) {
    out.evidence_paths = out.evidence_paths.map(p => sanitizeString(p));
  }
  if (Array.isArray(out.contributors)) {
    out.contributors = out.contributors.map(c => sanitizeString(c));
  }

  return out;
}

async function handlePdfOcr(file, opts = { mock: false }) {
  if (!file) {
    throw new Error('No file uploaded');
  }

  if (opts.mock) {
    // return sample JSON (matching frontend mock)
    return {
      risk_score: 42,
      level: 'MOD',
      ddi_summary: [
        { drug1: 'Aspirin', drug2: 'Warfarin', interaction: 'Increased bleeding risk', severity: 'HIGH' }
      ],
      adr_flags: ['Gastrointestinal bleeding'],
      dfi_cautions: [],
      home_remedies: [
        { name: 'Ginger Tea', indication: 'Nausea', preparation: 'Steep 1-2g in hot water', precautions: 'Avoid if on blood thinners', evidence_level: 'Moderate' }
      ],
      evidence_paths: [],
      contributors: ['mock-ocr'],
      history: []
    };
  }

  // First try extracting with pdf-parse
  let text = '';
  try {
    text = await extractTextFromPdf(file);
  } catch (err) {
    console.warn('pdf-parse failed:', err.message || err);
    // If pdf-parse fails (invalid PDF), try to read file as text
    try {
      text = fs.readFileSync(file.path, 'utf8');
    } catch (err2) {
      console.warn('Reading file as text failed:', err2.message || err2);
      text = '';
    }
  }

  // If the extracted text is short or empty, call OCR.space as a fallback
  if (!text || text.trim().length < 50) {
    try {
      const ocrText = await callOcrSpace(file);
      if (ocrText && ocrText.trim().length > text.trim().length) {
        text = ocrText;
      }
    } catch (err) {
      console.warn('OCR.space fallback failed:', err.message || err);
    }
  }

  const parsed = parseTextToJson(text);
  const normalized = validateAndNormalize(parsed);
  return normalized;
}

module.exports = { handlePdfOcr };
