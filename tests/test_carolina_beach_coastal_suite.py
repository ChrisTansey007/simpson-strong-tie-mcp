"""Comprehensive Test Suite for Carolina Beach 2-Story Coastal Build & Simpson Strong-Tie MCP."""

from decimal import Decimal

import pytest
from simpson_domain.enums import (
    AnswerClassification,
    CoatingType,
    DesignMethod,
    EnvironmentClassification,
    FastenerType,
    WoodSpeciesGroup,
)
from simpson_domain.models import ConnectionCheckRequest
from simpson_engineering import ConnectionService, CorrosionService, FastenerService
from simpson_mcp.main import (
    check_corrosion_compatibility,
    check_fastener_substitution,
    select_connector,
)


@pytest.fixture
def connection_service():
    return ConnectionService()


@pytest.fixture
def corrosion_service():
    return CorrosionService()


@pytest.fixture
def fastener_service():
    return FastenerService()


# --- SECTION 1: COASTAL CORROSION SUITE ---


def test_coastal_g90_prohibited(corrosion_service):
    """Verify standard G90 galvanized finish is strictly non-compliant in coastal environment."""
    is_suitable, msg = corrosion_service.check_coating_suitability(
        CoatingType.STANDARD_GALVANIZED, EnvironmentClassification.COASTAL_HIGH_CORROSION
    )
    assert is_suitable is False
    assert "non-compliant in coastal environments" in msg


def test_coastal_ss316_approved(corrosion_service):
    """Verify Type 316 Stainless Steel is approved for coastal salt spray environment."""
    is_suitable, msg = corrosion_service.check_coating_suitability(
        CoatingType.STAINLESS_316, EnvironmentClassification.COASTAL_HIGH_CORROSION
    )
    assert is_suitable is True
    assert "approved for coastal exposure" in msg


def test_treated_wood_zmax_hdg_approved(corrosion_service):
    """Verify ZMAX and HDG finishes are approved for contact with pressure-treated lumber."""
    is_zmax, _ = corrosion_service.check_coating_suitability(
        CoatingType.ZMAX, EnvironmentClassification.TREATED_WOOD
    )
    is_hdg, _ = corrosion_service.check_coating_suitability(
        CoatingType.HDG, EnvironmentClassification.TREATED_WOOD
    )
    assert is_zmax is True
    assert is_hdg is True


# --- SECTION 2: 2-STORY CONTINUOUS LOAD PATH SUITE (CAROLINA BEACH 150+ MPH ZONE) ---


@pytest.mark.asyncio
async def test_roof_to_top_plate_h1a_uplift(connection_service):
    """Verify H1A hurricane tie uplift capacity for Story 2 roof rafter connection."""
    req = ConnectionCheckRequest(
        model_number="H1A",
        required_uplift_lbf=Decimal("650"),
        design_method=DesignMethod.ASD,
        wood_species_group=WoodSpeciesGroup.SPF_HF,
        environment=EnvironmentClassification.DRY_INTERIOR,  # Interior baseline check
    )
    result = await connection_service.check_connection(req)
    assert result.is_compliant is True
    assert result.allowable_capacity_lbf == Decimal("745")
    assert result.classification == AnswerClassification.MANUFACTURER_PUBLISHED
    assert len(result.citations) > 0


@pytest.mark.asyncio
async def test_floor_joist_lus28_download(connection_service):
    """Verify LUS28 joist hanger download capacity for Story 2 floor framing."""
    req = ConnectionCheckRequest(
        model_number="LUS28",
        required_download_lbf=Decimal("1200"),
        design_method=DesignMethod.ASD,
        wood_species_group=WoodSpeciesGroup.DF_SP,
        environment=EnvironmentClassification.DRY_INTERIOR,
    )
    result = await connection_service.check_connection(req)
    assert result.is_compliant is True
    assert result.model_number == "LUS28"


