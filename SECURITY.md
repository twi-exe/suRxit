# Security Policy# Security Policy



## PHI Handling## PHI Handling

- All Protected Health Information (PHI) must be encrypted in transit and at rest.- All Protected Health Information (PHI) must be encrypted at rest and in transit.

- Never log or expose PHI in plaintext.- Access to PHI is restricted by Role-Based Access Control (RBAC).



## HTTPS/TLS## HTTPS/TLS

- All APIs and UI endpoints must enforce HTTPS/TLS 1.2+.- All external and internal service communication must use HTTPS/TLS 1.2+.



## Encrypted Storage## Encrypted Storage

- Use AES-256 or stronger encryption for all sensitive data.- Use industry-standard encryption (AES-256) for all sensitive data.

- Keys must be managed via a secure vault (e.g., HashiCorp Vault).- Keys must be managed securely (e.g., HashiCorp Vault).



## RBAC## RBAC

- Enforce Role-Based Access Control for all user and service actions.- Define roles for clinicians, admins, and service accounts.

- Principle of least privilege applies to all roles.- Enforce least-privilege access throughout the stack.

