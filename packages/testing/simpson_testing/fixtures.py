"""Synthetic test data factories."""

from simpson_domain.enums import CoatingType
from simpson_domain.models import Product, ProductVariant
from simpson_provenance.models import BoundingBox, Citation


def create_synthetic_product(model_number: str = "H1A") -> Product:
    """Generate synthetic product model labeled synthetic."""
    return Product(
        id="synth-prod-001",
        model_number=model_number,
        series_name="H Hurricane Ties",
        description="Synthetic test hurricane tie",
        category="Hurricane Ties",
        variants=[
            ProductVariant(
                id="synth-var-001",
                product_id="synth-prod-001",
                model_number=model_number,
                gauge=18,
                coating=CoatingType.STANDARD_GALVANIZED,
            )
        ],
    )


def create_synthetic_citation() -> Citation:
    """Generate synthetic citation record labeled synthetic."""
    return Citation(
        id="synth-cite-001",
        document_revision_id="synth-rev-001",
        page_number=287,
        section_heading="Allowable Loads",
        table_identifier="Table 2",
        row_label="H1A",
        column_label="Uplift SPF/HF",
        bounding_box=BoundingBox(x0=10.0, y0=20.0, x1=100.0, y1=200.0),
        supporting_excerpt="Synthetic test excerpt from C-C-2026",
    )
