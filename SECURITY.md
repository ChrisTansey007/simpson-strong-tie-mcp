# Security Policy

## Security Model & Boundaries

Simpson Strong-Tie Expert MCP processes technical catalogs, engineering code reports, product draw data, and fastener schedules.

### Security Guarantees:
1. **Untrusted Data Isolation**: All ingested documents (PDFs, HTML, text) are treated strictly as untrusted data. Content parser workers run in isolated processes and never execute embedded instructions or scripts inside PDFs/documents.
2. **Deterministic Service Boundary**: Engineering tools and MCP outputs are driven by verified structured records in PostgreSQL, never by raw unverified LLM output or prompt injection strings.
3. **No Credential Ingestion**: Secrets, API keys, and environment files MUST NOT be committed to Git.
4. **No Automated Crawling**: All source documents are loaded via explicit local intake or verified source manifest files.

## Reporting Vulnerabilities

If you discover a security vulnerability in this project:
- Do not create a public issue.
- Send a detailed security advisory report to the system administrator or repository maintainers.
- Reports will be triaged and addressed within 48 hours.
