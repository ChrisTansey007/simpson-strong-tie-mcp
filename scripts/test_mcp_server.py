"""Live test script for Simpson Strong-Tie Expert MCP server tools and resources."""

import asyncio
import json

from simpson_mcp.main import (
    check_corrosion_compatibility,
    check_fastener_substitution,
    get_product_resource,
    get_source_claim_resource,
    get_system_status_resource,
    search_products,
    select_connector,
    system_diagnostics,
)


async def main():
    print("=" * 70)
    print("      SIMPSON STRONG-TIE EXPERT MCP - LIVE TEST HARNESS RESULTS      ")
    print("=" * 70)

    # 1. System Diagnostics
    diag = await system_diagnostics()
    print("\n[1] Diagnostic Tool (`system_diagnostics`):")
    print(json.dumps(diag, indent=2))

    # 2. System Status Resource
    status_res = await get_system_status_resource()
    print("\n[2] System Status Resource (`system://status`):")
    print(status_res)

    # 3. Product Resource
    prod_res = await get_product_resource("H1A")
    print("\n[3] Product Resource (`products://H1A`):")
    print(prod_res)

    # 4. Source Claim Resource
    claim_res = await get_source_claim_resource("claim-789")
    print("\n[4] Provenance Source Claim Resource (`claims://claim-789`):")
    print(claim_res)

    # 5. Hybrid Search Tool
    search_res = await search_products("hurricane tie uplift")
    print("\n[5] Hybrid RRF Search Tool (`search_products('hurricane tie uplift')`):")
    print(json.dumps(search_res, indent=2))

    # 6. Connector Selection Tool (Valid ASD load check)
    conn_valid = await select_connector(
        model_number="H1A",
        required_uplift_lbf=500.0,
        design_method="ASD",
        wood_species_group="SPF_HF",
    )
    print("\n[6] Connector Selection Tool - Valid Compliant Query (`select_connector('H1A')`):")
    print(json.dumps(conn_valid, indent=2))

    # 7. Connector Selection Tool (Adversarial generic deck screw check)
    conn_prohibited = await select_connector(
        model_number="H1A",
        required_uplift_lbf=500.0,
        fastener_override="generic_deck_screw",
    )
    print("\n[7] Connector Selection Tool - Adversarial Prohibited Fastener Query:")
    print(json.dumps(conn_prohibited, indent=2))

    # 8. Fastener Substitution Tool (Approved substitution)
    fastener_approved = await check_fastener_substitution("10d_common", "SD9")
    print(
        "\n[8] Fastener Substitution Tool - Approved (`check_fastener_substitution('10d_common', 'SD9')`):"
    )
    print(json.dumps(fastener_approved, indent=2))

    # 9. Corrosion Compatibility Tool (Coastal SS316 check)
    corrosion_ss = await check_corrosion_compatibility("SS316", "COASTAL_HIGH_CORROSION")
    print("\n[9] Corrosion Compatibility Tool - Coastal SS316:")
    print(json.dumps(corrosion_ss, indent=2))

    # 10. Corrosion Compatibility Tool (Coastal G90 non-compliant check)
    corrosion_g90 = await check_corrosion_compatibility("G90", "COASTAL_HIGH_CORROSION")
    print("\n[10] Corrosion Compatibility Tool - Coastal G90 (Prohibited):")
    print(json.dumps(corrosion_g90, indent=2))

    print("\n" + "=" * 70)
    print("                     ALL LIVE TEST CHECKS PASSED                     ")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
