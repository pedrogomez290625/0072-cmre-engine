"""Jules API adapter (Google Cloud, REST v1alpha).

Jules is a Google coding agent that reached GA in August 2025.
Docs: https://jules.googleapis.com (REST v1alpha)
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, List, Optional

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from ..schemas import JulesTask

log = structlog.get_logger("cmre.agents.jules_api")


class JulesError(Exception):
    """Base error for Jules API failures."""


class JulesNotConfiguredError(JulesError):
    """Raised when CMRE_JULES_API_KEY is missing."""


class JulesRateLimitError(JulesError):
    def __init__(self, message: str, retry_after_seconds: Optional[int] = None):
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class RateLimitTracker:
    """Tracks daily task usage and concurrent in-flight sessions."""

    def __init__(self, daily_limit: int, concurrent_limit: int):
        self.daily_limit = daily_limit
        self.concurrent_limit = concurrent_limit
        self._date = date.today()
        self._used = 0
        self._in_flight = 0

    def _reset_if_new_day(self) -> None:
        today = date.today()
        if today != self._date:
            self._date = today
            self._used = 0
            self._in_flight = 0

    def can_dispatch(self) -> bool:
        self._reset_if_new_day()
        return self._used < self.daily_limit and self._in_flight < self.concurrent_limit

    def record_dispatch(self) -> None:
        self._reset_if_new_day()
        self._used += 1
        self._in_flight += 1

    def record_completion(self) -> None:
        self._in_flight = max(0, self._in_flight - 1)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "date": self._date.isoformat(),
            "used": self._used,
            "in_flight": self._in_flight,
            "daily_limit": self.daily_limit,
            "concurrent_limit": self.concurrent_limit,
        }


class JulesAPIAdapter:
    name = "jules_api"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.log = log
        self.tracker = RateLimitTracker(
            daily_limit=self.settings.jules_free_tier_daily_limit,
            concurrent_limit=self.settings.jules_concurrent_limit,
        )
        self._http: Optional[httpx.Client] = None
        if self.settings.jules_api_key:
            self._http = httpx.Client(
                base_url=self.settings.jules_api_base,
                timeout=60.0,
                headers={
                    "X-Goog-Api-Key": self.settings.jules_api_key,
                    "Content-Type": "application/json",
                },
            )

    def _require(self) -> None:
        if self._http is None:
            raise JulesNotConfiguredError(
                "CMRE_JULES_API_KEY is not set. Configure your Jules API key to use this adapter."
            )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def _post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        self._require()
        r = self._http.post(path, json=body)
        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After")
            raise JulesRateLimitError(
                "Jules API rate limit exceeded",
                retry_after_seconds=int(retry_after) if retry_after else None,
            )
        r.raise_for_status()
        return r.json() if r.text else {}

    def _get(self, path: str) -> Dict[str, Any]:
        self._require()
        r = self._http.get(path)
        r.raise_for_status()
        return r.json() if r.text else {}

    # --- Sessions --------------------------------------------------------

    def create_session(self, prompt: str, source_repo: str, title: str = "") -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "prompt": prompt,
            "source": {"repo": source_repo},
        }
        if title:
            body["title"] = title
        return self._post("/sessions", body)

    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        return self._post(f"/sessions/{session_id}:sendMessage", {"message": message})

    def approve_plan(self, session_id: str) -> Dict[str, Any]:
        return self._post(f"/sessions/{session_id}:approvePlan", {})

    def list_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        self._require()
        r = self._http.get("/sessions", params={"pageSize": limit})
        r.raise_for_status()
        data = r.json()
        return data.get("sessions", []) if isinstance(data, dict) else []

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self._get(f"/sessions/{session_id}")

    def get_activities(self, session_id: str) -> List[Dict[str, Any]]:
        self._require()
        r = self._http.get(f"/sessions/{session_id}/activities")
        r.raise_for_status()
        data = r.json()
        return data.get("activities", []) if isinstance(data, dict) else []

    # --- High-level dispatch --------------------------------------------

    def dispatch_task(self, task: JulesTask, source_repo: str) -> Dict[str, Any]:
        """Dispatch a JulesTask with rate-limit awareness."""
        if not self.tracker.can_dispatch():
            raise JulesRateLimitError(
                f"Daily limit reached: {self.tracker.snapshot()}",
                retry_after_seconds=None,
            )
        prompt_parts = [
            task.description,
            "",
            "Acceptance criteria:",
            *[f"- {c}" for c in task.acceptance_criteria],
            "",
            "Relevant files:",
            *[f"- {f}" for f in task.files],
        ]
        prompt = "\n".join(prompt_parts)
        self.tracker.record_dispatch()
        try:
            response = self.create_session(prompt=prompt, source_repo=source_repo, title=task.title)
        except Exception:
            self.tracker.record_completion()
            raise
        return {
            "task_id": task.id,
            "session_id": response.get("name", response.get("id")),
            "title": task.title,
            "rate_limit": self.tracker.snapshot(),
        }
