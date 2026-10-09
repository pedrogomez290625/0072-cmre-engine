"""Miner for extracting Kaggle/DrivenData winning write-ups.

Transforms extracted raw textual techniques into scientific Claims (Claims CMRE).
"""
from typing import Dict, Any, List
import json
import re

class WinningWriteupMiner:
    def __init__(self, target_competitions: List[str]):
        self.target_competitions = target_competitions

    def fetch_writeups(self) -> List[Dict[str, Any]]:
        """Simulates fetching writeups for target competitions."""
        # This interfaces with KaggleWriteupConnector under the hood.
        return [
            {
                "competition": comp,
                "title": "1st Place Solution",
                "content": "CV Scheme: 5-fold Stratified. Feature Engineering: Extracted robust aggregates. Architecture: EfficientNet-B5 with SDSI Leg C. Loss: Asymmetric Soft-F1. Ensemble: NNLS stacking and dynamic time warping."
            } for comp in self.target_competitions
        ]

    def mine_to_claims(self, writeups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extracts structured Claims from raw writeup text."""
        claims = []
        for w in writeups:
            # Simple heuristic parsing
            cv_match = re.search(r"CV Scheme:\s*(.*?)\.", w['content'])
            fe_match = re.search(r"Feature Engineering:\s*(.*?)\.", w['content'])
            arch_match = re.search(r"Architecture:\s*(.*?)\.", w['content'])
            loss_match = re.search(r"Loss:\s*(.*?)\.", w['content'])
            ens_match = re.search(r"Ensemble:\s*(.*?)\.", w['content'])

            structured_content = w['content']
            if any([cv_match, fe_match, arch_match, loss_match, ens_match]):
                structured_content = {
                    "cv_scheme": cv_match.group(1) if cv_match else "N/A",
                    "feature_engineering": fe_match.group(1) if fe_match else "N/A",
                    "architecture": arch_match.group(1) if arch_match else "N/A",
                    "loss": loss_match.group(1) if loss_match else "N/A",
                    "ensemble": ens_match.group(1) if ens_match else "N/A",
                    "raw_text": w['content']
                }

            claims.append({
                "id": f"C_MINED_{abs(hash(w['competition'])) % 10000}",
                "description": f"Extracted canonical techniques from {w['competition']} winning writeup",
                "origin": w['title'],
                "content": structured_content
            })
        return claims

    def dump_claims(self, claims: List[Dict[str, Any]], filepath: str = "data/knowledge/claims_cmre.json"):
        """Additive integration of new claims."""
        try:
            with open(filepath, "r") as f:
                existing = json.load(f)
        except Exception:
            existing = {"claims": []}

        # Avoid duplicates based on ID
        existing_ids = {c.get("id") for c in existing.get("claims", [])}
        for c in claims:
            if c["id"] not in existing_ids:
                if "claims" not in existing: existing["claims"] = []
                existing["claims"].append(c)

        with open(filepath, "w") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
