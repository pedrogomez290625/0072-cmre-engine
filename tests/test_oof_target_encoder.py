import pytest
from cmre.modules.signal import OOFTargetEncoder

def test_oof_target_encoder():
    categories = ['A', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'C', 'A']
    targets =    [1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]

    cv_splits = [
        ([2,3,4,5,6,7,8,9], [0,1]),
        ([0,1,4,5,6,7,8,9], [2,3]),
        ([0,1,2,3,6,7,8,9], [4,5]),
        ([0,1,2,3,4,5,8,9], [6,7]),
        ([0,1,2,3,4,5,6,7], [8,9])
    ]

    encoder = OOFTargetEncoder(m_smoothing=5.0, noise_level=0.0)

    oof_encoded = encoder.fit_transform(categories, targets, cv_splits)

    assert len(oof_encoded) == len(categories)

    # Validation fold [0, 1] (both 'A').
    # Training targets: [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    # Sum train targets: 3.0, Len train targets: 8. Global mean of train: 3.0/8 = 0.375
    # Train A targets: idx 6 (1.0), idx 9 (0.0).  Sum=1.0, Count=2. Mean=0.5
    # TE = (2 * 0.5 + 5 * 0.375) / (2 + 5) = (1.0 + 1.875) / 7 = 2.875 / 7 = 0.4107142857142857

    assert abs(oof_encoded[0] - 0.4107142857) < 1e-4
    assert abs(oof_encoded[1] - 0.4107142857) < 1e-4

    # With noise
    encoder_noise = OOFTargetEncoder(m_smoothing=5.0, noise_level=0.1)
    oof_encoded_noise = encoder_noise.fit_transform(categories, targets, cv_splits)

    assert len(oof_encoded_noise) == len(categories)
    assert oof_encoded_noise[0] != oof_encoded[0] # Very likely different due to noise
