# Simpson Strong-Tie MCP — External AI Auditor Prompt

> Copy and paste the prompt below into an external AI Agent (e.g. Devin, Claude, GPT-4o, or a custom Subagent) to perform a comprehensive audit and web/catalog research sweep against our live database.

---

```markdown
# TASK INSTRUCTIONS: SIMPSON STRONG-TIE MCP KNOWLEDGE BANK AUDITOR & RESEARCH SWEEP

You are acting as a Senior Principal Structural Engineer and AI Database Auditor. Your objective is to audit the live PostgreSQL database knowledge bank for the `simpson-strong-tie-mcp` platform, verify engineering accuracy, and research all missing Simpson Strong-Tie products to produce an actionable expansion specification.

---

## 🛑 MANDATORY AUDIT RULES

1. **STRICT NO SYNTHETIC FALLBACKS POLICY**: Never accept synthetic fallbacks, hardcoded mock values, or dummy estimates. Every capacity, citation, and fastener schedule must be backed by real Simpson Strong-Tie published catalog data (e.g., Catalog C-C-2026, C-CF-2026, C-A-2026, or ICC-ES Evaluation Reports).
2. **VERIFY LIVE DATABASE**: Ensure the PostgreSQL database container `simpson_postgres` (Port 5435) is online and querying live rows from `products`, `product_variants`, `published_capacities`, `citations`, and `source_claims`.
3. **FAIL-FAST VALIDATION**: If a requested product model is not found in PostgreSQL, confirm that the system correctly fails fast with `is_compliant: false` and `elimination_reasons: ["MODEL_NOT_FOUND_IN_DATABASE"]`.

---

## 📊 CURRENT INGESTED DATABASE INVENTORY (WHAT WE CURRENTLY HAVE)

The live database currently contains **32 Product Models**, **50 Variants**, **126 Load Capacities**, **10 Citations**, **50 SHA-256 Verified Claims**, and **61 Search Aliases** across 10 structural categories:

1. **Hurricane Ties (4 Models / 9 Variants / 22 Capacities)**:
   - Models: `H1A`, `H2.5A`, `H8`, `H10A`
   - Coatings: `G90` (Galvanized), `ZMAX`, `SS316` (Type 316 Stainless Steel)
   - Citations: `C-C-2026 Catalog p.287 Table 2`

2. **Joist Hangers (5 Models / 10 Variants / 26 Capacities)**:
   - Models: `LUS24`, `LUS26`, `LUS28`, `LUS210`, `HGUS28`
   - Coatings: `G90`, `ZMAX`, `SS316`
   - Citations: `C-C-2026 Catalog p.142 Table 1`

3. **Tension Straps (3 Models / 4 Variants / 8 Capacities)**:
   - Models: `LSTA18`, `LSTA24`, `MSTC40`
   - Coatings: `G90`, `SS316`
   - Citations: `C-C-2026 Catalog p.310 Table 4`

4. **Holdowns (2 Models / 3 Variants / 6 Capacities)**:
   - Models: `HTT4`, `HDU4` (`HDU4-SDS2.5`)
   - Coatings: `HDG` (Hot-Dip Galvanized), `SS316`
   - Citations: `C-C-2026 Catalog p.340 Table 6`

5. **Post Bases (2 Models / 3 Variants / 8 Capacities)**:
   - Models: `PBS44`, `ABW44`
   - Coatings: `HDG`, `ZMAX`, `SS316`
   - Citations: `C-C-2026 Catalog p.380 Table 8`

6. **Post Caps (1 Model / 1 Variant / 2 Capacities)**:
   - Models: `CC44`
   - Coatings: `HDG`
   - Citations: `C-C-2026 Catalog p.380 Table 8`

7. **Framing Angles (4 Models / 8 Variants / 18 Capacities)**:
   - Models: `A21`, `A23`, `A35`, `L90`
   - Coatings: `G90`, `ZMAX`, `SS316`
   - Citations: `C-C-2026 Catalog p.410 Table 10`

8. **Shearwall Systems (3 Models / 3 Variants / 9 Capacities)**:
   - Models: `WSW16` (Wood 16"), `WSW22` (Wood 22"), `SSW12` (Steel 12")
   - Coatings: `G90`
   - Citations: `C-C-2026 Catalog p.450 Table 12`

9. **Deck Connectors (1 Model / 2 Variants / 4 Capacities)**:
   - Models: `DTT2Z`
   - Coatings: `ZMAX`, `SS316`
   - Citations: `C-C-2026 Catalog p.470 Table 14`

10. **Mechanical Anchors & Screws (7 Models / 7 Variants / 18 Capacities)**:
    - Models: `Titen HD 3/8x3`, `Titen HD 1/2x4`, `Titen HD 5/8x5`, `Strong-Bolt 2 1/2x4-1/2`, `SD9112`, `SD10112`, `SDWS22300DB`
    - Coatings: `G90`, `ZMAX`, `SS316`
    - Citations: `C-CF-2026 Catalog p.85 Table 3`, `C-A-2026 Catalog p.112 Table 5`

---

## 🔎 RESEARCH MISSION & AUDIT SCOPE (WHAT TO RESEARCH)

Perform web research, catalog verification, and structural engineering analysis against official Simpson Strong-Tie literature (e.g. `strongtie.com`, `ICC-ES ESR` reports, and Simpson Wood Construction Catalogs) to identify missing items across the following categories:

### 1. Missing Hanger & Connection Lines:
- **Slope & Skew Hangers**: Research allowable loads for `SUR`/`SUL` skew hangers and `LSSU` adjustable slope/skew hangers.
- **Concealed Flange Hangers**: Research `LUC26`, `LUC28`, `IUS` I-joist hangers, and `HUC` heavy concealed flange hangers.
- **Top-Flange Hangers**: Research `BA`, `HB`, `ITS` top-flange I-joist hangers.

### 2. Missing Holdown & Shearwall Connectors:
- **Heavy Holdowns**: Research `HDU2-SDS2.5`, `HDU5-SDS2.5`, `HDU8-SDS2.5`, `HDQ8` heavy tension holdowns.
- **Deck Post Ties**: Research `DTT1Z` deck post tension tie and `DTT2-SS` stainless deck guardrail ties.

### 3. Missing Post Anchors & Column Caps:
- **Cast-In-Place Post Bases**: Research `CB44`, `CB66`, `CBSQ` cast-in-place post bases.
- **Standoff Column Bases**: Research `ABU44`, `ABU66`, `CPT44Z` concealed post ties.
- **End Column Caps**: Research `ECC44`, `ECC66`, `CCC66` triple beam column caps.

### 4. Missing Concrete Anchors & Chemical Systems:
- **Adhesive Anchor Systems**: Research `SET-3G` high-strength epoxy adhesive and `AT-XP` acrylic anchoring adhesive design tension/shear loads.
- **Cast-In-Place Concrete Anchors**: Research `MAB` mudsill anchors, `MAS` mudsill anchors, and `PAB` pre-assembled anchor bolts.

### 5. Missing Stainless Steel & Coastal Fasteners:
- **Stainless Screws**: Research `SD9112SS`, `SD10112SS`, `SDWS22300SS` Type 316 stainless structural screws for severe marine environments.
- **ICC-ES Evaluation Reports**: Map official ICC-ES evaluation report numbers (e.g. `ESR-2523`, `ESR-1023`, `ESR-2713`, `ESR-3050`) to product categories.

---

## 📋 EXPECTED AUDIT DELIVERABLE FORMAT

Produce a comprehensive **Simpson Strong-Tie Gap & Research Audit Report** formatted in clean GitHub markdown with:

1. **Audit Summary**: Verification of the current 32 product models and 126 load capacities in PostgreSQL.
2. **Missing Products Table**:
   - Product Model Number
   - Series Name & Category
   - Recommended Gauge & Finish Options (`G90`, `ZMAX`, `HDG`, `SS316`)
   - Allowable ASD Uplift, Download, & Lateral Loads (in lbf)
   - Fastener Schedule & Catalog Table Citation
3. **Python Seeding Snippet**: Provide a copy-paste ready Python data dictionary block to append into `scripts/seed_catalog_database.py` so we can immediately seed the database to 100% complete coverage for all newly researched items.
```
