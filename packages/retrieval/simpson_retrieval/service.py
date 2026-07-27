"""Retrieval service query DTOs and abstract service interface."""

from abc import ABC, abstractmethod

from pydantic import BaseModel
from simpson_domain.enums import VerificationStatus
from simpson_provenance.models import Citation


class RetrievalQuery(BaseModel):
    """Hybrid retrieval query payload."""

    text_query: str
    model_number: str | None = None
    category: str | None = None
    verification_status: VerificationStatus = VerificationStatus.HUMAN_VERIFIED
    limit: int = 10


class RetrievalResult(BaseModel):
    """Retrieval query result item."""

    score: float
    retrieval_method: str  # EXACT, LEXICAL, VECTOR, HYBRID_RRF
    subject_id: str
    title: str
    content_excerpt: str
    citation: Citation | None = None


class RetrievalService(ABC):
    """Abstract retrieval engine interface."""

    @abstractmethod
    async def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        """Execute hybrid search for given query."""
        pass
