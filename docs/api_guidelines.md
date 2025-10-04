# API Guidelines: suRxit

## General Principles
- Use RESTful endpoints for CRUD, gRPC for high-throughput services
- All endpoints require authentication (JWT or OAuth2)
- Use HTTPS only

## Naming Conventions
- Use kebab-case for URLs: `/api/v1/medical-documents`
- Use camelCase for JSON fields

## Versioning
- Prefix all endpoints with `/api/v1/`

## Error Handling
- Use standard HTTP status codes
- Return error objects: `{ "error": "message", "code": 400 }`

## Rate Limiting
- Enforce per-user and per-IP rate limits

## Example
```json
{
  "documentId": "12345",
  "entities": [
    { "type": "Diagnosis", "value": "Diabetes" }
  ]
}
```
