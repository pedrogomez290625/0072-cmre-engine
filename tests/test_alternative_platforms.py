"""
Unit tests for CMRE Alternative Platforms (DrivenData & Zindi) and Post-Mortems Integration.

Tests:
- MOD_ALTERNATIVE:
  * MultiTargetClassifierChainCalibrator (Flu Shot Learning)
  * OrdinalDamageClassifier & Nelder-Mead Thresholds (Richter's Predictor)
  * SpatioTemporalLagBlender (Zindi AirQo)
  * BiometricReIDArcFaceModeler (Zindi Turtle Recall)
- LEAK_AUDITOR Post-Mortem Autopsy Matching (Wall of Shame cross-reference)

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

import pytest
import numpy as np

from cmre.modules.alternative_platforms import (
    MultiTargetClassifierChainCalibrator,
    OrdinalDamageClassifier,
    SpatioTemporalLagBlender,
    BiometricReIDArcFaceModeler,
)
from cmre.services.leak_auditor import LeakAuditor


# ---------------------------------------------------------------------------
# 1. DrivenData Flu Shot Tests
# ---------------------------------------------------------------------------

def test_multitarget_missing_indicators():
    features = np.array([
        [1.0, np.nan, 3.0],
        [np.nan, 2.0, np.nan],
    ], dtype=np.float32)
    
    missing_ind = MultiTargetClassifierChainCalibrator.extract_missing_indicators(features)
    assert missing_ind.shape == (2, 3)
    assert missing_ind[0, 1] == 1.0
    assert missing_ind[0, 0] == 0.0
    assert missing_ind[1, 2] == 1.0


def test_multitarget_chain_conditional_probability():
    prob_y1 = np.array([0.8, 0.2], dtype=np.float32)
    p_y2_given_y1 = np.array([0.9, 0.7], dtype=np.float32)
    p_y2_given_y0 = np.array([0.1, 0.05], dtype=np.float32)
    
    marginal_y2 = MultiTargetClassifierChainCalibrator.chain_conditional_probability(
        prob_y1, p_y2_given_y1, p_y2_given_y0
    )
    # Expected:
    # idx 0: 0.9 * 0.8 + 0.1 * 0.2 = 0.72 + 0.02 = 0.74
    # idx 1: 0.7 * 0.2 + 0.05 * 0.8 = 0.14 + 0.04 = 0.18
    np.testing.assert_allclose(marginal_y2, [0.74, 0.18], rtol=1e-5)


# ---------------------------------------------------------------------------
# 2. DrivenData Richter's Predictor Tests
# ---------------------------------------------------------------------------

def test_ordinal_damage_slenderness():
    heights = np.array([10.0, 20.0, 5.0], dtype=np.float32)
    areas = np.array([25.0, 16.0, 100.0], dtype=np.float32)
    slender = OrdinalDamageClassifier.compute_slenderness_features(heights, areas)
    
    # 10 / sqrt(25) = 10 / 5 = 2.0
    # 20 / sqrt(16) = 20 / 4 = 5.0
    # 5 / sqrt(100) = 5 / 10 = 0.5
    np.testing.assert_allclose(slender, [2.0, 5.0, 0.5], rtol=1e-4)


def test_ordinal_damage_probabilities_and_nelder_mead():
    # Test monotonic conversion
    p_ge_2 = np.array([0.8, 0.4, 0.1], dtype=np.float32)
    p_ge_3 = np.array([0.5, 0.2, 0.05], dtype=np.float32)
    probs = OrdinalDamageClassifier.cumulative_to_multiclass_probs(p_ge_2, p_ge_3)
    
    assert probs.shape == (3, 3)
    # Each row must sum to 1.0
    np.testing.assert_allclose(np.sum(probs, axis=1), [1.0, 1.0, 1.0], rtol=1e-5)
    
    # Test Nelder-Mead threshold search
    scores = np.array([0.1, 0.2, 0.4, 0.5, 0.8, 0.9], dtype=np.float32)
    y_true = np.array([1, 1, 2, 2, 3, 3], dtype=np.int64)
    
    clf = OrdinalDamageClassifier(thresholds=(0.3, 0.7))
    th1, th2 = clf.optimize_thresholds_nelder_mead(scores, y_true)
    assert 0.0 < th1 < th2 < 1.0
    
    preds = clf.predict_classes_from_latent(scores, (th1, th2))
    assert np.mean(preds == y_true) >= 0.83  # At least 5/6 or 6/6 correct


# ---------------------------------------------------------------------------
# 3. Zindi AirQo Spatio-Temporal Tests
# ---------------------------------------------------------------------------

def test_spatio_temporal_harmonics_and_lags():
    hours = np.array([0.0, 6.0, 12.0, 18.0], dtype=np.float32)
    sin_h, cos_h = SpatioTemporalLagBlender.compute_diurnal_harmonics(hours)
    
    # At hour 0: sin=0, cos=1
    # At hour 6: sin=1, cos=0
    # At hour 12: sin=0, cos=-1
    # At hour 18: sin=-1, cos=0
    np.testing.assert_allclose(sin_h, [0.0, 1.0, 0.0, -1.0], atol=1e-5)
    np.testing.assert_allclose(cos_h, [1.0, 0.0, -1.0, 0.0], atol=1e-5)
    
    series = np.array([10.0, 15.0, 20.0, 25.0], dtype=np.float32)
    lags = SpatioTemporalLagBlender.compute_temporal_lags(series, lags=[1, 2])
    assert "lag_1" in lags and "lag_2" in lags
    np.testing.assert_allclose(lags["lag_1"], [10.0, 10.0, 15.0, 20.0])
    
    # Blending test
    pred_gbdt = np.array([50.0, 60.0])
    pred_knn = np.array([40.0, 50.0])
    blend = SpatioTemporalLagBlender.blend_gbdt_and_geoknn(pred_gbdt, pred_knn, w_gbdt=0.8)
    np.testing.assert_allclose(blend, [48.0, 58.0])


# ---------------------------------------------------------------------------
# 4. Zindi Turtle Recall ArcFace Tests
# ---------------------------------------------------------------------------

def test_biometric_arcface_and_open_set():
    modeler = BiometricReIDArcFaceModeler(scale=10.0, margin=0.2, open_set_threshold=0.5)
    
    # Cosine similarities for 2 samples, 3 classes
    cos_sim = np.array([
        [0.8, 0.2, 0.1],
        [0.1, 0.9, 0.2],
    ], dtype=np.float32)
    labels = np.array([0, 1], dtype=np.int64)
    
    penalized = modeler.compute_arcface_margin(cos_sim, labels)
    assert penalized.shape == (2, 3)
    # The target logit has margin penalty applied: cos(theta + m) < cos(theta)
    assert penalized[0, 0] < modeler.scale * cos_sim[0, 0]
    
    # Open-Set prediction test
    gallery_embs = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ], dtype=np.float32)
    gallery_labels = ["turtle_alpha", "turtle_beta"]
    
    query_embs = np.array([
        [0.99, 0.01, 0.0],  # Very close to alpha
        [0.0, 0.0, 1.0],    # Orthogonal to both -> should be 'new_turtle'
    ], dtype=np.float32)
    
    preds = modeler.predict_open_set(query_embs, gallery_embs, gallery_labels)
    assert preds[0] == "turtle_alpha"
    assert preds[1] == "new_turtle"


# ---------------------------------------------------------------------------
# 5. LeakAuditor Post-Mortem Matching Tests
# ---------------------------------------------------------------------------

def test_leak_auditor_postmortem_autopsy_matching():
    matches_mammography = LeakAuditor.match_postmortem_autopsies(
        has_groups=True,
        imbalance="high"
    )
    case_ids = [m["case_id"] for m in matches_mammography]
    assert "FAIL_01" in case_ids  # RSNA pF1 threshold collapse
    assert "FAIL_05" in case_ids  # ISIC Patient Identity leak
    
    matches_optiver = LeakAuditor.match_postmortem_autopsies(has_temporal=True)
    assert any(m["case_id"] == "FAIL_02" for m in matches_optiver)
    
    matches_casmi = LeakAuditor.match_postmortem_autopsies(has_scaffolds=True)
    assert any(m["case_id"] == "FAIL_04" for m in matches_casmi)
