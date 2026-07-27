import json

import pytest
from simpson_mcp.main import (
    check_corrosion_compatibility,
    check_fastener_substitution,
    get_product_resource,
    get_source_claim_resource,
    get_system_status_resource,
    select_connector,
    system_diagnostics,
)


@pytest.mark.asyncio
async def test_mcp_system_status_resource():
    json_str = await get_system_status_resource()
    assert "version" in json_str
    assert "0.1.0" in json_str


@pytest.mark.asyncio
async def test_mcp_system_diagnostics_tool():
    res = await system_diagnostics()
    assert res["status"] == "online"
    assert "database_connected" in res


@pytest.mark.asyncio
async def test_mcp_product_resource():
    res_str = await get_product_resource("H1A")
    data = json.loads(res_str)
    assert data["model_number"] == "H1A"
    assert "variants" in data


@pytest.mark.asyncio
async def test_mcp_source_claim_resource():
    res_str = await get_source_claim_resource("claim-123")
    data = json.loads(res_str)
    assert data["id"] == "claim-123"
    assert data["claim_type"] == "published_capacity"
    assert "citation_id" in data


@pytest.mark.asyncio
async def test_mcp_select_connector_tool():
    res = await select_connector(model_number="H1A", required_uplift_lbf=500.0)
    assert res["is_compliant"] is True
    assert res["model_number"] == "H1A"
    assert len(res["citations"]) > 0


@pytest.mark.asyncio
async def test_mcp_select_connector_prohibited_deck_screw():
    res = await select_connector(
        model_number="H1A", required_uplift_lbf=500.0, fastener_override="generic_deck_screw"
    )
    assert res["is_compliant"] is False
    assert "PROHIBITED_FASTENER_GENERIC_DECK_SCREW" in res["elimination_reasons"]


@pytest.mark.asyncio
async def test_mcp_check_fastener_substitution_tool():
    res = await check_fastener_substitution("10d_common", "SD9")
    assert res["is_approved"] is True

    res_prohibited = await check_fastener_substitution("10d_common", "generic_deck_screw")
    assert res_prohibited["is_approved"] is False
    assert res_prohibited["prohibited_generic_screw_warning"] is True


@pytest.mark.asyncio
async def test_mcp_check_corrosion_compatibility_tool():
    res_ss = await check_corrosion_compatibility("SS316", "COASTAL_HIGH_CORROSION")
    assert res_ss["is_suitable"] is True

    res_g90 = await check_corrosion_compatibility("G90", "COASTAL_HIGH_CORROSION")
    assert res_g90["is_suitable"] is False
