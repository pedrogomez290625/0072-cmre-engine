"""Unit tests for CMRE Canonical Code Modules (Paso 3).

Tests the 6 canonical modules:
- MOD_INGEST
- MOD_SIGNAL
- MOD_SPLIT
- MOD_LOSS
- MOD_ENSEMBLE
- MOD_HPC
And the claim-to-module registry.
"""

import pytest

from cmre.modules import (
    BitsetFingerprint,
    DisjointSetUnion,
    SimpleNNLSBlender,
    asymmetric_loss_numpy,
    compute_group_delta_stats,
    find_breast_bounding_box,
    get_module_for_claim,
    group_disjoint_kfold,
    molecular_scaffold_split,
    popcount64,
    process_dicom_array,
    purged_timeseries_split,
    rank_average_predictions,
    soft_f1_score_numpy,
)
from cmre.modules.signal import BayesianOofTargetEncoder


# ---------------------------------------------------------------------------
# MOD_INGEST Tests
# ---------------------------------------------------------------------------

def test_process_dicom_array_rescale_and_windowing():
    pixels = [100, 200, 300, 400]
    metadata = {
        "RescaleSlope": 2.0,
        "RescaleIntercept": -50.0,
        "PhotometricInterpretation": "MONOCHROME2",
        "WindowCenter": 350.0,
        "WindowWidth": 400.0,
    }
    processed = process_dicom_array(pixels, metadata)
    assert len(processed) == 4
    # All values normalized in [0, 1]
    assert all(0.0 <= v <= 1.0 for v in processed)


def test_process_dicom_array_monochrome1_inversion():
    pixels = [10, 50, 90]
    metadata = {
        "PhotometricInterpretation": "MONOCHROME1",
    }
    processed = process_dicom_array(pixels, metadata, apply_voi_lut=False)
    # Max is 90, so inversion is [90-10, 90-50, 90-90] = [80, 40, 0]
    assert processed == [80, 40, 0]


def test_find_breast_bounding_box_dummy():
    bbox = find_breast_bounding_box([[0, 0], [0, 1]])
    assert len(bbox) == 4


# ---------------------------------------------------------------------------
# MOD_SIGNAL Tests
# ---------------------------------------------------------------------------

def test_compute_group_delta_stats():
    rows = [
        {"patient_id": "P1", "measurement": 10.0},
        {"patient_id": "P1", "measurement": 20.0},
        {"patient_id": "P2", "measurement": 100.0},
    ]
    means, deltas = compute_group_delta_stats(rows, "patient_id", "measurement")
    assert means["P1"] == 15.0
    assert means["P2"] == 100.0
    # Deltas: P1: 10 - 15 = -5; 20 - 15 = 5; P2: 100 - 100 = 0
    assert deltas == [-5.0, 5.0, 0.0]


def test_bayesian_oof_target_encoder():
    categories = ["A", "A", "B", "B", "C"]
    targets = [1.0, 1.0, 0.0, 0.0, 1.0]

    encoder = BayesianOofTargetEncoder(m_smoothing=10.0, noise_level=0.0)
    encoder.fit(categories, targets)
    
    encoded = encoder.transform(["A", "B", "Unknown"])
    assert len(encoded) == 3
    # A has mean 1.0, B has mean 0.0, Unknown has global mean (3/5 = 0.6)
    assert encoded[0] > encoded[1]
    assert encoded[2] == pytest.approx(0.6, abs=1e-3)


# ---------------------------------------------------------------------------
# MOD_SPLIT Tests
# ---------------------------------------------------------------------------

def test_group_disjoint_kfold_no_overlap():
    groups = ["pt_1", "pt_1", "pt_2", "pt_2", "pt_3", "pt_4", "pt_5"]
    folds = group_disjoint_kfold(groups, n_splits=3)
    
    for tr_idx, va_idx in folds:
        tr_groups = {groups[i] for i in tr_idx}
        va_groups = {groups[i] for i in va_idx}
        # Intersect must be empty (0 group leakage)
        assert len(tr_groups.intersection(va_groups)) == 0


def test_purged_timeseries_split_causal():
    timestamps = list(range(100))
    folds = purged_timeseries_split(timestamps, n_splits=4, embargo_pct=0.02)
    assert len(folds) >= 3
    for tr_idx, va_idx in folds:
        assert max(tr_idx) < min(va_idx)


