from cmre.modules.ensemble import BimodalTabularVisionFusion

def test_bimodal_fusion_concat():
    fusion = BimodalTabularVisionFusion(tabular_dim=3, vision_dim=10, fusion_method="concat")
    tabular = [[25.0, 22.1, 1.0], [45.0, 28.5, 0.0]]  # Age, BMI, Prior
    vision = [
        [0.1] * 10,
        [0.2] * 10,
    ]

    fused = fusion.fuse(tabular, vision)
    assert len(fused) == 2
    assert len(fused[0]) == 10 + 64  # vision_dim + projected_tabular_dim
    assert fused[0][0] == 0.1

def test_bimodal_fusion_cross_attention():
    fusion = BimodalTabularVisionFusion(tabular_dim=3, vision_dim=5, fusion_method="cross_attention")
    tabular = [[25.0, 22.1, 1.0], [45.0, 28.5, 0.0]]
    vision = [
        [0.1] * 5,
        [0.2] * 5,
    ]

    fused = fusion.fuse(tabular, vision)
    assert len(fused) == 2
    assert len(fused[0]) == 5
    # Since attention weights are added (1.0 + weights), output should be slightly > input
    assert fused[0][0] > 0.1
