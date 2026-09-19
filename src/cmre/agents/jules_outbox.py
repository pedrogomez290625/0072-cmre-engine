"""Jules outbox helper.

Reads `.jules/tasks.yaml`, dispatches each task via JulesAPIAdapter, and
writes results to `.jules/outbox.jsonl`. Independent from the legacy
`agents/jules.py` stub.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import structlog
import yaml

from ..config import Settings, get_settings
from ..schemas import JulesTask
from .jules_api import JulesAPIAdapter, JulesNotConfiguredError, JulesRateLimitError

log = structlog.get_logger("cmre.agents.jules_outbox")


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_tasks_file(path: Path) -> List[dict]:
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        log.warning("jules_tasks_yaml_failed", error=str(exc))
        return []
    if not isinstance(data, dict):
        return []
    return data.get("tasks") or []


def dispatch_from_yaml(
    tasks_file: str | Path,
    outbox_file: str | Path,
    repo: str,
    settings: Optional[Settings] = None,
) -> List[dict]:
    """Read tasks.yaml, dispatch each, append results to outbox.

    Returns list of dispatch records (one per task).
    """
    settings = settings or get_settings()
    tasks_path = Path(tasks_file)
    outbox_path = Path(outbox_file)
    outbox_path.parent.mkdir(parents=True, exist_ok=True)

    raw = _load_tasks_file(tasks_path)
    records: list[dict] = []

    try:
        adapter = JulesAPIAdapter(settings)
    except JulesNotConfiguredError as exc:
        log.warning("jules_adapter_not_configured", error=str(exc))
        # Write a single record explaining and return
        record = {"timestamp": _utcnow_iso(), "error": str(exc)}
        outbox_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
        return [record]

    with outbox_path.open("a", encoding="utf-8") as f:
        for t in raw:
            try:
                task = JulesTask.model_validate(t)
            except Exception as exc:
                rec = {"timestamp": _utcnow_iso(), "error": "invalid_task", "detail": str(exc), "raw": t}
                f.write(json.dumps(rec) + "\n")
                records.append(rec)
                continue
            try:
                resp = adapter.dispatch_task(task, source_repo=repo)
                rec = {"timestamp": _utcnow_iso(), **resp}
            except JulesRateLimitError as exc:
                rec = {
                    "timestamp": _utcnow_iso(),
                    "task_id": t.get("id"),
                    "error": "rate_limited",
                    "detail": str(exc),
                }
                f.write(json.dumps(rec) + "\n")
                records.append(rec)
                # stop dispatching further tasks once rate-limited
                break
            except Exception as exc:
                rec = {
                    "timestamp": _utcnow_iso(),
                    "task_id": t.get("id"),
                    "error": "dispatch_failed",
                    "detail": str(exc),
                }
                f.write(json.dumps(rec) + "\n")
                records.append(rec)
                continue
            f.write(json.dumps(rec) + "\n")
            records.append(rec)

    return records
