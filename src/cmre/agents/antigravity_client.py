"""Enhanced Antigravity CLI client.

Antigravity is the local coding agent that talks to local models. It exposes
either:
- an OpenAI-compatible HTTP endpoint (preferred)
- a `agy` CLI command (fallback)

We probe availability first; if neither path works, the factory in
`cmre.agents.base` falls back to MockLLMClient.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any, Dict, List, Optional

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import Settings, get_settings
from .base import LLMClient

log = structlog.get_logger("cmre.agents.antigravity")


class AntigravityClient:
    name = "antigravity"

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self._http: Optional[httpx.Client] = None
        self._probe()

    def _probe(self) -> None:
        try:
            client = httpx.Client(
                base_url=self.settings.antigravity_base_url,
                timeout=2.0,
            )
            r = client.get("/v1/models")
            if r.status_code < 500:
                self._http = httpx.Client(
                    base_url=self.settings.antigravity_base_url,
                    timeout=self.settings.antigravity_timeout_seconds,
                )
                log.info("antigravity_http_endpoint_ok", base=self.settings.antigravity_base_url)
        except Exception as exc:
            log.warning("antigravity_http_unavailable", error=str(exc))
            self._http = None

    def is_available(self) -> bool:
        return self._http is not None or self._cli_available()

    def _cli_available(self) -> bool:
        try:
            r = subprocess.run(["which", "agy"], capture_output=True, text=True, timeout=2)
            return r.returncode == 0
        except Exception:
            return False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def _http_complete(self, system_prompt: str, user_prompt: str, temperature: float) -> Optional[str]:
        if self._http is None:
            return None
        payload = {
            "model": self.settings.antigravity_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        r = self._http.post("/v1/chat/completions", json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

    def _cli_complete(self, system_prompt: str, user_prompt: str) -> str:
        try:
            proc = subprocess.run(
                ["agy", "complete", "--system", system_prompt, "--user", user_prompt],
                capture_output=True,
                text=True,
                timeout=self.settings.antigravity_timeout_seconds,
            )
            if proc.returncode == 0:
                return proc.stdout
        except Exception as exc:
            log.warning("antigravity_cli_failed", error=str(exc))
        return ""

    # --- LLMClient protocol ----------------------------------------------

    def complete(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        temperature = float(kwargs.get("temperature", 0.2))
        text = self._http_complete(system_prompt, user_prompt, temperature)
        if text is None:
            text = self._cli_complete(system_prompt, user_prompt)
        return text or json.dumps({"error": "antigravity_unavailable"})

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
        if self._http is None:
            return [[0.0] * self.settings.embedding_dim for _ in texts]
        try:
            r = self._http.post("/v1/embeddings", json={"input": texts})
            r.raise_for_status()
            data = r.json()
            return [d["embedding"] for d in data["data"]]
        except Exception as exc:
            log.warning("antigravity_embed_failed", error=str(exc))
            return [[0.0] * self.settings.embedding_dim for _ in texts]

    def embed_with_fallback(self, texts: List[str]) -> List[List[float]]:
        """Try Antigravity; fall back to deterministic hash embeddings."""
        vecs = self.embed(texts)
        if all(any(v != 0.0 for v in vec) for vec in vecs):
            return vecs
        # Hash fallback
        import hashlib

        out = []
        for text in texts:
            row = []
            seed = text.encode("utf-8") or b" "
            for i in range(self.settings.embedding_dim):
                digest = hashlib.sha1(seed + i.to_bytes(2, "big")).digest()
                row.append((digest[0] - 128) / 128.0)
            out.append(row)
        return out
