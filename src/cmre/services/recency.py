"""Per-claim-type recency decay.

Different kinds of knowledge age at different speeds:

- mechanism: a fundamental principle (focal loss, calibration, temporal
  validation). Decays slowly because the underlying math doesn't go stale.
  Half-life: 5 years.

- empirical_trick: a heuristic that empirically helps in some context.
  Decays moderately. The community may find a better trick.
  Half-life: 1 year.

- platform_specific: tied to a specific platform / leaderboard behavior.
  Decays fast. Half-life: 6 months.

We also boost by validation_count and reproducibility_score so a
well-validated old claim does not die of old age.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from ..models import Claim


HALF_LIFE_DAYS = {
    "mechanism": 1825,        # 5 years
    "empirical_trick": 365,   # 1 year
    "platform_specific": 180, # 6 months
}

DEFAULT_HALF_LIFE = 365


def _now() -> datetime:
    return datetime.now(timezone.utc)


def recency_factor(claim: Claim, now: Optional[datetime] = None) -> float:
    """Compute the recency factor for a claim.

    Returns a value in [0.2, 1.0]. Older claims decay; well-validated claims
    are boosted; the result is clamped so even ancient validated claims keep
    some weight.

    Reference date: prefer last_validated_at (recent reproduction), then
    published_at. If both are missing, return a neutral 0.5 — we don't fall
    back to created_at because that would make every fresh claim look new.
    """
    now = now or _now()
    reference = claim.last_validated_at or claim.published_at
    if reference is None:
        return 0.5  # unknown age → neutral
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    age_days = max(0, (now - reference).days)

    half_life = HALF_LIFE_DAYS.get(claim.claim_type, DEFAULT_HALF_LIFE)
    base = 0.5 ** (age_days / half_life)

    # Validation boost: each validation adds up to 0.02, capped at 5.
    base += 0.02 * min(claim.validation_count, 5)

    # Reproducibility boost: up to +0.05
    base += 0.05 * max(0.0, min(1.0, claim.reproducibility_score))

    return max(0.2, min(1.0, base))


def recency_factors_for(claims: list[Claim], now: Optional[datetime] = None) -> dict[int, float]:
    """Bulk helper: returns {claim_id: recency_factor}."""
    return {c.id: recency_factor(c, now) for c in claims if c.id is not None}