def test_molecular_scaffold_split():
    scaffolds = ["benzene", "benzene", "pyridine", "indole", "indole", "furan"]
    tr_idx, te_idx = molecular_scaffold_split(scaffolds, test_ratio=0.33)
    
    tr_scaffolds = {scaffolds[i] for i in tr_idx}
    te_scaffolds = {scaffolds[i] for i in te_idx}
    # No scaffold overlap
    assert len(tr_scaffolds.intersection(te_scaffolds)) == 0


# ---------------------------------------------------------------------------
# MOD_LOSS Tests
# ---------------------------------------------------------------------------

def test_asymmetric_loss_calculation():
    y_true = [1.0, 0.0, 0.0, 0.0]
    y_pred = [0.9, 0.01, 0.05, 0.8]  # Last is a false positive
    loss = asymmetric_loss_numpy(y_true, y_pred)
    assert loss > 0.0


def test_soft_f1_score_calculation():
    y_true = [1.0, 1.0, 0.0, 0.0]
    y_pred = [0.95, 0.90, 0.05, 0.10]
    score = soft_f1_score_numpy(y_true, y_pred)
    assert score > 0.85


# ---------------------------------------------------------------------------
# MOD_ENSEMBLE Tests
# ---------------------------------------------------------------------------

def test_rank_average_predictions():
    # Model 1 has scale [0, 100], Model 2 has scale [0, 1]
    m1 = [10.0, 50.0, 90.0]
    m2 = [0.1, 0.5, 0.9]
    avg = rank_average_predictions([m1, m2])
    assert avg[0] < avg[1] < avg[2]


def test_simple_nnls_blender():
    m1 = [1.0, 0.0, 1.0, 0.0]
    m2 = [0.0, 1.0, 0.0, 1.0]
    y_true = [1.0, 0.0, 1.0, 0.0]  # M1 is a perfect predictor

    blender = SimpleNNLSBlender(max_iter=200, lr=0.1)
    blender.fit([m1, m2], y_true)
    
    # Weight for M1 should be dominant
    assert blender.weights[0] > blender.weights[1]
    assert sum(blender.weights) == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# MOD_HPC Tests
# ---------------------------------------------------------------------------

def test_popcount64():
    assert popcount64(0b10110) == 3
    assert popcount64(0) == 0
    assert popcount64(0xFFFFFFFFFFFFFFFF) == 64


def test_bitset_fingerprint_tanimoto():
    # 0b1110 and 0b1010 -> intersection=2 (bits 1,3), union=3 (bits 1,2,3) -> 2/3
    fp1 = BitsetFingerprint([14])
    fp2 = BitsetFingerprint([10])
    sim = fp1.tanimoto_similarity(fp2)
    assert sim == pytest.approx(2.0 / 3.0)


def test_disjoint_set_union():
    dsu = DisjointSetUnion(5)
    assert dsu.num_components == 5
    dsu.union(0, 1)
    dsu.union(1, 2)
    assert dsu.find(0) == dsu.find(2)
    assert dsu.num_components == 3
    assert dsu.component_size(0) == 3


# ---------------------------------------------------------------------------
# Registry Tests
# ---------------------------------------------------------------------------

def test_get_module_for_claim():
    info = get_module_for_claim("FC03")
    assert info is not None
    assert info["module"] == "MOD_INGEST"
    assert "RSNA" in info["description"]

    info_c01 = get_module_for_claim("[C01] Group Disjoint Cv")
    assert info_c01 is not None
    assert info_c01["module"] == "MOD_SPLIT"

# ---------------------------------------------------------------------------
# PyTorch Module Gradcheck Tests
# ---------------------------------------------------------------------------
import torch

def test_asymmetric_loss_gradcheck():
    from cmre.modules.loss import AsymmetricLoss
    # Use float64 for gradcheck
    x = torch.randn(2, 3, dtype=torch.float64, requires_grad=True)
    y = torch.randint(0, 2, (2, 3)).to(torch.float64)
    loss_fn = AsymmetricLoss(gamma_neg=4.0, gamma_pos=1.0, clip=0.05, eps=1e-8)

    # Check gradients using gradcheck
    assert torch.autograd.gradcheck(loss_fn, (x, y), eps=1e-6, atol=1e-4)

def test_soft_f1_loss_gradcheck():
    from cmre.modules.loss import SoftF1Loss
    # Use float64 for gradcheck
    x = torch.randn(2, 3, dtype=torch.float64, requires_grad=True)
    y = torch.randint(0, 2, (2, 3)).to(torch.float64)
    loss_fn = SoftF1Loss(eps=1e-7)

    # Check gradients using gradcheck
    assert torch.autograd.gradcheck(loss_fn, (x, y), eps=1e-6, atol=1e-4)
