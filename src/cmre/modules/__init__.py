"""CMRE Canonical Code Modules.

Six battle-tested modules extracted from elite Kaggle & platform winning solutions:
- MOD_INGEST: Fast 16-bit DICOM, Modality/VOI LUT, and breast/lesion ROI cropping.
- MOD_SIGNAL: Hierarchical group delta aggregations & Bayesian OOF target encoding.
- MOD_SPLIT: Group-disjoint, purged time-series, and molecular scaffold cross-validation.
- MOD_LOSS: Asymmetric and Soft-F1 losses for extreme medical/competition class imbalance.
- MOD_ENSEMBLE: Non-negative least squares (NNLS) and rank-average ensembling.
- MOD_HPC: Packed bitset popcount (Tanimoto/Hamming) and Disjoint Set Union (DSU).
"""

from .ensemble import SimpleNNLSBlender, rank_average_predictions
from .hpc import BitsetFingerprint, DisjointSetUnion, popcount64
from .ingest import find_breast_bounding_box, process_dicom_array
from .loss import asymmetric_loss_numpy, soft_f1_score_numpy
from .registry import CLAIM_MODULE_MAP, get_module_for_claim
from .signal import BayesianOofTargetEncoder, compute_group_delta_stats
from .split import group_disjoint_kfold, molecular_scaffold_split, purged_timeseries_split

__all__ = [
    "process_dicom_array",
    "find_breast_bounding_box",
    "compute_group_delta_stats",
    "BayesianOofTargetEncoder",
    "group_disjoint_kfold",
    "purged_timeseries_split",
    "molecular_scaffold_split",
    "asymmetric_loss_numpy",
    "soft_f1_score_numpy",
    "SimpleNNLSBlender",
    "rank_average_predictions",
    "BitsetFingerprint",
    "DisjointSetUnion",
    "popcount64",
    "CLAIM_MODULE_MAP",
    "get_module_for_claim",
]
