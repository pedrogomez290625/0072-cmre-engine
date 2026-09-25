"""Registry linking CMRE Claims to Canonical Code Modules and Templates."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from .ensemble import CODE_TEMPLATE_NNLS_BLEND
from .hpc import CODE_TEMPLATE_HPC_SIMD
from .ingest import CODE_TEMPLATE_DICOM_INGEST
from .loss import CODE_TEMPLATE_ASYMMETRIC_LOSS
from .signal import CODE_TEMPLATE_TARGET_ENCODER
from .split import CODE_TEMPLATE_PURGED_CV

CLAIM_MODULE_MAP: Dict[str, Dict[str, str]] = {
    "C01": {
        "module": "MOD_SPLIT",
        "mechanism": "group-disjoint-cv",
        "description": "Group-Disjoint K-Fold CV for patient/entity protection.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "C02": {
        "module": "MOD_SPLIT",
        "mechanism": "causal-time-split",
        "description": "Causal walk-forward split for temporal problems.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "C03": {
        "module": "MOD_SPLIT",
        "mechanism": "purged-embargo",
        "description": "Purged interval with temporal embargo.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "C05": {
        "module": "MOD_SIGNAL",
        "mechanism": "oof-target-encoding",
        "description": "Bayesian out-of-fold target encoding.",
        "template": CODE_TEMPLATE_TARGET_ENCODER,
    },
    "C07": {
        "module": "MOD_SIGNAL",
        "mechanism": "hierarchical-aggregations",
        "description": "Hierarchical multi-level group aggregations with delta trick.",
        "template": CODE_TEMPLATE_TARGET_ENCODER,
    },
    "C22": {
        "module": "MOD_ENSEMBLE",
        "mechanism": "rank-space-ensemble",
        "description": "Rank-space prediction averaging for uncalibrated models.",
        "template": CODE_TEMPLATE_NNLS_BLEND,
    },
    "C23": {
        "module": "MOD_ENSEMBLE",
        "mechanism": "nonnegative-blend",
        "description": "Non-Negative Least Squares (NNLS) OOF blend.",
        "template": CODE_TEMPLATE_NNLS_BLEND,
    },
    "C25": {
        "module": "MOD_INGEST",
        "mechanism": "dicom-physical-value-order",
        "description": "Standard physical DICOM preprocessing pipeline.",
        "template": CODE_TEMPLATE_DICOM_INGEST,
    },
    "C27": {
        "module": "MOD_LOSS",
        "mechanism": "imbalance-loss-ablation",
        "description": "Asymmetric and focal loss for extreme class imbalance.",
        "template": CODE_TEMPLATE_ASYMMETRIC_LOSS,
    },
    "FC01": {
        "module": "MOD_SIGNAL",
        "mechanism": "heterogeneous_gbdt_blend",
        "description": "Heterogeneous GBDT feature blending.",
        "template": CODE_TEMPLATE_TARGET_ENCODER,
    },
    "FC03": {
        "module": "MOD_INGEST",
        "mechanism": "dicom-roi-crop-convnext",
        "description": "RSNA Mammography DICOM ROI detection and ConvNeXt pipeline.",
        "template": CODE_TEMPLATE_DICOM_INGEST,
    },
    "FC06": {
        "module": "MOD_SPLIT",
        "mechanism": "chemical-scaffold-split",
        "description": "Bemis-Murcko molecular scaffold clustering split.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "FC07": {
        "module": "MOD_SPLIT",
        "mechanism": "climate-dengue-temporal-regression",
        "description": "Causal walk-forward split for epidemiological Dengue data.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "HPC01": {
        "module": "MOD_HPC",
        "mechanism": "packed-popcount-similarity",
        "description": "SIMD/Bitset popcount for Tanimoto and Hamming similarity.",
        "template": CODE_TEMPLATE_HPC_SIMD,
    },
    "HPC03": {
        "module": "MOD_HPC",
        "mechanism": "dsu-path-compression",
        "description": "Disjoint Set Union with path compression and rank union.",
        "template": CODE_TEMPLATE_HPC_SIMD,
    },
    "C31": {
        "module": "MOD_ENSEMBLE",
        "mechanism": "classwise-asymmetric-blending",
        "description": "Class-Wise Asymmetric Matrix Blending for multi-label radiology.",
        "template": CODE_TEMPLATE_NNLS_BLEND,
    },
    "C32": {
        "module": "MOD_HPC",
        "mechanism": "latency-bounded-pruning",
        "description": "Greedy Latency Budget Pruner for inference time guarantees.",
        "template": CODE_TEMPLATE_HPC_SIMD,
    },
    "C33": {
        "module": "MOD_SPLIT",
        "mechanism": "sirius-absence-axiom",
        "description": "SIRIUS neutral loss absence axiom filter against decoys.",
        "template": CODE_TEMPLATE_PURGED_CV,
    },
    "C34": {
        "module": "MOD_SIGNAL",
        "mechanism": "sdsi-hybrid-arbitration",
        "description": "Monotonic SDSI hybrid arbitration (symbolic + TTT neural).",
        "template": CODE_TEMPLATE_TARGET_ENCODER,
    },
    "C35": {
        "module": "MOD_SIGNAL",
        "mechanism": "anti-identity-fallback-guard",
        "description": "Guardián anti-identidad para prevenir colapso a 0.00 en grillas.",
        "template": CODE_TEMPLATE_TARGET_ENCODER,
    },
    "C36": {
        "module": "MOD_LOSS",
        "mechanism": "cuda-fp16-sanitization",
        "description": "Sanitización de tensores y normalización Float vs Double para FP16 CUDA.",
        "template": CODE_TEMPLATE_ASYMMETRIC_LOSS,
    },
}


def get_module_for_claim(claim_id_or_summary: str) -> Optional[Dict[str, str]]:
    """Finds canonical module mapping for a given claim ID or summary string."""
    # Check exact mechanism match first
    norm_text = claim_id_or_summary.replace("_", "-").lower()
    for cid, info in CLAIM_MODULE_MAP.items():
        if info["mechanism"].lower() in norm_text:
            return info

    # Check boundary-matched ID (e.g. 'FC03' won't match 'C03')
    for cid, info in CLAIM_MODULE_MAP.items():
        pattern = rf"(?:\b|\[){re.escape(cid)}(?:\b|\])"
        if re.search(pattern, claim_id_or_summary):
            return info

    return None
