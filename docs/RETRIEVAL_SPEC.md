# Retrieval Engine Specification

## Retrieval Cascade Order
1. **Exact Identifier Matching**: Resolve product model numbers and aliases (`H1A`, `LUS28`).
2. **Structured Query Filtering**: Filter by category, design method, wood species, and verification status.
3. **Lexical Full-Text Search**: PostgreSQL `pg_trgm` fuzzy & full-text search.
4. **Vector Semantic Search**: `pgvector` similarity search across chunk embeddings.
5. **Reciprocal Rank Fusion (RRF)**: Blend lexical and vector candidate lists.
