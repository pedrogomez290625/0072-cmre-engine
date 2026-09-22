"""Kaggle Connector for CMRE.

Handles authentication, competition kernel harvesting, and metadata retrieval.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import certifi
    os.environ["SSL_CERT_FILE"] = certifi.where()
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
except ImportError:
    pass

CREDS_BASE = Path(r"C:\Users\rafae\.gemini\01_PROYECTOS\0072-cmre-engine-datos\kaggle-credenciales")


class KaggleConnector:
    """Industrial Kaggle API connector supporting dual-account routing."""

    def __init__(self, account_type: str = "oficial"):
        self.account_type = account_type
        self.username = ""
        self._authenticate()

    def _authenticate(self) -> None:
        """Configure credentials from disk or environment."""
        if not os.environ.get("KAGGLE_USERNAME") or not os.environ.get("KAGGLE_KEY"):
            target_file = (
                CREDS_BASE / "pedrogomez290625@gmail.com" / "kaggle.json"
                if self.account_type.lower() in ("pedro", "sandbox")
                else CREDS_BASE / "cuenta-oficial" / "kaggle.json"
            )
            if target_file.exists():
                try:
                    data = json.loads(target_file.read_text(encoding="utf-8"))
                    os.environ["KAGGLE_USERNAME"] = data["username"]
                    os.environ["KAGGLE_KEY"] = data["key"]
                    self.username = data["username"]
                except Exception as e:
                    print(f"[WARN] No se pudieron cargar credenciales de {target_file}: {e}")
        else:
            self.username = os.environ.get("KAGGLE_USERNAME", "")

        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            self.api = KaggleApi()
            self.api.authenticate()
        except Exception as e:
            raise RuntimeError(f"Error al inicializar KaggleApi: {e}")

    def list_top_kernels(
        self,
        competition_slug: str,
        sort_by: str = "scoreDescending",
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Fetch metadata for top kernels in a competition."""
        kernels = self.api.kernels_list(
            competition=competition_slug,
            sort_by=sort_by,
            page_size=page_size
        )
        catalog = []
        for idx, k in enumerate(kernels, start=1):
            ref = getattr(k, "ref", "")
            slug = getattr(k, "slug", ref.split("/")[-1] if "/" in ref else ref)
            votes = getattr(k, "total_votes", getattr(k, "totalVotes", 0))
            score = getattr(k, "best_public_score", getattr(k, "bestPublicScore", "N/A"))
            catalog.append({
                "rank": idx,
                "author": getattr(k, "author", ""),
                "title": getattr(k, "title", ""),
                "ref": ref,
                "slug": slug,
                "votes": votes,
                "score": score,
                "url": f"https://www.kaggle.com/code/{ref}"
            })
        return catalog

    def download_kernel(self, kernel_ref: str, output_dir: Path) -> Optional[Path]:
        """Download a single kernel into the destination directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        try:
            self.api.kernels_pull(kernel_ref, path=str(output_dir))
            for f in output_dir.glob("*"):
                if f.suffix in (".ipynb", ".py"):
                    return f
        except Exception as e:
            print(f"[ERROR] Falló descarga de {kernel_ref}: {e}")
        return None
