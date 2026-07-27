# ADR 0005: PostgreSQL-Backed Leased Job Queue and Outbox

## Context
Document parsing and indexing jobs require asynchronous queue processing with retries and status tracking. Adding Redis and Celery introduces additional operational overhead.

## Decision
Implement job queuing via a `leased_jobs` PostgreSQL table using `FOR UPDATE SKIP LOCKED` semantics and transactional outbox.

## Consequences
- Zero additional queue infrastructure required.
- Transactional consistency between data updates and job scheduling.
