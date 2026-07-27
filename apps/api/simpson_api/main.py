"""FastAPI Admin API main entrypoint."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simpson_common import configure_logging, get_logger, get_settings
from simpson_persistence import check_db_health

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger(__name__)

app = FastAPI(
    title="Simpson Strong-Tie Expert MCP Admin API",
    version="0.1.0",
    description="Admin API for ingestion monitoring, human verification, and diagnostic search",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Basic service health check."""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/ready")
async def readiness_check() -> dict[str, str | bool]:
    """Readiness probe checking database connectivity."""
    db_ok = await check_db_health()
    return {
        "status": "ready" if db_ok else "not_ready",
        "database_connected": db_ok,
    }


def run_server() -> None:
    """Run API server via Uvicorn console script entrypoint."""
    logger.info("Starting simpson-api server", port=settings.api_port)
    uvicorn.run(
        "simpson_api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    run_server()
