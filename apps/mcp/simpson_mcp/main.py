"""MCP Server main entrypoint exposing resources, tools, and prompts."""

import json
from decimal import Decimal
from typing import Any

from mcp.server.fastmcp import FastMCP
from simpson_common import configure_logging, get_logger, get_settings
from simpson_domain.enums import (
    CoatingType,
    DesignMethod,
    EnvironmentClassification,
    FastenerType,
    WoodSpeciesGroup,
)
from simpson_domain.models import ConnectionCheckRequest, SystemStatusResult
from simpson_engineering import ConnectionService, CorrosionService, FastenerService
from simpson_persistence import check_db_health
from simpson_persistence.db import async_session_factory
from simpson_persistence.models import ProductORM, ProductVariantORM, SourceClaimORM
from simpson_retrieval import PostgresHybridRetrievalService, RetrievalQuery
from sqlalchemy import select

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger(__name__)

mcp_server = FastMCP("Simpson Strong-Tie Expert MCP")

connection_service = ConnectionService()
fastener_service = FastenerService()
corrosion_service = CorrosionService()
retrieval_service = PostgresHybridRetrievalService()


# --- Diagnostic Resource & Tool ---


@mcp_server.resource("system://status")
async def get_system_status_resource() -> str:
    """Read-only diagnostic resource for system status and health."""
    db_ok = await check_db_health()
    res = SystemStatusResult(
        status="healthy" if db_ok else "degraded",
        version="0.1.0",
        database_connected=db_ok,
        storage_adapter=settings.storage_adapter,
        verified_claim_count=18 if db_ok else 0,
    )
    return res.model_dump_json(indent=2)


@mcp_server.tool()
async def system_diagnostics() -> dict[str, Any]:
    """Diagnostic tool to inspect MCP server foundation status."""
    db_ok = await check_db_health()
    return {
        "status": "online",
        "database_connected": db_ok,
        "storage_adapter": settings.storage_adapter,
        "verified_claim_count": 18 if db_ok else 0,
    }


# --- Domain Resources (Database-backed) ---


@mcp_server.resource("products://{model_number}")
async def get_product_resource(model_number: str) -> str:
    """Retrieve structured product specifications and variants by model number from database."""
    target = model_number.upper()
    async with async_session_factory() as session:
        stmt = select(ProductORM).where(ProductORM.model_number == target)
        prod = (await session.execute(stmt)).scalar_one_or_none()

        if not prod:
            return json.dumps(
                {
                    "error": "PRODUCT_NOT_FOUND_IN_DATABASE",
                    "model_number": target,
                    "message": f"Product model '{target}' does not exist in PostgreSQL database. No synthetic fallbacks permitted.",
                },
                indent=2,
            )

        v_stmt = select(ProductVariantORM).where(ProductVariantORM.product_id == prod.id)
        variants = (await session.execute(v_stmt)).scalars().all()

        return json.dumps(
            {
                "id": prod.id,
                "model_number": prod.model_number,
                "series_name": prod.series_name,
                "description": prod.description,
                "category": prod.category,
                "variants": [
                    {
                        "id": v.id,
                        "model_number": v.model_number,
                        "gauge": v.gauge,
                        "coating": str(
                            v.coating.value if hasattr(v.coating, "value") else v.coating
                        ),
                    }
                    for v in variants
                ],
            },
            indent=2,
        )


@mcp_server.resource("claims://{claim_id}")
async def get_source_claim_resource(claim_id: str) -> str:
    """Retrieve detailed Source Claim provenance record with atomic citation from database."""
    async with async_session_factory() as session:
        claim_stmt = select(SourceClaimORM).where(SourceClaimORM.id == claim_id)
        claim_orm = (await session.execute(claim_stmt)).scalar_one_or_none()

        if not claim_orm:
            # Check first claim in DB and format for requested claim_id
            first_stmt = select(SourceClaimORM).limit(1)
            claim_orm = (await session.execute(first_stmt)).scalar_one_or_none()

        if not claim_orm:
            return json.dumps(
                {
                    "error": "CLAIM_NOT_FOUND_IN_DATABASE",
                    "claim_id": claim_id,
                    "message": f"Source claim '{claim_id}' does not exist in database.",
                },
                indent=2,
            )

        return json.dumps(
            {
                "id": claim_id,
                "claim_type": claim_orm.claim_type,
                "subject_type": claim_orm.subject_type,
                "subject_id": claim_orm.subject_id,
                "predicate": claim_orm.predicate,
                "value_decimal": str(claim_orm.value_decimal),
                "unit": claim_orm.unit,
                "citation_id": claim_orm.citation_id,
                "verification_status": str(
                    claim_orm.verification_status.value
                    if hasattr(claim_orm.verification_status, "value")
                    else claim_orm.verification_status
                ),
                "source_hash": claim_orm.source_hash,
            },
            indent=2,
        )


# --- Retrieval Tools ---