@pytest.mark.asyncio
async def test_story_to_story_lsta24_tension_strap(connection_service):
    """Verify LSTA24 tension strap capacity for Story 2 to Story 1 floor-to-floor tie."""
    req = ConnectionCheckRequest(
        model_number="LSTA24",
        required_uplift_lbf=Decimal("850"),
        design_method=DesignMethod.ASD,
        wood_species_group=WoodSpeciesGroup.DF_SP,
        environment=EnvironmentClassification.DRY_INTERIOR,
    )
    result = await connection_service.check_connection(req)
    assert result.is_compliant is True


@pytest.mark.asyncio
async def test_foundation_htt4_holdown(connection_service):
    """Verify HTT4 heavy tension holdown capacity for Story 1 wall-to-foundation anchor."""
    req = ConnectionCheckRequest(
        model_number="HTT4",
        required_uplift_lbf=Decimal("3200"),
        design_method=DesignMethod.ASD,
        wood_species_group=WoodSpeciesGroup.DF_SP,
        environment=EnvironmentClassification.DRY_INTERIOR,
    )
    result = await connection_service.check_connection(req)
    assert result.is_compliant is True


# --- SECTION 3: FASTENER SUBSTITUTION & PROHIBITED HARDWARE SUITE ---


def test_approved_sd9_screw_substitution(fastener_service):
    """Verify Strong-Drive SD9 screw is approved 1-to-1 replacement for 10d common nail."""
    is_ok, msg = fastener_service.check_substitution(
        FastenerType.NAIL_COMMON_10D, FastenerType.SCREW_SD9
    )
    assert is_ok is True
    assert "approved 1-to-1 replacement" in msg


def test_approved_sd10_screw_substitution(fastener_service):
    """Verify Strong-Drive SD10 screw is approved 1-to-1 replacement for 16d common nail."""
    is_ok, msg = fastener_service.check_substitution(
        FastenerType.NAIL_COMMON_16D, FastenerType.SCREW_SD10
    )
    assert is_ok is True
    assert "approved 1-to-1 replacement" in msg


def test_prohibited_generic_deck_screw_rejection(fastener_service):
    """Verify generic deck screw is strictly rejected with prohibition warning."""
    is_ok, msg = fastener_service.check_substitution(
        FastenerType.NAIL_COMMON_10D, FastenerType.GENERIC_DECK_SCREW
    )
    assert is_ok is False
    assert "PROHIBITED" in msg


# --- SECTION 4: MCP SERVER ENGINE TOOL SUITE ---


@pytest.mark.asyncio
async def test_mcp_tool_select_connector_valid():
    res = await select_connector(
        model_number="H1A",
        required_uplift_lbf=650.0,
        design_method="ASD",
        wood_species_group="SPF_HF",
        environment="DRY_INTERIOR",
    )
    assert res["is_compliant"] is True
    assert Decimal(str(res["allowable_capacity_lbf"])) == Decimal("745")


@pytest.mark.asyncio
async def test_mcp_tool_select_connector_coastal_g90_rejection():
    res = await select_connector(
        model_number="H1A",
        required_uplift_lbf=650.0,
        environment="COASTAL_HIGH_CORROSION",
    )
    assert res["is_compliant"] is False
    assert "INSUFFICIENT_CORROSION_RESISTANCE" in res["elimination_reasons"]


@pytest.mark.asyncio
async def test_mcp_tool_check_fastener_substitution():
    res = await check_fastener_substitution("10d_common", "SD9")
    assert res["is_approved"] is True
    assert res["prohibited_generic_screw_warning"] is False

    res_deck = await check_fastener_substitution("10d_common", "generic_deck_screw")
    assert res_deck["is_approved"] is False
    assert res_deck["prohibited_generic_screw_warning"] is True


@pytest.mark.asyncio
async def test_mcp_tool_check_corrosion_compatibility():
    res_ss = await check_corrosion_compatibility("SS316", "COASTAL_HIGH_CORROSION")
    assert res_ss["is_suitable"] is True

    res_g90 = await check_corrosion_compatibility("G90", "COASTAL_HIGH_CORROSION")
    assert res_g90["is_suitable"] is False
