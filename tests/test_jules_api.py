"""Tests for Jules API adapter and rate-limit tracker."""

from datetime import date, timedelta
from cmre.agents.jules_api import RateLimitTracker, JulesNotConfiguredError, JulesRateLimitError


def test_rate_limit_tracker_can_dispatch_under_limit():
    t = RateLimitTracker(daily_limit=5, concurrent_limit=2)
    assert t.can_dispatch() is True
    t.record_dispatch()
    assert t._used == 1
    assert t._in_flight == 1


def test_rate_limit_tracker_blocks_at_daily_limit():
    t = RateLimitTracker(daily_limit=2, concurrent_limit=10)
    t.record_dispatch()
    t.record_completion()
    t.record_dispatch()
    t.record_completion()
    assert t.can_dispatch() is False


def test_rate_limit_tracker_blocks_at_concurrent_limit():
    t = RateLimitTracker(daily_limit=100, concurrent_limit=2)
    t.record_dispatch()
    t.record_dispatch()
    assert t.can_dispatch() is False


def test_rate_limit_tracker_resets_on_new_day():
    t = RateLimitTracker(daily_limit=2, concurrent_limit=10)
    t.record_dispatch()
    t.record_completion()
    t.record_dispatch()
    t.record_completion()
    assert t.can_dispatch() is False
    # Simulate next day
    t._date = date.today() - timedelta(days=1)
    t._reset_if_new_day()
    assert t.can_dispatch() is True


def test_jules_not_configured_raises_when_no_key():
    from cmre.config import Settings
    from cmre.agents.jules_api import JulesAPIAdapter

    s = Settings(jules_api_key=None)
    a = JulesAPIAdapter(s)
    try:
        a.list_sessions()
        assert False, "expected JulesNotConfiguredError"
    except JulesNotConfiguredError:
        pass


def test_jules_rate_limit_error_has_retry_after():
    err = JulesRateLimitError("test", retry_after_seconds=42)
    assert err.retry_after_seconds == 42
