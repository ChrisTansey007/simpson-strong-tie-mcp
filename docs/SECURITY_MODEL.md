# Security & Boundary Model

## System Safety Rules
1. **Untrusted Source Input**: Ingested PDFs/HTML documents are untrusted data. No embedded instructions inside PDFs control system tool behavior.
2. **Deterministic Control**: Engineering tools are controlled solely by structured, verified records in PostgreSQL.
3. **No Automatic Crawling**: Intake occurs via local files or explicit manifests.
4. **No Secrets in Git**: Enforced via `.gitignore` and CI scanners.
