"""Domain models and typed data objects."""

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from simpson_domain.enums import (
    AnswerClassification,
    CoatingType,
    DesignMethod,
    EnvironmentClassification,
    FastenerType,
    LoadDirection,
    VerificationStatus,
    WoodSpeciesGroup,
)


class ProductAlias(BaseModel):
    """Product model number alias or typo variation."""

    alias: str
    target_model: str
    is_canonical: bool = False


class ProductVariant(BaseModel):
    """Specific product variant (gauge, coating, dimension)."""

    id: str
    product_id: str
    model_number: str
    gauge: int | None = None
    coating: CoatingType = CoatingType.STANDARD_GALVANIZED
    dimensions_in: str | None = None


class Product(BaseModel):
    """Core product line definition."""

    id: str
    model_number: str
    series_name: str
    description: str
    category: str
    variants: list[ProductVariant] = Field(default_factory=list)


class FastenerSchedule(BaseModel):
    """Schedule of required fasteners for a connector installation."""

    id: str
    fastener_type: FastenerType
    quantity: int
    header_qty: int | None = None
    joist_qty: int | None = None


class PublishedCapacity(BaseModel):
    """Manufacturer published load capacity claim."""

    id: str
    product_variant_id: str
    design_method: DesignMethod
    load_direction: LoadDirection
    wood_species_group: WoodSpeciesGroup
    capacity_lbf: Decimal
    fastener_schedule_id: str
    citation_id: str
    verification_status: VerificationStatus = VerificationStatus.HUMAN_VERIFIED


class ConnectionCheckRequest(BaseModel):
    """Input payload for deterministic connector selection/checking."""

    model_number: str
    required_uplift_lbf: Decimal | None = None
    required_download_lbf: Decimal | None = None
    required_lateral_lbf: Decimal | None = None
    design_method: DesignMethod = DesignMethod.ASD
    wood_species_group: WoodSpeciesGroup = WoodSpeciesGroup.DF_SP
    environment: EnvironmentClassification = EnvironmentClassification.DRY_INTERIOR
    fastener_override: FastenerType | None = None


class ConnectionCheckResult(BaseModel):
    """Result payload from deterministic connector checking."""

    is_compliant: bool
    classification: AnswerClassification
    model_number: str
    allowable_capacity_lbf: Decimal | None = None
    required_load_lbf: Decimal | None = None
    unity_ratio: Decimal | None = None
    fastener_schedule: str | None = None
    citations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    elimination_reasons: list[str] = Field(default_factory=list)


class SystemStatusResult(BaseModel):
    """Diagnostic system health and foundation status result."""

    status: str
    version: str
    database_connected: bool
    storage_adapter: str
    verified_claim_count: int
    details: dict[str, Any] = Field(default_factory=dict)
