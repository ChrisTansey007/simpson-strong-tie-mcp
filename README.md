# Simpson Strong-Tie Expert MCP

An independent, versioned engineering knowledge and Model Context Protocol (MCP) server for Simpson Strong-Tie products, fastener schedules, continuous load paths, and structural connection verification.

---

## Overview

Simpson Strong-Tie Expert MCP is a high-reliability engineering knowledge server built for AI agents and human structural engineers. It combines:
- **Immutable Source Evidence**: Hashed PDF and document storage with bounding-box citations down to catalog, page, table, row, and footnote.
- **Deterministic Domain Services**: Typed ASD/LRFD capacity selection, fastener substitution, member fit, and treated-wood corrosion compatibility checks.
- **Hybrid Retrieval**: Identifier exact matching, PostgreSQL `pg_trgm` lexical search, and `pgvector` semantic retrieval with Reciprocal Rank Fusion (RRF).
- **Human Verification Gate**: Admin review interface ensuring extracted engineering data is human-verified before powering critical MCP tools.
- **MCP Standard Interface**: Exposing typed resources, tools, and prompts for AI assistants via STDIO and HTTP endpoints.

---

## Quick Start

### Prerequisites
- Python 3.12+
- `uv` package manager (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Node.js 20+ & `npm`
- Docker & Docker Compose (for PostgreSQL 18 + pgvector)

### Bootstrap Environment
```bash
make bootstrap
```

### Run Applications Locally
```bash
# Start PostgreSQL & infrastructure dependencies
docker compose up -d postgres minio

# Run Database Migrations
make migrate

# Start FastAPI Admin API (port 8000)
make api

# Start MCP Server (STDIO mode)
make mcp

# Start Background Worker
make worker

# Start Admin Verification Web UI
make web
```

---

## Project Architecture

```text
simpson-strong-tie-mcp/
├── apps/
│   ├── api/          # FastAPI administrative API & health checks
│   ├── mcp/          # Model Context Protocol (MCP) server
│   ├── worker/       # Asynchronous document & indexing job worker
│   └── admin-web/    # React + TypeScript verification UI
├── packages/
│   ├── common/       # Settings, logging, and shared exceptions
│   ├── domain/       # Pure DTOs, domain models, enums, value objects
│   ├── persistence/  # SQLAlchemy models, db session, repositories
│   ├── provenance/   # SourceClaim, Citation, verification status models
│   ├── ingestion/    # Document parsers (Docling, PyMuPDF, Simpson tables)
│   ├── retrieval/    # Exact, lexical, vector, and RRF hybrid search
│   ├── engineering/  # Load, fastener, corrosion, member-fit services
│   ├── storage/      # Object storage abstraction & SHA-256 hashers
│   └── testing/      # Fixtures & synthetic document generators
├── migrations/       # Alembic database migrations
└── docs/             # Technical architecture specs & ADRs
```

---

## Verification & Quality Gate

Run the full local quality gate:
```bash
make verify
```

---

## License

Internal Owner Review Placeholder — See [LICENSE.md](file:///c:/Users/theca/sub-intel/simpson-strong-tie-mcp/LICENSE.md).
