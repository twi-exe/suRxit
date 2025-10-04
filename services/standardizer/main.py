# Standardizer Service main.py
import os
import glob
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from rapidfuzz import process, fuzz

app = FastAPI(title="Standardizer Service", description="Maps entity names to canonical IDs using fuzzy string matching on manual CSVs.")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/manual'))

class EntityIn(BaseModel):
	text: str
	type: str

class StandardizedEntity(BaseModel):
	text: str
	type: str
	canonical_id: str
	score: float
	manual_review_flag: bool

class StandardizeRequest(BaseModel):
	entities: List[EntityIn]

class StandardizeResponse(BaseModel):
	results: List[StandardizedEntity]

def load_canonical_dicts():
	# Load all relevant CSVs into a dict: {type: {name: id}}
	mapping = {}
	for fname in glob.glob(os.path.join(DATA_DIR, 'nodes_*.csv')):
		typ = fname.split('nodes_')[-1].split('.')[0].upper()
		df = pd.read_csv(fname)
		# Expect columns: id, name (or similar)
		name_col = next((c for c in df.columns if c.lower() in ['name', 'drug', 'allergy', 'food', 'sideeffect', 'patient']), None)
		id_col = next((c for c in df.columns if c.lower() in ['id', 'drug_id', 'allergy_id', 'food_id', 'sideeffect_id', 'patient_id']), None)
		if name_col and id_col:
			mapping[typ] = {str(row[name_col]): str(row[id_col]) for _, row in df.iterrows()}
	return mapping

CANONICAL_DICTS = load_canonical_dicts()

@app.post("/standardize", response_model=StandardizeResponse)
async def standardize_entities(req: StandardizeRequest):
	results = []
	for ent in req.entities:
		typ = ent.type.upper()
		candidates = CANONICAL_DICTS.get(typ, {})
		canonical_id = None
		score = 0.0
		manual_review_flag = True
		if candidates:
			match, score, _ = process.extractOne(ent.text, candidates.keys(), scorer=fuzz.ratio)
			canonical_id = candidates[match] if score > 80 else None
			manual_review_flag = score <= 80
		results.append(StandardizedEntity(
			text=ent.text,
			type=ent.type,
			canonical_id=canonical_id or '',
			score=score,
			manual_review_flag=manual_review_flag
		))
	return {"results": results}
