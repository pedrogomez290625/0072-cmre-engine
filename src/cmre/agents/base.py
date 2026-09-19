"""LLM client interface and default implementations.

The CMRE engine never imports a concrete LLM SDK directly. All LLM calls go
through an ``LLMClient`` protocol. This lets the same code path run against:
- Antigravity CLI (default, local, free)
- Gemini API (cloud, paid)
- Mock (offline, CI)

Adding a new backend = writing one class that satisfies this protocol.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from typing import Any, Dict, List, Optional, Protocol

import httpx

from ..config import Settings, get_settings


class LLMClient(Protocol):
    def complete(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str: ...
    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str, **kwargs: Any) -> Dict[str, Any]: ...
    def embed(self, texts: List[str]) -> List[List[float]]: ...
    @property
    def name(self) -> str: ...


# ---------------------------------------------------------------------------
# Mock — used in CI and offline mode
# ---------------------------------------------------------------------------

class MockLLMClient:
    name = "mock"

    def complete(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        return json.dumps({"stub": True, "system": system_prompt[:80]})

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str, **kwargs: Any) -> Dict[str, Any]:
        if schema_name == "ArtifactCandidateList":
            return {"artifacts": []}
        if schema_name == "ClaimDraftList":
            return {"claims": []}
        if schema_name == "ProblemDNA":
            return {}
        return {}

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Deterministic zero-vector; useful only for smoke tests.
        return [[0.0] * 16 for _ in texts]


# ---------------------------------------------------------------------------
# Antigravity — local models via the Antigravity CLI HTTP endpoint
# ---------------------------------------------------------------------------

class AntigravityClient:
    """Talks to a local Antigravity CLI HTTP endpoint.

    By default the CLI is expected to expose an OpenAI-compatible interface at
    ``CMRE_ANTIGRAVITY_BASE_URL``. If it does not, we can fall back to invoking
    the CLI as a subprocess.
    """

    name = "antigravity"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self._http = httpx.Client(
            base_url=self.settings.antigravity_base_url,
            timeout=self.settings.antigravity_timeout_seconds,
        )

    def complete(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        payload = {
            "model": self.settings.antigravity_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": kwargs.get("temperature", 0.2),
        }
        try:
            r = self._http.post("/v1/chat/completions", json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]
        except Exception:
            return self._subprocess_fallback(system_prompt, user_prompt)

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str, **kwargs: Any) -> Dict[str, Any]:
        text = self.complete(
            system_prompt + "\n\nReturn only valid JSON. Schema hint: " + schema_name,
            user_prompt,
            temperature=kwargs.get("temperature", 0.1),
        )
        try:
            return json.loads(text)
        except Exception:
            return {}

    def embed(self, texts: List[str]) -> List[List[float]]:
        try:
            r = self._http.post("/v1/embeddings", json={"input": texts})
            r.raise_for_status()
            data = r.json()
            return [d["embedding"] for d in data["data"]]
        except Exception:
            return [[0.0] * self.settings.embedding_dim for _ in texts]

    def _subprocess_fallback(self, system_prompt: str, user_prompt: str) -> str:
        """Run Antigravity CLI as a subprocess if HTTP fails.

        The exact CLI invocation depends on the installed version. This is a
        best-effort fallback so the system stays usable when the daemon is
        down.
        """
        try:
            proc = subprocess.run(
                ["agy", "complete", "--system", system_prompt, "--user", user_prompt],
                capture_output=True,
                text=True,
                timeout=self.settings.antigravity_timeout_seconds,
            )
            if proc.returncode == 0:
                return proc.stdout
        except Exception:
            pass
        return ""


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_llm_client(settings: Optional[Settings] = None) -> LLMClient:
    """Pick the best available client.

    Priority:
    1. Antigravity (local, free, default).
    2. Gemini (cloud, requires key, optional).
    3. Mock (last resort).
    """
    settings = settings or get_settings()

    # Try Antigravity first.
    try:
        return AntigravityClient(settings)
    except Exception:
        pass

    # Then Gemini if configured.
    if settings.gemini_api_key:
        try:
            from .gemini_client import GeminiClient  # lazy import
            return GeminiClient(settings)
        except Exception:
            pass

    return MockLLMClient()
