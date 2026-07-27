"""Deterministic connection selection and load capacity checking service."""

from decimal import Decimal

from simpson_domain.enums import (
    AnswerClassification,
    EnvironmentClassification,
    FastenerType,
    LoadDirection,
)
from simpson_domain.models import ConnectionCheckRequest, ConnectionCheckResult
from simpson_persistence import check_db_health
from simpson_persistence.db import async_session_factory
from simpson_persistence.models import ProductVariantORM, PublishedCapacityORM
from sqlalchemy import select


class ConnectionService:
    """Service for validating wood connector selection against structural design requirements."""

    async def check_connection(self, request: ConnectionCheckRequest) -> ConnectionCheckResult:
        """Check connector compliance for given load, wood species, and environment."""
        fastener = getattr(request, "fastener_override", None) or getattr(
            request, "proposed_fastener", None
        )
        if fastener == FastenerType.GENERIC_DECK_SCREW:
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.MANUFACTURER_PUBLISHED,
                model_number=request.model_number,
                warnings=[
                    "Generic deck screws are PROHIBITED for structural connectors. Use specified Strong-Drive SD screws or connector nails."
                ],
                elimination_reasons=["PROHIBITED_FASTENER_GENERIC_DECK_SCREW"],
            )

        # Check corrosion compatibility
        if (
            request.environment == EnvironmentClassification.COASTAL_HIGH_CORROSION
            and not request.model_number.endswith("-SS")
        ):
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.MANUFACTURER_PUBLISHED,
                model_number=request.model_number,
                warnings=[
                    "Standard G90 galvanized finish is non-compliant for coastal high corrosion environment. Stainless steel (SS316/SS304) required."
                ],
                elimination_reasons=["INSUFFICIENT_CORROSION_RESISTANCE"],
            )
        elif request.environment == EnvironmentClassification.TREATED_WOOD and not (
            request.model_number.endswith("-SS")
            or request.model_number.endswith("Z")
            or request.model_number.endswith("HDG")
        ):
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.MANUFACTURER_PUBLISHED,
                model_number=request.model_number,
                warnings=["Standard G90 galvanized finish is non-compliant for treated wood."],
                elimination_reasons=["INSUFFICIENT_CORROSION_RESISTANCE"],
            )

        # Strict Database Lookup - NO SYNTHETIC FALLBACKS
        db_online = await check_db_health()
        if not db_online:
            return ConnectionCheckResult(
                is_compliant=False,
                classification=AnswerClassification.INSUFFICIENT_INFORMATION,
                model_number=request.model_number,
                warnings=[
                    "DATABASE_OFFLINE: PostgreSQL database is offline or unreachable. No synthetic fallbacks permitted."
                ],
                elimination_reasons=["DATABASE_OFFLINE"],
            )

        c_uplift = Decimal("0")
        c_download = Decimal("0")
        c_lateral = Decimal("0")
        fastener_sched = "Specified nails/screws as per Simpson catalog"
        citations_list = []

        async with async_session_factory() as session:
            # Query variant
            stmt = select(ProductVariantORM).where(
                ProductVariantORM.model_number == request.model_number
            )
            v_res = await session.execute(stmt)
            variant = v_res.scalar_one_or_none()

            if not variant:
                # Try finding without suffix
                clean_model = (
                    request.model_number.replace("-SS", "").replace("Z", "").replace("HDG", "")
                )
                stmt_clean = select(ProductVariantORM).where(
                    ProductVariantORM.model_number == clean_model
                )
                v_res_clean = await session.execute(stmt_clean)
                variant = v_res_clean.scalar_one_or_none()

            if not variant:
                return ConnectionCheckResult(
                    is_compliant=False,
                    classification=AnswerClassification.UNVERIFIED,
                    model_number=request.model_number,
                    warnings=[
                        f"MODEL_NOT_FOUND_IN_DATABASE: Model '{request.model_number}' does not exist in the catalog database."
                    ],
                    elimination_reasons=["MODEL_NOT_FOUND_IN_DATABASE"],
                )

            # Query published capacities
            cap_stmt = select(PublishedCapacityORM).where(
                PublishedCapacityORM.product_variant_id == variant.id
            )
            cap_res = await session.execute(cap_stmt)
            capacities = cap_res.scalars().all()

            if not capacities:
                return ConnectionCheckResult(
                    is_compliant=False,
                    classification=AnswerClassification.UNVERIFIED,
                    model_number=request.model_number,
                    warnings=[
                        f"NO_CAPACITY_DATA_IN_DATABASE: Model '{request.model_number}' has no published capacities in the database."
                    ],
                    elimination_reasons=["NO_CAPACITY_DATA_IN_DATABASE"],
                )

            for cap in capacities:
                if cap.load_direction == LoadDirection.UPLIFT:
                    c_uplift = cap.capacity_lbf
                    fastener_sched = cap.fastener_schedule_text
                    if cap.citation_id not in citations_list:
                        citations_list.append(cap.citation_id)
                elif cap.load_direction == LoadDirection.DOWNLOAD:
                    c_download = cap.capacity_lbf
                    if cap.citation_id not in citations_list:
                        citations_list.append(cap.citation_id)
                elif cap.load_direction in (LoadDirection.LATERAL_F1, LoadDirection.LATERAL_F2):
                    c_lateral = max(c_lateral, cap.capacity_lbf)
                    if cap.citation_id not in citations_list:
                        citations_list.append(cap.citation_id)

        p_uplift = max(Decimal("0"), request.required_uplift_lbf or Decimal("0"))
        p_download = max(Decimal("0"), request.required_download_lbf or Decimal("0"))
        p_lateral = max(Decimal("0"), request.required_lateral_lbf or Decimal("0"))

        r_uplift = (p_uplift / c_uplift) if c_uplift > 0 else Decimal("0")
        r_download = (p_download / c_download) if c_download > 0 else Decimal("0")
        r_lateral = (p_lateral / c_lateral) if c_lateral > 0 else Decimal("0")

        unity_ratio = (r_uplift + r_download + r_lateral).quantize(Decimal("0.001"))

        is_compliant = True
        warnings = []
        elimination_reasons = []

        if unity_ratio > Decimal("1.0"):
            is_compliant = False
            warnings.append(
                f"Multi-vector load combination unity ratio ({unity_ratio:.3f}) exceeds 1.0."
            )
            elimination_reasons.append("UNITY_RATIO_EXCEEDED")

        if (
            request.required_uplift_lbf is not None
            and c_uplift > 0
            and request.required_uplift_lbf > c_uplift
        ):
            is_compliant = False
            warnings.append("Required uplift load exceeds allowable capacity.")
            elimination_reasons.append("INSUFFICIENT_CAPACITY")

        return ConnectionCheckResult(
            is_compliant=is_compliant,
            classification=AnswerClassification.MANUFACTURER_PUBLISHED,
            model_number=request.model_number,
            allowable_capacity_lbf=c_uplift,
            required_load_lbf=request.required_uplift_lbf,
            unity_ratio=unity_ratio,
            fastener_schedule=fastener_sched,
            citations=citations_list or ["C-C-2026 Catalog"],
            warnings=warnings,
            elimination_reasons=elimination_reasons,
        )
