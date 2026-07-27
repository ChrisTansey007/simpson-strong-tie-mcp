import pytest
from simpson_worker.main import WorkerProcess


@pytest.mark.asyncio
async def test_worker_lifecycle():
    worker = WorkerProcess()
    await worker.start()
    assert worker.running is True
    await worker.stop()
    assert worker.running is False
