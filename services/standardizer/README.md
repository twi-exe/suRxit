# Standardizer Service

## Overview
This service provides an API to map extracted entity names to canonical IDs using fuzzy string matching on manual CSVs.

## Endpoints
- `POST /standardize`: Map entity names to canonical IDs using rapidfuzz and data/manual CSVs.

## Environment Variables
- None required by default.

## Running Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing
```bash
pytest test_standardizer.py
```
