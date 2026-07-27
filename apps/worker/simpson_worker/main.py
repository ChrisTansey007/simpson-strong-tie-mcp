"""Background job queue worker loop entrypoint."""

import asyncio
import sys

from simpson_common import configure_logging, get_logger, get_settings
from simpson_persistence import check_db_health

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger(__name__)


class WorkerProcess:
    """Asynchronous background worker manager."""

    def __init__(self) -> None:
        self.running = False

    async def start(self) -> None:
        """Start worker job polling loop."""
        self.running = True
        logger.info("Background worker process initializing")

        db_ok = await check_db_health()
        if not db_ok:
            logger.warning("Worker database connectivity check failed")
        else:
            logger.info("Worker database connectivity verified")

        logger.info("Worker polling loop ready")

    async def stop(self) -> None:
        """Shut down worker cleanly."""
        logger.info("Worker process shutting down")
        self.running = False


async def async_main() -> None:
    worker = WorkerProcess()
    await worker.start()
    # In one-shot / test run, perform clean check and shutdown
    await asyncio.sleep(0.5)
    await worker.stop()


def run_worker() -> None:
    """Console script entrypoint for simpson-worker."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Worker interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    run_worker()
