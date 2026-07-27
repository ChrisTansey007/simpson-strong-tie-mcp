# ADR 0003: Immutable Source Documents and Provenance Claims

## Context
Engineering capacities must be reproducible and linked directly to authoritative manufacturer catalogs and technical letters.

## Decision
Source document files are stored immutably using SHA-256 content hashes. Every extracted claim is stored as a `SourceClaim` linked to a `Citation` with page, table, row, and bounding box coordinates.

## Consequences
- Complete auditability and zero risk of silent evidence mutation.
- Support for human verification before extracted claims drive tools.
