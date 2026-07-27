# Decomposed Build Plan & Task Tracker

> Controlling task execution matrix for **Simpson Strong-Tie Expert MCP**.

---

## Task Execution Matrix

### Phase 1: Repository Foundation (SETUP)

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-001` | Scaffold repository structure & root configurations | **COMPLETE** | None | `make verify` |
| `TASK-002` | Create core domain & common packages (`simpson-domain`, `simpson-common`) | **COMPLETE** | `TASK-001` | `uv run pytest` |
| `TASK-003` | Create object storage abstraction & filesystem adapter (`simpson-storage`) | **COMPLETE** | `TASK-002` | `uv run pytest` |
| `TASK-004` | Create database persistence layer & initial migration (`simpson-persistence`, Alembic 0001) | **COMPLETE** | `TASK-002` | `uv run pytest` |
| `TASK-005` | Scaffold runnable applications (`simpson-api`, `simpson-mcp`, `simpson-worker`, `admin-web`) | **COMPLETE** | `TASK-004` | `make verify` |

#### TASK-001 Completion Evidence:
- Root files created: `pyproject.toml`, `package.json`, `docker-compose.yml`, `Makefile`, `AGENTS.md`, `README.md`, `LICENSE.md`, `SECURITY.md`, `CONTRIBUTING.md`.
- `docs/SIMPSON_MCP_TECHNICAL_BUILD_PLAN.md` copied from artifact package.

#### TASK-002 Completion Evidence:
- Packages `simpson-domain` and `simpson-common` created with type definitions, enums, structured logging, and error hierarchy.

#### TASK-003 Completion Evidence:
- `simpson-storage` created with SHA-256 calculator and immutable object key generator.

#### TASK-004 Completion Evidence:
- `simpson-persistence` created with SQLAlchemy async engine, session factory, system metadata table, and Alembic `0001_init_foundation` migration.

#### TASK-005 Completion Evidence:
- `simpson-api` (FastAPI `/health`, `/ready`), `simpson-mcp` (MCP server `system_status`), `simpson-worker` (async queue process), and `admin-web` (React UI status dashboard) created.

---

### Phase 2: Ingestion Pipeline & Parser Engine

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-010` | Implement source registration & manifest parser | **NEXT READY** | `TASK-005` | `uv run pytest` |
| `TASK-011` | Implement Docling & PyMuPDF document parser pipeline | IN_PROGRESS | `TASK-010` | `uv run pytest` |
| `TASK-012` | Implement Simpson table & footnote extraction parsers | NOT_STARTED | `TASK-011` | `uv run pytest` |
| `TASK-013` | Implement candidate claim generator & revision diffing | NOT_STARTED | `TASK-012` | `uv run pytest` |

---

### Phase 3: Hybrid Retrieval Engine

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-020` | Implement product model exact & `pg_trgm` fuzzy resolver | NOT_STARTED | `TASK-005` | `uv run pytest` |
| `TASK-021` | Implement `pgvector` semantic embedding search & RRF rank fusion | NOT_STARTED | `TASK-020` | `uv run pytest` |

---

### Phase 4: Deterministic Engineering Services

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-030` | Implement ASD/LRFD connector selection service | **COMPLETE** | `TASK-005` | `uv run pytest` |
| `TASK-031` | Implement fastener schedule & substitution verification rules | **COMPLETE** | `TASK-030` | `uv run pytest` |
| `TASK-032` | Implement coastal corrosion & treated-wood coating suitability service | **COMPLETE** | `TASK-030` | `uv run pytest` |

---

### Phase 5: MCP Server & Admin Verification UI

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-040` | Implement MCP Resources (`products://`, `claims://`, `documents://`) | NOT_STARTED | `TASK-032` | `uv run pytest` |
| `TASK-041` | Implement MCP Engineering Tools (`select_connector`, `check_substitution`) | NOT_STARTED | `TASK-040` | `uv run pytest` |
| `TASK-042` | Implement Admin Web claim verification & PDF evidence crop viewer | NOT_STARTED | `TASK-041` | `npm test` |

---

### Phase 6: Adversarial Safety Test Suite

| Task ID | Task Description | Status | Dependencies | Verification Command |
|---|---|---|---|---|
| `TASK-050` | Build adversarial test suite (generic screw block, coastal corrosion block) | NOT_STARTED | `TASK-041` | `uv run pytest` |
