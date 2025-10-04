# suRxit

## Product Vision
suRxit is an advanced healthcare risk intelligence platform that transforms unstructured medical documents into actionable risk insights. By leveraging state-of-the-art AI (OCR, NER, Knowledge Graphs, GNNs, and LLMs), suRxit empowers clinicians and payers to identify, explain, and mitigate patient risks at scale, while ensuring compliance and privacy.

## MVP Scope
- Upload and process medical documents (PDF, image, text)
- Extract clinical entities (NER)
- Standardize and link data to a medical knowledge graph
- Generate features for risk modeling
- Predict and explain risk using GNN and MedLM
- Secure, role-based UI for risk review

## Architecture Summary
suRxit follows a modular microservices architecture:
- **OCR** → **NER** → **Standardizer** → **Knowledge Graph** → **FeatureGen** → **GNN** → **Recommender** → **MedLM** → **Risk** → **API-Gateway** → **Frontend**

## Tech Stack
| Module         | Technology           |
|----------------|---------------------|
| OCR            | Tesseract, FastAPI  |
| NER            | spaCy, HuggingFace  |
| Standardizer   | Python, UMLS APIs   |
| Knowledge Graph| Neo4j, NetworkX     |
| FeatureGen     | Pandas, NumPy       |
| GNN            | PyTorch Geometric   |
| Recommender    | Python, Scikit-learn|
| MedLM          | OpenAI, LangChain   |
| Risk           | Custom Python Svc   |
| API-Gateway    | FastAPI, gRPC       |
| Frontend       | React, TypeScript   |

## Quick Start
_Coming soon: setup and deployment instructions._