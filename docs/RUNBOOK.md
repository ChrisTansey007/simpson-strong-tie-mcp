# Operational Runbook

## Local Operations

### Environment Bootstrap
```bash
make bootstrap
```

### Database Migration
```bash
make migrate
```

### Application Entrypoints
- Admin API: `make api` (port 8000)
- MCP Server: `make mcp` (STDIO)
- Worker: `make worker`
- Admin Web: `make web` (port 5173)

### Full Quality Gate Execution
```bash
make verify
```
