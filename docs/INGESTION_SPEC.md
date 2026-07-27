# Ingestion Pipeline Specification

## Immutable Evidence Layer
Original documents are write-once by SHA-256 hash.

Path template:
`sources/{publisher}/{document_key}/{sha256_hash}/original.pdf`

## Pipeline Stages
1. `REGISTER_SOURCE`: Read manifest entry or local intake file.
2. `HASH_AND_DEDUPLICATE`: Calculate SHA-256 hex digest.
3. `STORE_ORIGINAL`: Write to immutable storage (`simpson-storage`).
4. `PARSE_DOCUMENT`: Extract layout, hierarchy, and text with Docling & PyMuPDF.
5. `EXTRACT_CLAIMS`: Parse load tables, fastener schedules, and footnotes into candidate `SourceClaim` records.
6. `HUMAN_VERIFICATION`: Create human review tasks in admin app.
7. `ACTIVATE_RECORDS`: Mark claims as `HUMAN_VERIFIED` to enable tool consumption.
