"""Provenance and evidence models."""

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field
from simpson_domain.enums import VerificationStatus


class BoundingBox(BaseModel):
    """Bounding box coordinates on a source page: [x0, y0, x1, y1]."""

    x0: float
    y0: float
    x1: float
    y1: float


class Citation(BaseModel):
    """Atomic citation linking a claim directly to source document location."""

    id: str
    document_revision_id: str
    page_number: int
    section_heading: str | None = None
    table_identifier: str | None = None
    row_label: str | None = None
    column_label: str | None = None
    footnote_ids: list[str] = Field(default_factory=list)
    bounding_box: BoundingBox | None = None
    supporting_excerpt: str | None = None
    evidence_crop_object_key: str | None = None


class SourceClaim(BaseModel):
    """Structured atomic evidence claim extracted from technical literature."""

    id: str
    claim_type: str
    subject_type: str
    subject_id: str
    predicate: str
    value_decimal: Decimal | None = None
    unit: str | None = None
    conditions: dict[str, Any] = Field(default_factory=dict)
    citation_id: str
    verification_status: VerificationStatus = VerificationStatus.HUMAN_VERIFIED
    source_hash: str
