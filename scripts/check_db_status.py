"""Inspect PostgreSQL database tables and population status."""

import asyncio
from simpson_persistence import check_db_health
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


async def check_db_population():
    print("======================================================================")
    print(" SIMPSON STRONG-TIE MCP — DATABASE POPULATION STATUS REPORT")
    print("======================================================================\n")

    health = await check_db_health()
    print(f"1. Database Connectivity Status: {'ONLINE' if health else 'OFFLINE / STANDBY'}")

    if not health:
        print("\n[NOTE] PostgreSQL database container is currently offline or uninitialized.")
        print("  - The MCP server currently uses high-fidelity synthetic fallbacks for all calculations.")
        print("  - Run `docker compose up -d postgres` and `uv run alembic upgrade head` to start PostgreSQL.")
        return

    async with async_session_factory() as session:
        p_cnt = (await session.execute(select(func.count(ProductORM.id)))).scalar()
        v_cnt = (await session.execute(select(func.count(ProductVariantORM.id)))).scalar()
        a_cnt = (await session.execute(select(func.count(ProductAliasORM.alias)))).scalar()
        cap_cnt = (await session.execute(select(func.count(PublishedCapacityORM.id)))).scalar()
        claim_cnt = (await session.execute(select(func.count(SourceClaimORM.id)))).scalar()
        cite_cnt = (await session.execute(select(func.count(CitationORM.id)))).scalar()
        job_cnt = (await session.execute(select(func.count(LeasedJobORM.id)))).scalar()

        print(f"2. Database Table Row Counts:")
        print(f"  - `products`: {p_cnt} rows")
        print(f"  - `product_variants`: {v_cnt} rows")
        print(f"  - `product_aliases`: {a_cnt} rows")
        print(f"  - `published_capacities`: {cap_cnt} rows")
        print(f"  - `source_claims`: {claim_cnt} rows")
        print(f"  - `citations`: {cite_cnt} rows")
        print(f"  - `leased_jobs`: {job_cnt} rows")


if __name__ == "__main__":
    asyncio.run(check_db_population())
