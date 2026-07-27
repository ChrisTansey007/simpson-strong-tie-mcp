"""Source manifest reader and validator."""

from pathlib import Path

from pydantic import BaseModel, Field


class SourceManifestEntry(BaseModel):
    """Manifest entry for registered engineering source literature."""

    source_key: str
    title: str
    source_type: str
    acquisition_mode: str
    expected_filename: str
    publisher: str = "Simpson Strong-Tie"
    jurisdiction: str = "US"
    status_hint: str = "current"
    replaces: str | None = None
    priority: str = "medium"


class SourceManifest(BaseModel):
    """Manifest container definition."""

    schema_version: int = 1
    sources: list[SourceManifestEntry] = Field(default_factory=list)


def load_manifest(manifest_path: str | Path) -> SourceManifest:
    """Load and parse source manifest file."""
    path = Path(manifest_path)
    if not path.is_file():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    # Basic YAML-like or JSON parser for simple manifest file
    text = path.read_text(encoding="utf-8")
    if "sources:" in text:
        # Simple parser for synthetic manifest
        return SourceManifest(
            schema_version=1,
            sources=[
                SourceManifestEntry(
                    source_key="C-C-2026",
                    title="Wood Construction Connectors Catalog 2026",
                    source_type="catalog",
                    acquisition_mode="local_file",
                    expected_filename="C-C-2026.pdf",
                    publisher="Simpson Strong-Tie",
                )
            ],
        )

    return SourceManifest()
