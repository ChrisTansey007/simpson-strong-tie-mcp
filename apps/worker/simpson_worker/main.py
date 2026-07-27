"""Background job queue worker loop entrypoint."""

import asyncio
import sys
import uuid
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any

from simpson_common import configure_logging, get_logger, get_settings
from simpson_persistence import check_db_health
from simpson_persistence.db import async_session_factory
from simpson_persistence.models import LeasedJobORM
from sqlalchemy import select

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger("simpson_worker")

PIPELINE_STAGES = ["REGISTER", "HASH", "PARSE", "EXTRACT", "ACTIVATE"]


class WorkerProcess:
    """Asynchronous background worker manager."""

    def __init__(self, worker_id: str | None = None) -> None:
        self.running = False
        self.worker_id = worker_id or f"worker-{uuid.uuid4()}"
        self.poll_interval = 2.0
        self.lease_duration = timedelta(minutes=5)
        self.task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start worker job polling loop."""
        self.running = True
        logger.info(f"Background worker {self.worker_id} process initializing")

        db_ok = await check_db_health()
        if not db_ok:
            logger.warning("Database unavailable, standing by...")
        else:
            logger.info("Worker database connectivity verified")

        logger.info("Worker polling loop ready")
        self.task = asyncio.create_task(self._loop())

    async def _loop(self) -> None:
        while self.running:
            try:
                processed = await self.poll_and_process()
                if not processed:
                    await asyncio.sleep(self.poll_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                await asyncio.sleep(self.poll_interval)

    async def poll_and_process(self) -> bool:
        """Poll for a job, lease it, and process it."""
        now = datetime.now(UTC)
        job_id = None
        current_stage = "REGISTER"

        async with async_session_factory() as session:
            stmt = (
                select(LeasedJobORM)
                .where(LeasedJobORM.status == "PENDING")
                .where(LeasedJobORM.available_at <= now)
                .where((LeasedJobORM.leased_until.is_(None)) | (LeasedJobORM.leased_until <= now))
                .order_by(LeasedJobORM.priority.desc(), LeasedJobORM.created_at.asc())
                .limit(1)
                .with_for_update(skip_locked=True)
            )

            result = await session.execute(stmt)
            job = result.scalar_one_or_none()

            if not job:
                return False

            job.leased_by = self.worker_id
            job.leased_until = now + self.lease_duration
            job.status = "PROCESSING"
            job.attempt_count += 1

            job_id = job.id
            payload = job.payload_json
            current_stage = payload.get("stage", "REGISTER")

            await session.commit()

        renew_task = asyncio.create_task(self._renew_lease(job_id))
        success = False
        next_stage = None
        error_msg = None

        try:
            logger.info(f"Processing job {job_id} at stage {current_stage}")

            # Simulate job processing (or delegate to actual pipeline logic)
            await self._process_job(job_id, current_stage, payload)

            if current_stage in PIPELINE_STAGES:
                current_idx = PIPELINE_STAGES.index(current_stage)
                if current_idx < len(PIPELINE_STAGES) - 1:
                    next_stage = PIPELINE_STAGES[current_idx + 1]
                else:
                    next_stage = "COMPLETED"
            else:
                next_stage = "COMPLETED"

            success = True
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Job {job_id} failed: {e}")
        finally:
            renew_task.cancel()
            with suppress(asyncio.CancelledError):
                await renew_task

        async with async_session_factory() as session:
            stmt = select(LeasedJobORM).where(LeasedJobORM.id == job_id).with_for_update()
            result = await session.execute(stmt)
            job = result.scalar_one_or_none()
            if job:
                job.leased_by = None
                job.leased_until = None

                if success:
                    job.last_error = None
                    if next_stage == "COMPLETED":
                        job.status = "COMPLETED"
                    else:
                        job.status = "PENDING"
                        payload = dict(job.payload_json)
                        payload["stage"] = next_stage
                        job.payload_json = payload
                        job.attempt_count = 0
                else:
                    job.last_error = error_msg
                    if job.attempt_count >= job.max_attempts:
                        job.status = "FAILED"
                    else:
                        job.status = "PENDING"
                        # Exponential backoff retry logic
                        delay_seconds = 2**job.attempt_count
                        job.available_at = datetime.now(UTC) + timedelta(seconds=delay_seconds)

                await session.commit()

        return True

    async def _process_job(self, job_id: str, stage: str, payload: dict[str, Any]) -> None:
        """Override or delegate to real processor."""
        if payload.get("force_fail"):
            raise ValueError("Simulated failure")
        await asyncio.sleep(0.01)

    async def _renew_lease(self, job_id: str) -> None:
        """Background task to renew lease periodically."""
        try:
            while True:
                await asyncio.sleep(self.lease_duration.total_seconds() / 2)
                async with async_session_factory() as session:
                    stmt = select(LeasedJobORM).where(LeasedJobORM.id == job_id).with_for_update()
                    result = await session.execute(stmt)
                    job = result.scalar_one_or_none()
                    if job and job.leased_by == self.worker_id:
                        job.leased_until = datetime.now(UTC) + self.lease_duration
                        await session.commit()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Failed to renew lease for job {job_id}: {e}")

    async def stop(self) -> None:
        """Shut down worker cleanly."""
        logger.info("Background worker process stopping")
        self.running = False
        if self.task:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                await self.task


async def async_main() -> None:
    worker = WorkerProcess()
    await worker.start()
    # Let it run for a moment if started manually, just for demo
    await asyncio.sleep(0.5)
    await worker.stop()


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Worker process terminated by user")
        sys.exit(0)


run_worker = main


if __name__ == "__main__":
    main()
