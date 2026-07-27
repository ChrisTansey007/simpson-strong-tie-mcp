# ADR 0004: Official MCP Python SDK v1 Constraint

## Context
The official Model Context Protocol Python SDK stable line is v1 (`mcp>=1.27,<2`).

## Decision
Pin `mcp>=1.27,<2` in `pyproject.toml` and isolate MCP server adapters inside `apps/mcp/` so that a future migration to v2 can be done without modifying domain business logic.

## Consequences
- Stable protocol compatibility with current MCP host tools.
- Clean isolation between domain logic and protocol transport layer.
