# suRxit Architecture# System Architecture



suRxit is built as a set of loosely coupled microservices, each responsible for a distinct stage in the risk intelligence pipeline. This modularity enables scalability, maintainability, and rapid iteration.MedKG-Rx is built as a set of loosely coupled microservices, each responsible for a distinct stage in the clinical document-to-risk pipeline. The architecture ensures scalability, modularity, and compliance with healthcare data standards.



## Microservices Flow## Microservice Flow

1. **OCR**: Converts scanned documents/images to text.1. **OCR**: Converts scanned documents to machine-readable text.

2. **NER**: Extracts clinical entities from text.2. **NER**: Extracts medical entities from text.

3. **Standardizer**: Maps entities to standard vocabularies (UMLS, SNOMED).3. **Standardizer**: Maps entities to standard vocabularies (e.g., SNOMED, RxNorm).

4. **Knowledge Graph**: Links entities and relationships.4. **KG**: Stores and queries medical relationships in a knowledge graph.

5. **FeatureGen**: Generates features for downstream models.5. **FeatureGen**: Generates patient-specific features for risk modeling.

6. **GNN**: Predicts risk using graph neural networks.6. **GNN**: Applies graph neural networks for risk prediction.

7. **Recommender**: Suggests interventions or next steps.7. **Recommender**: Suggests interventions based on risk.

8. **MedLM**: Provides LLM-based explanations.8. **MedLM**: Provides explanations and Q&A using medical LLMs.

9. **Risk**: Aggregates and explains risk scores.9. **Risk**: Aggregates and scores risk.

10. **API-Gateway**: Orchestrates requests and enforces security.10. **API-Gateway**: Orchestrates service calls and enforces security.

11. **Frontend**: UI for clinicians and payers.11. **Frontend**: Presents results and explanations to clinicians.



## Diagram## Architecture Diagram

```mermaid```mermaid

flowchart LRflowchart LR

    A[OCR] --> B[NER]    A[OCR] --> B[NER]

    B --> C[Standardizer]    B --> C[Standardizer]

    C --> D[Knowledge Graph]    C --> D[KG]

    D --> E[FeatureGen]    D --> E[FeatureGen]

    E --> F[GNN]    E --> F[GNN]

    F --> G[Recommender]    F --> G[Recommender]

    G --> H[MedLM]    G --> H[MedLM]

    H --> I[Risk]    H --> I[Risk]

    I --> J[API-Gateway]    I --> J[API-Gateway]

    J --> K[Frontend]    J --> K[Frontend]

``````

