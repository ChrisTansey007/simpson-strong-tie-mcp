"""Ingestion stage abstractions and contracts."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class IngestionJob(BaseModel):
    """Payload definition for PostgreSQL leased job queue."""

    id: str
    source_key: str
    document_path: str
    idempotency_key: str
    stage: str = "REGISTER"
    status: str = "PENDING"
    attempt_count: int = 0
    max_attempts: int = 3
    payload: dict[str, Any] = Field(default_factory=dict)


class IngestionPipelineStage(ABC):
    """Base abstract stage for document processing pipeline."""

    @abstractmethod
    async def process(self, job: IngestionJob) -> IngestionJob:
        """Process job and return updated job payload."""
        pass
