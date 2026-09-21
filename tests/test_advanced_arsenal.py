"""
Unit tests for CMRE Advanced Competitive & Medical Vision Arsenal (Paso 5).

Tests:
- MOD_HPC: SegmentTreeLazy, SimulatedAnnealingSelector, ChokudaiSearchOptimizer
- MOD_RADIOLOGY: CrossViewMammographyAttention, HanningWindowTiler, UglyDucklingPatientNormalizer
- LEAK_AUDITOR: LeakAuditor, LeakAuditResult (Anti-Shakeup Service)

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.modules.hpc_advanced import (
    SegmentTreeLazy,
    SimulatedAnnealingSelector,
    ChokudaiSearchOptimizer,
)
from cmre.modules.radiology_advanced import (
    HanningWindowTiler,
    UglyDucklingPatientNormalizer,
    CrossViewMammographyAttention,
    HAS_TORCH,
)
from cmre.services.leak_auditor import LeakAuditor, LeakAuditResult


# ---------------------------------------------------------------------------
# 1. HPC Advanced Tests
# ---------------------------------------------------------------------------

def test_segment_tree_lazy_sum():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    st = SegmentTreeLazy(data, op="sum")
    
    # Query total sum
    assert st.query_range(0, 4) == pytest.approx(15.0)
    # Query sub-range
    assert st.query_range(1, 3) == pytest.approx(9.0)
    
    # Range update: add 10 to indices [1, 3] -> [1, 12, 13, 14, 5]
    st.update_range(1, 3, 10.0)
    assert st.query_range(1, 3) == pytest.approx(39.0)
    assert st.query_range(0, 4) == pytest.approx(45.0)
    assert st.query_range(0, 0) == pytest.approx(1.0)
    assert st.query_range(4, 4) == pytest.approx(5.0)


def test_segment_tree_lazy_max_min():
    data = [10.0, 50.0, 30.0, 90.0, 20.0]
    st_max = SegmentTreeLazy(data, op="max")
    assert st_max.query_range(0, 4) == pytest.approx(90.0)
    assert st_max.query_range(0, 2) == pytest.approx(50.0)
    
    st_min = SegmentTreeLazy(data, op="min")
    assert st_min.query_range(0, 4) == pytest.approx(10.0)
    assert st_min.query_range(1, 3) == pytest.approx(30.0)


def test_simulated_annealing_selector():
    # 15 features, select best 3. Target optimal features are 3, 7, 11.
    target_set = {3, 7, 11}
    
    def eval_fn(features):
        return float(len(set(features).intersection(target_set)))
    
    sa = SimulatedAnnealingSelector(
        n_features=15,
        k_target=3,
        max_steps=500,
        initial_temp=5.0,
        cooling_rate=0.98,
        seed=42,
    )
    best_features, best_score = sa.fit(eval_fn)
    
    assert len(best_features) == 3
    assert best_score >= 2.0  # Should find at least 2 or all 3 optimal features
    assert all(0 <= f < 15 for f in best_features)


def test_chokudai_search_optimizer():
    # 3 models, ideal weights [0.5, 0.3, 0.2]
    ideal = [0.5, 0.3, 0.2]
    
    def eval_weights(weights):
        # Negative L2 distance to ideal weights
        dist = sum((w - id_w) ** 2 for w, id_w in zip(weights, ideal))
        return -dist
    
    chokudai = ChokudaiSearchOptimizer(
        n_models=3,
        beam_width=5,
        max_depth=10,
        time_limit_sec=0.2,
    )
    weights, best_score = chokudai.optimize(eval_weights)
    
    assert len(weights) == 3
    assert sum(weights) == pytest.approx(1.0, abs=1e-5)
    assert all(w >= 0.0 for w in weights)
    # The highest weight should be model 0
    assert weights[0] >= weights[1] >= weights[2]


# ---------------------------------------------------------------------------
# 2. Medical Vision & Radiology Advanced Tests
# ---------------------------------------------------------------------------

def test_hanning_window_tiler_grayscale():
    tiler = HanningWindowTiler(tile_size=128, stride=96)
    image = np.ones((256, 256), dtype=np.float32) * 5.0
    
    tiles = tiler.extract_tiles(image)
    assert len(tiles) > 0
    
    # Reconstruct from tiles
    reconstructed = tiler.reconstruct_from_tiles(tiles, (256, 256))
    assert reconstructed.shape == (256, 256)
    # The reconstructed flat constant image should closely match the original
    np.testing.assert_allclose(reconstructed, image, rtol=1e-2, atol=1e-2)


def test_hanning_window_tiler_multichannel():
    tiler = HanningWindowTiler(tile_size=64, stride=48)
    image = np.full((120, 120, 3), 2.5, dtype=np.float32)
    
    tiles = tiler.extract_tiles(image)
    reconstructed = tiler.reconstruct_from_tiles(tiles, (120, 120, 3))
    assert reconstructed.shape == (120, 120, 3)
    np.testing.assert_allclose(reconstructed, image, rtol=1e-2, atol=1e-2)


def test_ugly_duckling_patient_normalizer():
    # 4 lesions, 3 features
    lesions = np.array([
        [1.0, 2.0, 10.0],
        [1.1, 2.1, 10.2],
        [0.9, 1.9, 9.8],
        [5.0, 8.0, 50.0],  # Outlier lesion ("Ugly Duckling")
    ], dtype=np.float32)
    
    delta, ratio = UglyDucklingPatientNormalizer.normalize_lesions(lesions)
    assert delta.shape == (4, 3)
    assert ratio.shape == (4, 3)
    
    # The ugly duckling (index 3) should have much higher positive delta and ratio
    assert delta[3, 0] > delta[0, 0]
    assert ratio[3, 0] > 2.0


def test_cross_view_mammography_attention():
    if not HAS_TORCH:
        pytest.skip("PyTorch no instalado en el entorno actual")
        
    import torch
    model = CrossViewMammographyAttention(in_features=64, num_heads=2, dropout=0.0)
    model.eval()
    
    feat_cc = torch.randn(2, 64)
    feat_mlo = torch.randn(2, 64)
    
    logit, fused = model(feat_cc, feat_mlo)
    assert logit.shape == (2, 1)
    assert fused.shape == (2, 128)
    
    # Test gradient pass
    model.train()
    logit, _ = model(feat_cc, feat_mlo)
    loss = logit.sum()
    loss.backward()
    
    assert model.fc_fusion[0].weight.grad is not None


# ---------------------------------------------------------------------------
# 3. Anti-Shakeup Leak Auditor Tests
# ---------------------------------------------------------------------------

def test_leak_auditor_group_detection():
    # Patient groups
    groups = ["P1", "P2", "P3", "P4", "P1", "P5"]
    train_idx = [0, 1, 2]       # Groups: P1, P2, P3
    val_idx_leak = [4, 5]       # Groups: P1 (LEAK!), P5
    val_idx_clean = [3, 5]      # Groups: P4, P5
    
    res_leak = LeakAuditor.audit_split(train_idx, val_idx_leak, groups=groups)
    assert res_leak.has_leak is True
    assert res_leak.risk_score >= 0.5
    assert any("GROUP_LEAKAGE" in l for l in res_leak.detected_leaks)
    assert "SNIP_SPLIT_GROUP_PATIENT_DISJOINT (StratifiedGroupKFold)" in res_leak.prescribed_defenses
    
    res_clean = LeakAuditor.audit_split(train_idx, val_idx_clean, groups=groups)
    assert res_clean.has_leak is False
    assert res_clean.risk_score == 0.0


def test_leak_auditor_temporal_lookahead():
    timestamps = [100, 200, 300, 400, 500]
    train_idx = [0, 1, 4]  # Has t=500 in train
    val_idx = [2, 3]       # Has t=300, 400 in val (t=500 is in the future!)
    
    res = LeakAuditor.audit_split(train_idx, val_idx, timestamps=timestamps)
    assert res.has_leak is True
    assert any("TEMPORAL_LOOKAHEAD" in l for l in res.detected_leaks)
    assert "SNIP_SPLIT_PURGED_EMBARGO_TIME (PurgedGroupTimeSeriesSplit)" in res.prescribed_defenses


def test_leak_auditor_class_imbalance_warning():
    targets = [0] * 99 + [1]  # 1% positive rate
    train_idx = list(range(50))
    val_idx = list(range(50, 100))
    
    res = LeakAuditor.audit_split(train_idx, val_idx, targets=targets)
    assert len(res.warnings) > 0
    assert any("CLASS_IMBALANCE" in w for w in res.warnings)
    assert "SNIP_LOSS_ASYMMETRIC_CUDA (AsymmetricLoss)" in res.prescribed_defenses
    assert "SNIP_LOSS_SOFT_F1_WEIGHTED (SoftF1Loss)" in res.prescribed_defenses
