"""Domain entities migration for products, variants, claims, citations, capacities.

Revision ID: 0002_domain_entities
Revises: 0001_init_foundation
Create Date: 2026-07-26
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_domain_entities"
down_revision = "0001_init_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Products table
    op.create_table(
        "products",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column("model_number", sa.String(length=100), unique=True, nullable=False),
        sa.Column("series_name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_products_model_number", "products", ["model_number"])
    op.create_index("ix_products_category", "products", ["category"])

    # Product variants table
    op.create_table(
        "product_variants",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column(
            "product_id", sa.String(length=100), sa.ForeignKey("products.id"), nullable=False
        ),
        sa.Column("model_number", sa.String(length=100), nullable=False),
        sa.Column("gauge", sa.Integer(), nullable=True),
        sa.Column("coating", sa.String(length=50), nullable=False, server_default="G90"),
        sa.Column("dimensions_in", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_product_variants_model_number", "product_variants", ["model_number"])

    # Product aliases table
    op.create_table(
        "product_aliases",
        sa.Column("alias", sa.String(length=100), primary_key=True),
        sa.Column("target_model", sa.String(length=100), nullable=False),
        sa.Column("is_canonical", sa.Boolean(), server_default="false", nullable=False),
    )
    op.create_index("ix_product_aliases_target_model", "product_aliases", ["target_model"])

    # Citations table
    op.create_table(
        "citations",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column("document_revision_id", sa.String(length=100), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("section_heading", sa.String(length=255), nullable=True),
        sa.Column("table_identifier", sa.String(length=100), nullable=True),
        sa.Column("row_label", sa.String(length=100), nullable=True),
        sa.Column("column_label", sa.String(length=100), nullable=True),
        sa.Column("footnote_ids", sa.JSON(), nullable=False),
        sa.Column("bounding_box_json", sa.JSON(), nullable=True),
        sa.Column("supporting_excerpt", sa.Text(), nullable=True),
    )

    # Source claims table
    op.create_table(
        "source_claims",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column("claim_type", sa.String(length=100), nullable=False),
        sa.Column("subject_type", sa.String(length=100), nullable=False),
        sa.Column("subject_id", sa.String(length=100), nullable=False),
        sa.Column("predicate", sa.String(length=100), nullable=False),
        sa.Column("value_decimal", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("conditions_json", sa.JSON(), nullable=False),
        sa.Column(
            "citation_id", sa.String(length=100), sa.ForeignKey("citations.id"), nullable=False
        ),
        sa.Column(
            "verification_status",
            sa.String(length=50),
            nullable=False,
            server_default="HUMAN_VERIFIED",
        ),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
    )
    op.create_index("ix_source_claims_claim_type", "source_claims", ["claim_type"])
    op.create_index("ix_source_claims_subject_id", "source_claims", ["subject_id"])

    # Published capacities table
    op.create_table(
        "published_capacities",
        sa.Column("id", sa.String(length=100), primary_key=True),
        sa.Column(
            "product_variant_id",
            sa.String(length=100),
            sa.ForeignKey("product_variants.id"),
            nullable=False,
        ),
        sa.Column("design_method", sa.String(length=20), nullable=False),
        sa.Column("load_direction", sa.String(length=50), nullable=False),
        sa.Column("wood_species_group", sa.String(length=50), nullable=False),
        sa.Column("capacity_lbf", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("fastener_schedule_text", sa.Text(), nullable=False),
        sa.Column(
            "citation_id", sa.String(length=100), sa.ForeignKey("citations.id"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("published_capacities")
    op.drop_table("source_claims")
    op.drop_table("citations")
    op.drop_table("product_aliases")
    op.drop_table("product_variants")
    op.drop_table("products")
