"""Domain enumerations for Simpson Strong-Tie MCP."""

from enum import StrEnum


class SourceStatus(StrEnum):
    """Document/source lifecycle status."""

    CURRENT = "CURRENT"
    SUPERSEDED = "SUPERSEDED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"
    UNKNOWN = "UNKNOWN"


class VerificationStatus(StrEnum):
    """Extraction verification lifecycle status."""

    AUTO_PARSED = "AUTO_PARSED"
    AUTO_PARSED_REVIEW_REQUIRED = "AUTO_PARSED_REVIEW_REQUIRED"
    HUMAN_VERIFIED = "HUMAN_VERIFIED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class AnswerClassification(StrEnum):
    """Classification of output information authority."""

    MANUFACTURER_PUBLISHED = "MANUFACTURER_PUBLISHED"
    SYSTEM_DERIVED = "SYSTEM_DERIVED"
    ENGINEERING_JUDGMENT = "ENGINEERING_JUDGMENT"
    UNVERIFIED = "UNVERIFIED"
    SUPERSEDED_SOURCE = "SUPERSEDED_SOURCE"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"


class DesignMethod(StrEnum):
    """Structural design calculation methodology."""

    ASD = "ASD"
    LRFD = "LRFD"


class LoadDirection(StrEnum):
    """Force vector direction."""

    UPLIFT = "UPLIFT"
    LATERAL_F1 = "LATERAL_F1"
    LATERAL_F2 = "LATERAL_F2"
    DOWNLOAD = "DOWNLOAD"


class WoodSpeciesGroup(StrEnum):
    """Wood species specific gravity group."""

    DF_SP = "DF_SP"  # Douglas Fir-Larch / Southern Pine (G >= 0.50)
    SPF_HF = "SPF_HF"  # Spruce-Pine-Fir / Hem-Fir (G >= 0.42)


class FastenerType(StrEnum):
    """Structural fastener classifications."""

    NAIL_COMMON_10D = "10d_common"
    NAIL_COMMON_16D = "16d_common"
    NAIL_SINKER_10D = "10d_sinker"
    NAIL_SINKER_16D = "16d_sinker"
    SCREW_SD9 = "SD9"
    SCREW_SD10 = "SD10"
    SCREW_SDWS = "SDWS"
    SCREW_SDWH = "SDWH"
    GENERIC_DECK_SCREW = "generic_deck_screw"  # Prohibited for structural connectors


class CoatingType(StrEnum):
    """Protective surface finishes."""

    STANDARD_GALVANIZED = "G90"
    ZMAX = "ZMAX"
    HDG = "HDG"
    STAINLESS_304 = "SS304"
    STAINLESS_316 = "SS316"


class EnvironmentClassification(StrEnum):
    """Corrosion exposure environments."""

    DRY_INTERIOR = "DRY_INTERIOR"
    WET_EXTERIOR = "WET_EXTERIOR"
    COASTAL_HIGH_CORROSION = "COASTAL_HIGH_CORROSION"
    TREATED_WOOD = "TREATED_WOOD"
