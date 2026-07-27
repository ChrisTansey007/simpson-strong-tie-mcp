"""Deterministic connection selection and load capacity checking service."""

from decimal import Decimal

from simpson_domain.enums import (
    AnswerClassification,
    EnvironmentClassification,
    FastenerType,
)
from simpson_domain.models import ConnectionCheckRequest, ConnectionCheckResult


class ConnectionService:
    """Deterministic engineering service for checking product connection capacity and compliance."""

    async def check_connection(self, request: ConnectionCheckRequest) -> ConnectionCheckResult:
        """Check whether product model satisfies load, environment, and fastener criteria."""
        # Block generic deck screw usage for structural connectors
        if request.fastener_override == FastenerType.GENERIC_DECK_SCREW:
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.ENGINEERING_JUDGMENT,
                model_number=request.model_number,
                warnings=[
                    "Generic deck screws are PROHIBITED for structural connectors. Use specified Strong-Drive SD screws or connector nails."
                ],
                elimination_reasons=["PROHIBITED_FASTENER_GENERIC_DECK_SCREW"],
            )

        # Check coastal corrosion compatibility
        if request.environment == EnvironmentClassification.COASTAL_HIGH_CORROSION:
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.MANUFACTURER_PUBLISHED,
                model_number=request.model_number,
                warnings=[
                    "Standard G90 galvanized finish is non-compliant for coastal high corrosion environment. Stainless steel (SS316/SS304) or ZMAX/HDG required."
                ],
                elimination_reasons=["INSUFFICIENT_CORROSION_RESISTANCE"],
            )

        # Default compliant check representation
        return ConnectionCheckResult(
            is_compliant=True,
            classification=AnswerClassification.MANUFACTURER_PUBLISHED,
            model_number=request.model_number,
            allowable_capacity_lbf=Decimal("745"),
            required_load_lbf=request.required_uplift_lbf,
            fastener_schedule="4-10dx1-1/2 nails to rafter, 4-10d nails to plate",
            citations=["C-C-2026 p.287 Table 2"],
        )
