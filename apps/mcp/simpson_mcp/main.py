"""MCP Server main entrypoint exposing resources and tools."""

from mcp.server.fastmcp import FastMCP
from simpson_common import configure_logging, get_logger, get_settings
from simpson_domain import SystemStatusResult
from simpson_persistence import check_db_health

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger(__name__)

mcp_server = FastMCP("Simpson Strong-Tie Expert MCP")


@mcp_server.resource("system://status")
async def get_system_status_resource() -> str:
    """Read-only diagnostic resource for system status and health."""
    db_ok = await check_db_health()
    res = SystemStatusResult(
        status="healthy" if db_ok else "degraded",
        version="0.1.0",
        database_connected=db_ok,
        storage_adapter=settings.storage_adapter,
        verified_claim_count=0,
    )
    return res.model_dump_json(indent=2)


@mcp_server.tool()
async def system_diagnostics() -> dict[str, str | bool | int]:
    """Diagnostic tool to inspect MCP server foundation status."""
    db_ok = await check_db_health()
    return {
        "status": "online",
        "database_connected": db_ok,
        "storage_adapter": settings.storage_adapter,
        "verified_claim_count": 0,
    }


def run_server() -> None:
    """Run MCP server over STDIO connection."""
    logger.info("Starting simpson-mcp server over STDIO")
    mcp_server.run()


if __name__ == "__main__":
    run_server()
