"""Catalog revision diffing engine."""

import json

from simpson_domain.enums import VerificationStatus
from simpson_provenance.models import SourceClaim


def _get_claim_identity(claim: SourceClaim) -> str:
    """Generate a unique identity string for a claim based on its logical components."""
    # Convert conditions dict to a sorted string for stable hashing/comparison
    conditions_str = json.dumps(claim.conditions, sort_keys=True)

    return f"{claim.claim_type}::{claim.subject_type}::{claim.subject_id}::{claim.predicate}::{conditions_str}"


class RevisionDiffEngine:
    """Engine for diffing claims between catalog revisions."""

    def __init__(self):
        pass

    def diff_revisions(
        self, old_claims: list[SourceClaim], new_claims: list[SourceClaim]
    ) -> tuple[list[SourceClaim], list[SourceClaim]]:
        """
        Compare claims across revisions.

        Args:
            old_claims: Claims from the previous revision.
            new_claims: Claims from the new revision.

        Returns:
            Tuple of (updated_old_claims, new_claims)
        """
        # Map new claims by their logical identity
        new_claims_map: dict[str, SourceClaim] = {_get_claim_identity(c): c for c in new_claims}

        updated_old_claims = []

        for old_claim in old_claims:
            identity = _get_claim_identity(old_claim)

            # Whether superseded by a new matching claim or removed, the old claim is SUPERSEDED
            old_claim.verification_status = VerificationStatus.SUPERSEDED

            if identity in new_claims_map:
                new_claim = new_claims_map[identity]
                # Link old claim to new claim
                old_claim.superseded_by = new_claim.id
            else:
                old_claim.superseded_by = None

            updated_old_claims.append(old_claim)

        return updated_old_claims, new_claims
