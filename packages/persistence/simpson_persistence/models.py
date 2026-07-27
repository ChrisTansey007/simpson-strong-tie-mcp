"""SQLAlchemy ORM base and domain entity models."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from simpson_domain.enums import (
    CoatingType,
    DesignMethod,
    LoadDirection,
    VerificationStatus,
    WoodSpeciesGroup,
)
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class SystemMetadataORM(Base):
    """System metadata table for DB connectivity & migration verification."""

    __tablename__ = "system_metadata"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class ProductORM(Base):
    """Core product line definition table."""

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    model_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    series_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    variants: Mapped[list["ProductVariantORM"]] = relationship(
        "ProductVariantORM", back_populates="product", cascade="all, delete-orphan"
    )


class ProductVariantORM(Base):
    """Specific product variant (gauge, coating, dimensions)."""

    __tablename__ = "product_variants"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(100), ForeignKey("products.id"), nullable=False)
    model_number: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    gauge: Mapped[int | None] = mapped_column(Integer, nullable=True)
    coating: Mapped[CoatingType] = mapped_column(
        Enum(CoatingType), default=CoatingType.STANDARD_GALVANIZED, nullable=False
    )
    dimensions_in: Mapped[str | None] = mapped_column(String(100), nullable=True)

    product: Mapped["ProductORM"] = relationship("ProductORM", back_populates="variants")
    capacities: Mapped[list["PublishedCapacityORM"]] = relationship(
        "PublishedCapacityORM", back_populates="variant", cascade="all, delete-orphan"
    )


class ProductAliasORM(Base):
    """Product model alias or search variation mapping."""

    __tablename__ = "product_aliases"

    alias: Mapped[str] = mapped_column(String(100), primary_key=True)
    target_model: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    is_canonical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CitationORM(Base):
    """Citation linking claims directly to source document location."""

    __tablename__ = "citations"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    document_revision_id: Mapped[str] = mapped_column(String(100), nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    section_heading: Mapped[str | None] = mapped_column(String(255), nullable=True)
    table_identifier: Mapped[str | None] = mapped_column(String(100), nullable=True)
    row_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    column_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    footnote_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    bounding_box_json: Mapped[dict[str, float] | None] = mapped_column(JSON, nullable=True)
    supporting_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)


class SourceClaimORM(Base):
    """Structured atomic evidence claim extracted from technical literature."""

    __tablename__ = "source_claims"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    claim_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    subject_type: Mapped[str] = mapped_column(String(100), nullable=False)
    subject_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    predicate: Mapped[str] = mapped_column(String(100), nullable=False)
    value_decimal: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    conditions_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    citation_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("citations.id"), nullable=False
    )
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.HUMAN_VERIFIED, nullable=False
    )
    source_hash: Mapped[str] = mapped_column(String(64), nullable=False)


class PublishedCapacityORM(Base):
    """Published load capacity for product variants."""

    __tablename__ = "published_capacities"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    product_variant_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("product_variants.id"), nullable=False
    )
    design_method: Mapped[DesignMethod] = mapped_column(Enum(DesignMethod), nullable=False)
    load_direction: Mapped[LoadDirection] = mapped_column(Enum(LoadDirection), nullable=False)
    wood_species_group: Mapped[WoodSpeciesGroup] = mapped_column(
        Enum(WoodSpeciesGroup), nullable=False
    )
    capacity_lbf: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    fastener_schedule_text: Mapped[str] = mapped_column(Text, nullable=False)
    citation_id: Mapped[str] = mapped_column(
        String(100), ForeignKey("citations.id"), nullable=False
    )

    variant: Mapped["ProductVariantORM"] = relationship(
        "ProductVariantORM", back_populates="capacities"
    )
