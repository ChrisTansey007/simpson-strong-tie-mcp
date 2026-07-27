# ADR 0001: Modular Monolith Architecture

## Context
Simpson Strong-Tie Expert MCP requires strong internal boundaries between domain models, persistence, retrieval engines, document ingestion, and external protocol adapters (FastAPI, MCP). Premature microservices add deployment complexity without engineering benefit.

## Decision
Build as a single modular monolith repository (`simpson-strong-tie-mcp`) containing isolated packages (`packages/*`) and multiple process entrypoints (`apps/*`).

## Consequences
- Single codebase and single build pipeline.
- Explicit package import boundaries enforced via Pyright and Ruff.
- Easy transition to microservices later if scaling demands require it.
