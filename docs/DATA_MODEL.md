# Data Model Specification

## Architectural Principle

PostgreSQL is the system of record. Every extracted engineering capacity or fastener schedule must be backed by an immutable `SourceClaim` linked to a `Citation`.

## Key Tables & Schemas

### 1. Products & Variants
- `products`: id, model_number, series_name, description, category
- `product_variants`: id, product_id, model_number, gauge, coating, dimensions_in
- `product_aliases`: alias (PK), target_model, is_canonical

### 2. Fasteners & Schedules
- `fasteners`: id, fastener_type, name, diameter_in, length_in
- `fastener_schedules`: id, product_variant_id, fastener_type, quantity, header_qty, joist_qty

### 3. Load Capacities & Claims
- `published_capacities`: id, product_variant_id, design_method, load_direction, wood_species_group, capacity_lbf, citation_id
- `source_claims`: id, claim_type, subject_type, subject_id, predicate, value_decimal, unit, citation_id, verification_status, source_hash

### 4. Provenance & Citations
- `citations`: id, document_revision_id, page_number, section_heading, table_identifier, row_label, column_label, footnote_ids, bounding_box, supporting_excerpt
