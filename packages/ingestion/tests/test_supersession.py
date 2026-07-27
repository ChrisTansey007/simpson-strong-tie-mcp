"""Tests for catalog revision diffing engine."""

from decimal import Decimal

from simpson_domain.enums import VerificationStatus
from simpson_ingestion.supersession import RevisionDiffEngine, _get_claim_identity
from simpson_provenance.models import SourceClaim


def create_claim(id: str, subject_id: str, value: str = "10.0") -> SourceClaim:
    return SourceClaim(
        id=id,
        claim_type="published_capacity",
        subject_type="product",
        subject_id=subject_id,
        predicate="allowable_uplift_load",
        value_decimal=Decimal(value),
        unit="lbs",
        conditions={"wood_type": "DF"},
        citation_id=f"cite-{id}",
        source_hash="hash",
    )


def test_get_claim_identity():
    c1 = create_claim("claim-1", "H1")
    c2 = create_claim("claim-2", "H1")
    c3 = create_claim("claim-3", "H2.5A")

    # c1 and c2 have the same identity
    assert _get_claim_identity(c1) == _get_claim_identity(c2)

    # c1 and c3 have different identities
    assert _get_claim_identity(c1) != _get_claim_identity(c3)


def test_diff_revisions_superseded_and_linked():
    old_claims = [
        create_claim("old-1", "H1", "10.0"),  # Will be updated in new revision
        create_claim("old-2", "H2", "20.0"),  # Will be removed in new revision
    ]

    new_claims = [
        create_claim("new-1", "H1", "15.0"),  # Updates old-1
        create_claim("new-3", "H3", "30.0"),  # Completely new
    ]

    engine = RevisionDiffEngine()
    updated_old, new_claims_out = engine.diff_revisions(old_claims, new_claims)

    # Check old claims
    assert len(updated_old) == 2

    # old-1 was updated
    assert updated_old[0].id == "old-1"
    assert updated_old[0].verification_status == VerificationStatus.SUPERSEDED
    assert updated_old[0].superseded_by == "new-1"

    # old-2 was removed
    assert updated_old[1].id == "old-2"
    assert updated_old[1].verification_status == VerificationStatus.SUPERSEDED
    assert updated_old[1].superseded_by is None

    # Check new claims out
    assert len(new_claims_out) == 2
    assert new_claims_out[0].id == "new-1"
    assert new_claims_out[1].id == "new-3"
