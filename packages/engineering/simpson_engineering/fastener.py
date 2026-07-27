"""Fastener schedule and substitution rules."""

from simpson_domain.enums import FastenerType


class FastenerService:
    """Fastener verification and approved substitution check service."""

    def check_substitution(
        self, original: FastenerType, proposed: FastenerType
    ) -> tuple[bool, str]:
        """Check if proposed fastener is an approved substitution for original fastener."""
        if proposed == FastenerType.GENERIC_DECK_SCREW:
            return (
                False,
                "Generic deck screws are PROHIBITED for structural connector installation.",
            )

        if original == FastenerType.NAIL_COMMON_10D and proposed == FastenerType.SCREW_SD9:
            return (
                True,
                "Strong-Drive SD9 screw is an approved 1-to-1 replacement for 10d common nail.",
            )

        if original == FastenerType.NAIL_COMMON_16D and proposed == FastenerType.SCREW_SD10:
            return (
                True,
                "Strong-Drive SD10 screw is an approved 1-to-1 replacement for 16d common nail.",
            )

        if original == proposed:
            return True, "Fastener matches original specified schedule."

        return (
            False,
            f"Proposed fastener '{proposed.value}' is not a pre-approved substitution for '{original.value}'.",
        )
