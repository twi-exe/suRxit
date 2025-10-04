# Project Plan: suRxit

## Stakeholder List
- Product Owner: Dr. A. Smith (Healthcare Domain Expert)
- Tech Lead: ParmarDarshan29
- Compliance Officer: J. Lee
- DevOps: S. Patel
- Clinical Advisors: Dr. R. Gupta, Dr. M. Chen
- End Users: Clinicians, Payers

## Roles & Responsibilities
- Product Owner: Define vision, prioritize features
- Tech Lead: Architecture, code quality, technical decisions
- Compliance Officer: Ensure GDPR/HIPAA, audit trails
- DevOps: CI/CD, infrastructure, monitoring
- Clinical Advisors: Validate clinical accuracy
- Developers: Implement features, write tests

## Compliance Checklist
- [ ] Data encryption (at rest, in transit)
- [ ] PHI redaction in logs
- [ ] Consent management
- [ ] Audit logging
- [ ] Role-based access control
- [ ] Regular security reviews

## MVP Feature List
- Document upload (PDF, image, text)
- OCR pipeline
- NER extraction
- Entity standardization
- Knowledge graph linking
- Feature generation
- GNN-based risk prediction
- MedLM explanations
- Risk dashboard UI

## Non-Functional Requirements
- **Scalability:** Handle 10k docs/day, auto-scale services
- **Latency SLO:** <2s per document (end-to-end)
- **Security:** End-to-end encryption, RBAC, regular pen-testing

## Risk Register & Mitigations
| Risk                        | Impact | Likelihood | Mitigation                        |
|-----------------------------|--------|------------|-----------------------------------|
| PHI data breach             | High   | Medium     | Encryption, access controls       |
| Model bias                  | High   | Medium     | Diverse training data, audits     |
| Regulatory non-compliance   | High   | Low        | Regular reviews, legal counsel    |
| Service downtime            | Med    | Medium     | Redundant infra, monitoring       |
| Data loss                   | High   | Low        | Backups, disaster recovery        |
