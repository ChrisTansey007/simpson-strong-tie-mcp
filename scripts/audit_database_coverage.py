"""Detailed Database Coverage Audit script for Simpson Strong-Tie Knowledge Bank."""

import asyncio
from simpson_persistence.db import async_session_factory
from simpson_persistence.models import (
    CitationORM,
    LeasedJobORM,
    ProductAliasORM,
    ProductORM,
    ProductVariantORM,
    PublishedCapacityORM,
    SourceClaimORM,
)
from sqlalchemy import func, select


async def audit_coverage():
    print("======================================================================")
    print(" SIMPSON STRONG-TIE KNOWLEDGE BANK — DETAILED DATABASE AUDIT")
    print("======================================================================\n")

    async with async_session_factory() as session:
        # 1. Product Categories & Models
        prods_res = await session.execute(select(ProductORM))
        prods = prods_res.scalars().all()

        print(f"--- 1. PRODUCTS ({len(prods)} models) ---")
        categories = {}
        for p in prods:
            categories.setdefault(p.category, []).append(f"{p.model_number} ({p.series_name})")

        for cat, model_list in categories.items():
            print(f"  Category: [{cat}]")
            for m in model_list:
                print(f"    - {m}")

        # 2. Variants & Finishes
        vars_res = await session.execute(select(ProductVariantORM))
        variants = vars_res.scalars().all()

        print(f"\n--- 2. PRODUCT VARIANTS ({len(variants)} finish/gauge variations) ---")
        var_by_coating = {}
        for v in variants:
            c_val = v.coating.value if hasattr(v.coating, 'value') else str(v.coating)
            var_by_coating.setdefault(c_val, []).append(v.model_number)

        for coating, models in var_by_coating.items():
            print(f"  Coating/Finish [{coating}]: {len(models)} variants -> {', '.join(models)}")

        # 3. Published Capacities
        caps_res = await session.execute(select(PublishedCapacityORM))
        capacities = caps_res.scalars().all()

        print(f"\n--- 3. PUBLISHED LOAD CAPACITIES ({len(capacities)} directional load records) ---")
        cap_by_dir = {}
        for c in capacities:
            d_val = c.load_direction.value if hasattr(c.load_direction, 'value') else str(c.load_direction)
            cap_by_dir.setdefault(d_val, 0)
            cap_by_dir[d_val] += 1

        for d_name, count in cap_by_dir.items():
            print(f"  Load Direction [{d_name}]: {count} records")

        # 4. Citations & Revision Tracking
        cites_res = await session.execute(select(CitationORM))
        citations = cites_res.scalars().all()

        print(f"\n--- 4. CITATIONS & CATALOG PROVENANCE ({len(citations)} table locations) ---")
        for cite in citations:
            print(f"  - [{cite.id}] Rev: {cite.document_revision_id} | Page {cite.page_number} | {cite.table_identifier} | {cite.row_label} -> {cite.column_label}")

        # 5. Provenance Claims
        claims_res = await session.execute(select(SourceClaimORM))
        claims = claims_res.scalars().all()
        print(f"\n--- 5. PROVENANCE SOURCE CLAIMS ({len(claims)} verified claims) ---")
        verified_cnt = sum(1 for cl in claims if (cl.verification_status.value if hasattr(cl.verification_status, 'value') else str(cl.verification_status)) == "HUMAN_VERIFIED")
        print(f"  - Human Verified Claims: {verified_cnt} / {len(claims)}")

        # 6. Model Aliases
        alias_res = await session.execute(select(ProductAliasORM))
        aliases = alias_res.scalars().all()
        print(f"\n--- 6. PRODUCT MODEL ALIASES ({len(aliases)} mapped search terms) ---")
        print(f"  - Mapped search aliases: {', '.join([a.alias for a in aliases])}")

        print("\n======================================================================")


if __name__ == "__main__":
    asyncio.run(audit_coverage())
