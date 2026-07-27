# Model Context Protocol (MCP) Contract

## SDK & Versioning
- SDK: Official MCP Python SDK (`mcp>=1.27,<2`)
- Protocol: STDIO (initial foundation) & Streamable HTTP (future phase)

## Exposed Resources
- `system://status`: Diagnostic system health & claim counts.
- `products://{model_number}`: Product specifications & published load tables.
- `claims://{claim_id}`: Verified source claims and bounding box evidence.

## Exposed Tools
- `system_diagnostics`: Foundations status check tool.
- `select_connector`: Deterministic connector selection given loads & wood species.
- `check_fastener_substitution`: Fastener schedule substitution verification.
- `check_corrosion_compatibility`: Environmental finish suitability check.
