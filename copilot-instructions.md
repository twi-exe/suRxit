You are a senior full-stack engineer and MLOps lead. Create a new GitHub repo skeleton for a clinical medication safety product named "suRxit". Use Python + FastAPI, Neo4j for KG, React for frontend. Produce the following in the repo:

1. Top-level directories:
   - services/ocr
   - services/ner
   - services/standardizer
   - services/kg
   - services/featuregen
   - services/gnn
   - services/recommender
   - services/medlm
   - api_gateway
   - frontend
   - infra
   - data/manual
   - tests

2. Create Dockerfiles for Python services and a docker-compose.yml that brings up:
   - Neo4j (dev)
   - Postgres
   - Redis
   - api_gateway (FastAPI stub)
   - frontend (React stub)

3. Add starter code:
   - services/ocr/app.py: FastAPI endpoint POST /ocr/upload that accepts image/pdf, saves file, enqueues a job, returns ingest_id.
   - services/ner/app.py: POST /ner/parse that accepts text returns tokenized entities schema.
   - services/kg/import.py: script to import `data/manual/nodes.csv` and `data/manual/rels.csv` into Neo4j using Bolt driver.
   - api_gateway main service routing to microservices.
   - frontend React app with a simple dashboard page and a form to upload prescription images.

4. Add docs:
   - README.md with architecture diagram, quickstart, environment variables.
   - OpenAPI spec stub at api_gateway/openapi.yaml

5. Add CI:
   - GitHub Actions workflow to lint (flake8), run unit tests, build docker images.

6. Provide instructions for local dev: how to run docker-compose up, example curl to call /ocr/upload, sample test data in data/manual.

Requirements: produce working minimal endpoints (no heavy ML models required now but include TODO markers and tests). Include unit tests for the upload endpoints.

Return final commit-ready file tree and short usage instructions.
