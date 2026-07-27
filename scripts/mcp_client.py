"""Official MCP Client connecting to simpson-mcp over STDIO JSON-RPC protocol."""

import asyncio
import sys
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def run_mcp_client():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "simpson-mcp"],
        env=None,
    )

    print("Connecting to Simpson Strong-Tie Expert MCP Server over STDIO...")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("[SUCCESS] Official MCP ClientSession initialized via STDIO JSON-RPC!\n")

            # 1. List Available Resources
            resources = await session.list_resources()
            print(f"[1] Available MCP Resources ({len(resources.resources)}):")
            for res in resources.resources:
                print(f"  - {res.uri} ({res.name})")

            # 2. Read Resource (system://status)
            status_content = await session.read_resource("system://status")
            print("\n[2] Reading Resource `system://status`:")
            print(status_content.contents[0].text)

            # 3. Read Resource (products://H1A)
            product_content = await session.read_resource("products://H1A")
            print("\n[3] Reading Resource `products://H1A`:")
            print(product_content.contents[0].text)

            # 4. List Available Tools
            tools = await session.list_tools()
            print(f"\n[4] Available MCP Tools ({len(tools.tools)}):")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description.splitlines()[0]}")

            # 5. Call Tool: select_connector
            print("\n[5] Calling Tool `select_connector` (Model H1A, 600 lbf uplift):")
            res_conn = await session.call_tool(
                "select_connector",
                arguments={
                    "model_number": "H1A",
                    "required_uplift_lbf": 600.0,
                    "design_method": "ASD",
                    "wood_species_group": "SPF_HF",
                },
            )
            print(res_conn.content[0].text)

            # 6. Call Tool: check_fastener_substitution (10d common nail -> SD9 screw)
            print("\n[6] Calling Tool `check_fastener_substitution` (10d_common -> SD9):")
            res_fastener = await session.call_tool(
                "check_fastener_substitution",
                arguments={
                    "original_fastener": "10d_common",
                    "proposed_fastener": "SD9",
                },
            )
            print(res_fastener.content[0].text)

            # 7. Call Tool: check_corrosion_compatibility (G90 in COASTAL_HIGH_CORROSION)
            print("\n[7] Calling Tool `check_corrosion_compatibility` (G90 in Coastal):")
            res_corrosion = await session.call_tool(
                "check_corrosion_compatibility",
                arguments={
                    "coating": "G90",
                    "environment": "COASTAL_HIGH_CORROSION",
                },
            )
            print(res_corrosion.content[0].text)

            # 8. Call Tool: search_products
            print("\n[8] Calling Tool `search_products` ('hurricane tie uplift'):")
            res_search = await session.call_tool(
                "search_products",
                arguments={"text_query": "hurricane tie uplift", "limit": 3},
            )
            print(res_search.content[0].text)


if __name__ == "__main__":
    asyncio.run(run_mcp_client())
