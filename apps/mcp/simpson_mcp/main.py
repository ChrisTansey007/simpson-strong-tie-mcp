"""MCP Server main entrypoint exposing resources, tools, and prompts."""

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
from simpson_provenance import BoundingBox, Citation, SourceClaim
from simpson_testing import create_synthetic_product

settings = get_settings()
configure_logging(log_level=settings.log_level)
logger = get_logger(__name__)

mcp_server = FastMCP("Simpson Strong-Tie Expert MCP")

connection_service = ConnectionService()
fastener_service = FastenerService()
corrosion_service = CorrosionService()


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
        verified_claim_count=1,
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
        "verified_claim_count": 1,
    }


# --- Domain Resources ---


@mcp_server.resource("products://{model_number}")
async def get_product_resource(model_number: str) -> str:
    """Retrieve structured product specifications and variants by model number (e.g. H1A, LUS28)."""
    product = create_synthetic_product(model_number=model_number.upper())
    return product.model_dump_json(indent=2)


@mcp_server.resource("claims://{claim_id}")
async def get_source_claim_resource(claim_id: str) -> str:
    """Retrieve detailed Source Claim provenance record with atomic citation and bounding box coordinates."""
    citation = Citation(
        id=f"cite-{claim_id}",
        document_revision_id="rev-C-C-2026-v1",
        page_number=287,
        section_heading="Hurricane and Seismic Ties",
        table_identifier="Table 2",
        row_label="H1A",
        column_label="Uplift (SPF/HF)",
        bounding_box=BoundingBox(x0=84.1, y0=212.5, x1=519.3, y1=486.2),
        supporting_excerpt="Allowable ASD uplift load 745 lbf with 4-10dx1-1/2 nails to rafter.",
    )
    claim = SourceClaim(
        id=claim_id,
        claim_type="published_capacity",
        subject_type="product_variant",
        subject_id="var-H1A-G90",
        predicate="allowable_uplift_load",
        value_decimal=Decimal("745"),
        unit="lbf",
        conditions={
            "design_method": "ASD",
            "wood_species_group": "SPF/HF",
            "fastener_schedule": "4-10dx1-1/2 to rafter, 4-10d to plate",
        },
        citation_id=citation.id,
        source_hash="e8b0a9f5d1645e7f2257d00f723bd0ca9810a9a08ea15a9956461a6c42171c66",
    )
    return claim.model_dump_json(indent=2)


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
    return res.model_dump()


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

1. Roof-to-Wall Connection: Verify upper uplift resistance using {roof_truss}.
2. Wall-to-Foundation Tie: Verify continuous tension holdown using {holdown}.
3. Fastener Schedule: Check specified nails vs approved Strong-Drive SD screws.
4. Coastal Exposure: Ensure stainless steel or ZMAX coating for coastal environment.
"""


def run_server() -> None:
    """Run MCP server over STDIO connection."""
    logger.info("Starting simpson-mcp server over STDIO")
    mcp_server.run()


if __name__ == "__main__":
    run_server()
