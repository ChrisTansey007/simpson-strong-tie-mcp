"""Domain entities, enums, value objects, and typed records."""

from simpson_domain.enums import (
    AnswerClassification,
    CoatingType,
    DesignMethod,
    EnvironmentClassification,
    FastenerType,
    LoadDirection,
    SourceStatus,
    VerificationStatus,
    WoodSpeciesGroup,
)
from simpson_domain.models import (
    ConnectionCheckRequest,
    ConnectionCheckResult,
    FastenerSchedule,
    Product,
    ProductAlias,
    ProductVariant,
    PublishedCapacity,
    SystemStatusResult,
)

__all__ = [
    "SourceStatus",
    "VerificationStatus",
    "AnswerClassification",
    "DesignMethod",
    "LoadDirection",
    "WoodSpeciesGroup",
    "FastenerType",
    "CoatingType",
    "EnvironmentClassification",
    "Product",
    "ProductVariant",
    "ProductAlias",
    "FastenerSchedule",
    "PublishedCapacity",
    "ConnectionCheckRequest",
    "ConnectionCheckResult",
    "SystemStatusResult",
]
