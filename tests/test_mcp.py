import pytest
from simpson_mcp.main import get_system_status_resource, system_diagnostics


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