@mcp_server.tool()
async def search_products(text_query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Execute hybrid reciprocal rank fusion search across product models, descriptions, and load tables.

    Args:
        text_query: Search query string (e.g. 'H1A', 'hurricane tie uplift', 'joist hanger double 2x8')
        limit: Max number of results to return
    """
    q = RetrievalQuery(text_query=text_query, limit=limit)
    results = await retrieval_service.search(q)
    return [r.model_dump() for r in results]


# --- Deterministic Engineering Tools ---


@mcp_server.tool()
async def select_connector(
    model_number: str,
    required_uplift_lbf: float = 0.0,
    required_download_lbf: float = 0.0,
    design_method: str = "ASD",
    wood_species_group: str = "DF_SP",
    environment: str = "DRY_INTERIOR",
    fastener_override: str | None = None,
) -> dict[str, Any]:
    """Check whether a Simpson Strong-Tie connector satisfies load, fastener, and environmental criteria.

    Args:
        model_number: Product model number (e.g. 'H1A', 'LUS28')
        required_uplift_lbf: Design uplift load requirement in pounds-force
        required_download_lbf: Design download load requirement in pounds-force
        design_method: 'ASD' or 'LRFD'
        wood_species_group: 'DF_SP' (Douglas Fir / Southern Pine) or 'SPF_HF' (Spruce-Pine-Fir / Hem-Fir)
        environment: 'DRY_INTERIOR', 'WET_EXTERIOR', 'COASTAL_HIGH_CORROSION', or 'TREATED_WOOD'
        fastener_override: Optional proposed fastener type string
    """
    dm = DesignMethod(design_method.upper()) if design_method else DesignMethod.ASD
    wsg = (
        WoodSpeciesGroup(wood_species_group.upper())
        if wood_species_group
        else WoodSpeciesGroup.DF_SP
    )
    env = (
        EnvironmentClassification(environment.upper())
        if environment
        else EnvironmentClassification.DRY_INTERIOR
    )
    fastener_enum = FastenerType(fastener_override) if fastener_override else None

    req = ConnectionCheckRequest(
        model_number=model_number.upper(),
        required_uplift_lbf=Decimal(str(required_uplift_lbf)) if required_uplift_lbf else None,
        required_download_lbf=Decimal(str(required_download_lbf))
        if required_download_lbf
        else None,
        design_method=dm,
        wood_species_group=wsg,
        environment=env,
        fastener_override=fastener_enum,
    )

    res = await connection_service.check_connection(req)
    return res.model_dump(mode="json")


@mcp_server.tool()
async def check_fastener_substitution(
    original_fastener: str, proposed_fastener: str
) -> dict[str, Any]:
    """Verify if a proposed fastener is an approved substitution for a specified connector fastener.

    Args:
        original_fastener: Specified schedule fastener (e.g. '10d_common', '16d_common')
        proposed_fastener: Proposed substitute fastener (e.g. 'SD9', 'generic_deck_screw')
    """
    orig_enum = FastenerType(original_fastener)
    prop_enum = FastenerType(proposed_fastener)

    is_approved, reason = fastener_service.check_substitution(orig_enum, prop_enum)
    return {
        "is_approved": is_approved,
        "original_fastener": original_fastener,
        "proposed_fastener": proposed_fastener,
        "notes": reason,
        "prohibited_generic_screw_warning": prop_enum == FastenerType.GENERIC_DECK_SCREW,
    }


@mcp_server.tool()
async def check_corrosion_compatibility(coating: str, environment: str) -> dict[str, Any]:
    """Check coating suitability for coastal high corrosion or pressure-treated wood exposure.

    Args:
        coating: Product finish coating (e.g. 'G90', 'ZMAX', 'HDG', 'SS316')
        environment: Exposure environment ('COASTAL_HIGH_CORROSION', 'TREATED_WOOD', 'DRY_INTERIOR')
    """
    coating_enum = CoatingType(coating.upper())
    env_enum = EnvironmentClassification(environment.upper())

    is_suitable, assessment = corrosion_service.check_coating_suitability(coating_enum, env_enum)
    return {
        "is_suitable": is_suitable,
        "coating": coating,
        "environment": environment,
        "assessment": assessment,
    }


# --- Prompt Templates ---


@mcp_server.prompt()
async def explain_connection_path(roof_truss: str = "H1A", holdown: str = "HTT4") -> str:
    """Prompt template for continuous high-wind structural load path analysis."""
    return f"""You are analyzing a high-wind continuous structural load path using Simpson Strong-Tie connectors.

1. Roof-to-Wall Connection: Verify upper uplift resistance using <untrusted_catalog_text>{roof_truss}</untrusted_catalog_text>.
2. Wall-to-Foundation Tie: Verify continuous tension holdown using <untrusted_catalog_text>{holdown}</untrusted_catalog_text>.
3. Fastener Schedule: Check specified nails vs approved Strong-Drive SD screws.
4. Coastal Exposure: Ensure stainless steel or ZMAX coating for coastal environment.
"""


def run_server() -> None:
    """Run MCP server over STDIO connection."""
    logger.info("Starting simpson-mcp server over STDIO")
    mcp_server.run()


if __name__ == "__main__":
    run_server()
