"""Query Simpson Strong-Tie Expert MCP for a 2-Story Coastal Build in Carolina Beach, NC."""

import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def run_carolina_beach_query():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "simpson-mcp"],
        env=None,
    )

    print("======================================================================")
    print(" CAROLINA BEACH, NC - 2-STORY COASTAL BUILD CONNECTOR SPECIFICATION")
    print(" Environment: COASTAL_HIGH_CORROSION (Salt Spray / Exposure Category D)")
    print(" Design Load Path: ASD Continuous High-Wind Load Path (150+ mph Zone)")
    print("======================================================================\n")

    async with (
        stdio_client(server_params) as (read_stream, write_stream),
        ClientSession(read_stream, write_stream) as session,
    ):
        await session.initialize()

        # 1. Environmental Corrosion Compatibility Check
        print("--- STEP 1: Environmental Finish & Corrosion Compatibility Check ---")
        g90_check = await session.call_tool(
            "check_corrosion_compatibility",
            arguments={"coating": "G90", "environment": "COASTAL_HIGH_CORROSION"},
        )
        print("[G90 Standard Galvanized Check]:", g90_check.content[0].text)

        ss316_check = await session.call_tool(
            "check_corrosion_compatibility",
            arguments={"coating": "SS316", "environment": "COASTAL_HIGH_CORROSION"},
        )
        print("[SS316 Stainless Steel Check]:", ss316_check.content[0].text)
        print()

        # 2. Roof Rafter-to-Top-Plate Tie (2nd Floor Roof)
        print("--- STEP 2: Roof-to-Wall Tie (Story 2 Rafters/Trusses) ---")
        roof_tie = await session.call_tool(
            "select_connector",
            arguments={
                "model_number": "H1A",
                "required_uplift_lbf": 650.0,
                "design_method": "ASD",
                "wood_species_group": "SPF_HF",
                "environment": "COASTAL_HIGH_CORROSION",
            },
        )
        print("[Roof Hurricane Tie - H1A]:", roof_tie.content[0].text)
        print()

        # 3. 2nd Floor Joist Hangers
        print("--- STEP 3: Floor Framing Hangers (Story 2 Joists) ---")
        joist_hanger = await session.call_tool(
            "select_connector",
            arguments={
                "model_number": "LUS28",
                "required_download_lbf": 1200.0,
                "design_method": "ASD",
                "wood_species_group": "DF_SP",
                "environment": "COASTAL_HIGH_CORROSION",
            },
        )
        print("[Floor Joist Hanger - LUS28]:", joist_hanger.content[0].text)
        print()

        # 4. Story-to-Story Floor Tension Tie (Story 2 Wall to Story 1 Wall)
        print("--- STEP 4: Story-to-Story Wall Tension Strap (Story 2 -> Story 1) ---")
        wall_strap = await session.call_tool(
            "select_connector",
            arguments={
                "model_number": "LSTA24",
                "required_uplift_lbf": 850.0,
                "design_method": "ASD",
                "wood_species_group": "DF_SP",
                "environment": "COASTAL_HIGH_CORROSION",
            },
        )
        print("[Story-to-Story Strap - LSTA24]:", wall_strap.content[0].text)
        print()

        # 5. Wall-to-Foundation Holdown (1st Story Foundation Anchor)
        print("--- STEP 5: Wall-to-Foundation Tension Holdown (Story 1 Wall Anchor) ---")
        holdown = await session.call_tool(
            "select_connector",
            arguments={
                "model_number": "HTT4",
                "required_uplift_lbf": 3200.0,
                "design_method": "ASD",
                "wood_species_group": "DF_SP",
                "environment": "COASTAL_HIGH_CORROSION",
            },
        )
        print("[Foundation Holdown - HTT4]:", holdown.content[0].text)
        print()

        # 6. Fastener Substitution Verification
        print("--- STEP 6: Fastener Schedule & Substitution Verification ---")
        sd_check = await session.call_tool(
            "check_fastener_substitution",
            arguments={"original_fastener": "10d_common", "proposed_fastener": "SD9"},
        )
        print("[SD9 Screw Substitution for 10d Nail]:", sd_check.content[0].text)

        deck_screw_check = await session.call_tool(
            "check_fastener_substitution",
            arguments={
                "original_fastener": "10d_common",
                "proposed_fastener": "generic_deck_screw",
            },
        )
        print("[Generic Deck Screw Check]:", deck_screw_check.content[0].text)


if __name__ == "__main__":
    asyncio.run(run_carolina_beach_query())
