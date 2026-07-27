"""Corrosion exposure and coating compatibility rules."""

from simpson_domain.enums import CoatingType, EnvironmentClassification


class CorrosionService:
    """Deterministic check for finish/coating environment suitability."""

    def check_coating_suitability(
        self, coating: CoatingType, environment: EnvironmentClassification
    ) -> tuple[bool, str]:
        """Check if coating finish is suitable for environment."""
        if environment == EnvironmentClassification.COASTAL_HIGH_CORROSION:
            if coating in (CoatingType.STAINLESS_316, CoatingType.STAINLESS_304):
                return True, "Stainless steel is approved for coastal exposure."
            return False, "Standard galvanized finishes are non-compliant in coastal environments."

        if environment == EnvironmentClassification.TREATED_WOOD:
            if coating in (
                CoatingType.ZMAX,
                CoatingType.HDG,
                CoatingType.STAINLESS_304,
                CoatingType.STAINLESS_316,
            ):
                return True, "ZMAX/HDG/Stainless steel approved for pressure-treated wood."
            return (
                False,
                "Standard G90 coating is prohibited in contact with pressure-treated wood.",
            )

        return True, "Finish suitable for interior dry environment."
