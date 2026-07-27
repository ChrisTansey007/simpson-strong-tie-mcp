from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from simpson_worker.main import WorkerProcess


@pytest.mark.asyncio
async def test_worker_lifecycle():
    worker = WorkerProcess()
    with patch("simpson_worker.main.check_db_health", return_value=True):
        await worker.start()
        assert worker.running is True
        await worker.stop()
        assert worker.running is False


@pytest.mark.asyncio
@patch("simpson_worker.main.async_session_factory")
async def test_worker_poll_and_process_success(mock_session_factory):
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_job = MagicMock()
    mock_job.id = "test-job-123"
    mock_job.payload_json = {"stage": "REGISTER"}
    mock_job.attempt_count = 0
    mock_job.max_attempts = 3
    mock_job.leased_by = None
    mock_job.leased_until = None
    mock_job.status = "PENDING"

    mock_result = MagicMock()
    # First call returns a job, second call (in finalizer) returns the same job
    mock_result.scalar_one_or_none.return_value = mock_job
    mock_session.execute.return_value = mock_result

    worker = WorkerProcess()
    processed = await worker.poll_and_process()

    assert processed is True
    assert mock_job.leased_by is None
    assert mock_job.leased_until is None
    assert mock_job.status == "PENDING"
    assert mock_job.payload_json["stage"] == "HASH"
    assert mock_job.attempt_count == 0


@pytest.mark.asyncio
@patch("simpson_worker.main.async_session_factory")
async def test_worker_poll_and_process_completion(mock_session_factory):
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_job = MagicMock()
    mock_job.id = "test-job-456"
    mock_job.payload_json = {"stage": "ACTIVATE"}
    mock_job.attempt_count = 0
    mock_job.max_attempts = 3
    mock_job.leased_by = None
    mock_job.leased_until = None
    mock_job.status = "PENDING"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_job
    mock_session.execute.return_value = mock_result

    worker = WorkerProcess()
    processed = await worker.poll_and_process()

    assert processed is True
    assert mock_job.status == "COMPLETED"


@pytest.mark.asyncio
@patch("simpson_worker.main.async_session_factory")
async def test_worker_poll_and_process_failure_with_backoff(mock_session_factory):
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_job = MagicMock()
    mock_job.id = "test-job-789"
    mock_job.payload_json = {"stage": "PARSE", "force_fail": True}
    mock_job.attempt_count = 1
    mock_job.max_attempts = 3
    mock_job.leased_by = None
    mock_job.leased_until = None
    mock_job.status = "PENDING"
    mock_job.available_at = datetime.now(UTC)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_job
    mock_session.execute.return_value = mock_result

    worker = WorkerProcess()
    processed = await worker.poll_and_process()

    assert processed is True
    assert mock_job.status == "PENDING"
    assert mock_job.attempt_count == 2
    assert mock_job.last_error == "Simulated failure"
    assert mock_job.available_at > datetime.now(UTC)


@pytest.mark.asyncio
@patch("simpson_worker.main.async_session_factory")
async def test_worker_poll_and_process_failure_max_attempts(mock_session_factory):
    mock_session = AsyncMock()
    mock_session_factory.return_value.__aenter__.return_value = mock_session

    mock_job = MagicMock()
    mock_job.id = "test-job-000"
    mock_job.payload_json = {"stage": "EXTRACT", "force_fail": True}
    mock_job.attempt_count = 2  # Will be incremented to 3 before execution
    mock_job.max_attempts = 3
    mock_job.leased_by = None
    mock_job.leased_until = None
    mock_job.status = "PENDING"

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_job
    mock_session.execute.return_value = mock_result

    worker = WorkerProcess()
    processed = await worker.poll_and_process()

    assert processed is True
    assert mock_job.status == "FAILED"
    assert mock_job.attempt_count == 3
    assert mock_job.last_error == "Simulated failure"
