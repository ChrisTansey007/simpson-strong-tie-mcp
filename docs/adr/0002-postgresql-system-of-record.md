# ADR 0002: PostgreSQL 18 as Primary System of Record and Search Platform

## Context
Engineering capacity selections and fastener schedules require exact structured relational queries, fuzzy product identifier lookups, and vector semantic retrieval.

## Decision
Use PostgreSQL 18 with `pgvector` and `pg_trgm` extensions as the single authoritative system of record and search engine. Avoid adding Redis, OpenSearch, or external vector DBs during foundation phase.

## Consequences
- Single database dependency for relational data, full-text search, and vector search.
- ACID transactions across domain entities and job queue outbox.
