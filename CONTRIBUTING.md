# Contributing to Simpson Strong-Tie Expert MCP

Thank you for contributing to Simpson Strong-Tie Expert MCP!

## Development Workflow

### Setup Workspace
Ensure Python 3.12+ and `uv` are installed.

```bash
uv sync --all-packages --dev
npm install
```

### Code Standards
- **Python**: Strict type hints (`pyright`), Ruff formatting & linting.
- **Frontend**: TypeScript strict mode, React 19 standards, ESLint.
- **Architecture**: Modular monolith layout. Keep domain packages completely decoupled from web/API frameworks.

### Running Quality Gate
Before submitting a PR or marking a task as complete:

```bash
make verify
```
Or manually execute:
```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
npm run lint
npm run typecheck
npm test -- --run
docker compose config
```

### Commit Hygiene
- Keep commits focused per task/feature.
- Ensure all tests pass prior to commit.
