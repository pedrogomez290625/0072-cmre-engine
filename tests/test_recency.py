"""Tests for per-claim-type recency decay."""

from datetime import datetime, timezone, timedelta

from cmre.models import Claim
from cmre.services.recency import recency_factor


def _claim(claim_type: str, published_at: datetime | None, **kwargs) -> Claim:
    return Claim(
        statement="x",
        claim_type=claim_type,
        published_at=published_at,
        **kwargs,
    )


def test_recency_mechanism_old_does_not_die():
    """A mechanism from 5 years ago should still have non-trivial weight."""
    long_ago = datetime.now(timezone.utc) - timedelta(days=365 * 5)
    c = _claim("mechanism", long_ago)
    w = recency_factor(c)
    # Mechanism half-life = 5y → 5y/5y = 1 half-life → 0.5
    assert w >= 0.45


def test_recency_mechanism_very_old_decays_slowly():
    """A 10-year-old mechanism still survives (vs empirical_trick dying)."""
    long_ago = datetime.now(timezone.utc) - timedelta(days=365 * 10)
    c_mech = _claim("mechanism", long_ago)
    c_trick = _claim("empirical_trick", long_ago)
    w_mech = recency_factor(c_mech)
    w_trick = recency_factor(c_trick)
    # Mechanism survives much better than empirical trick
    assert w_mech > w_trick


def test_recency_empirical_trick_recent_is_strong():
    recent = datetime.now(timezone.utc) - timedelta(days=30)
    c = _claim("empirical_trick", recent)
    w = recency_factor(c)
    assert w > 0.9


def test_recency_platform_specific_decays_fast():
    """Platform-specific claim from 2 years ago should be heavily penalized."""
    long_ago = datetime.now(timezone.utc) - timedelta(days=365 * 2)
    c = _claim("platform_specific", long_ago)
    w = recency_factor(c)
    # half-life 180d → 730/180 = 4 half-lives → 0.5^4 ≈ 0.06, clamped to 0.2
    assert w <= 0.30


def test_recency_validation_count_boosts():
    """Validation boost is most visible on older claims where base has decayed."""
    some_time_ago = datetime.now(timezone.utc) - timedelta(days=365 * 2)
    c_no_val = _claim("empirical_trick", some_time_ago, validation_count=0)
    c_many_val = _claim("empirical_trick", some_time_ago, validation_count=5)
    w_no = recency_factor(c_no_val)
    w_many = recency_factor(c_many_val)
    assert w_many > w_no


def test_recency_reproducibility_boosts():
    """Reproducibility boost is most visible on older claims."""
    some_time_ago = datetime.now(timezone.utc) - timedelta(days=365 * 2)
    c_low = _claim("mechanism", some_time_ago, reproducibility_score=0.0)
    c_high = _claim("mechanism", some_time_ago, reproducibility_score=1.0)
    assert recency_factor(c_high) > recency_factor(c_low)


def test_recency_unknown_published_at_returns_neutral():
    c = _claim("mechanism", None)
    w = recency_factor(c)
    assert 0.4 <= w <= 0.6


def test_recency_clamped_to_min_0_2():
    """Even ancient claims have a floor weight so they're not forgotten."""
    ancient = datetime.now(timezone.utc) - timedelta(days=365 * 50)
    c = _claim("platform_specific", ancient)
    w = recency_factor(c)
    assert w >= 0.2
