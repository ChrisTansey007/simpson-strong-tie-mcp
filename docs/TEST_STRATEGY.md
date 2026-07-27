# Test Strategy & Quality Gate

## Quality Gate Suite
1. **Unit Tests**: Domain entities, SHA-256 hasher, engineering rules.
2. **Integration Tests**: Database persistence, Alembic migrations, PostgreSQL `pgvector` & `pg_trgm`.
3. **Contract Tests**: API health endpoints, MCP resources & diagnostic tools.
4. **Adversarial Safety Tests**: Prohibited fastener substitution (generic deck screws), coastal corrosion suitability enforcement, unverified claim exclusion.
5. **Frontend Tests**: React status component rendering & API mock tests.

## Commands
```bash
make verify
```
