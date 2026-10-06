from cmre.modules.ingest import AnatomicallySafeAugmenter

def test_anatomically_safe_augmenter():
    augmenter = AnatomicallySafeAugmenter()

    img1 = [[0.1, 0.1, 0.1],
            [0.1, 0.5, 0.1],
            [0.1, 0.1, 0.1]]

    img2 = [[0.9, 0.9, 0.9],
            [0.9, 0.9, 0.9],
            [0.9, 0.9, 0.9]]

    roi_mask = [[0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0]]

    mixed = augmenter.apply_local_mixup(img1, img2, roi_mask)

    # Outside ROI should be identical to img1
    assert mixed[0][0] == 0.1
    # Inside ROI should be a mix (not 0.5 anymore)
    assert mixed[1][1] != 0.5
    assert mixed[1][1] > 0.5 # Since img2 is 0.9

    deformed = augmenter.apply_roi_elastic_deformation(img1, roi_mask)
    assert deformed[0][0] == 0.1
    # Inside ROI gets some mock noise
    assert deformed[1][1] >= 0.0
