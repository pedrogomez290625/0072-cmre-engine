import pytest
import numpy as np
from cmre.modules.ingest import StrictDicomLUTDecoder

def test_strict_dicom_lut_decoder():
    decoder = StrictDicomLUTDecoder()

    # Simulate a raw DICOM array
    # Dense tissue (bright in MONOCHROME2) should have lower values in MONOCHROME1
    pixel_array = np.array([0, 1000, 2000, 3000, 4000], dtype=np.float32)

    # 1. Test MONOCHROME1 Inversion
    metadata_m1 = {
        "PhotometricInterpretation": "MONOCHROME1"
    }

    decoded_m1 = decoder.decode(pixel_array.copy(), metadata_m1)
    # The max value is 4000. Inversion: 4000 - [0, 1000, 2000, 3000, 4000]
    expected_m1 = np.array([4000, 3000, 2000, 1000, 0], dtype=np.float32)
    np.testing.assert_array_almost_equal(decoded_m1, expected_m1)

    # 2. Test MONOCHROME2 (no inversion)
    metadata_m2 = {
        "PhotometricInterpretation": "MONOCHROME2"
    }

    decoded_m2 = decoder.decode(pixel_array.copy(), metadata_m2)
    np.testing.assert_array_almost_equal(decoded_m2, pixel_array)

    # 3. Test Rescale and Windowing
    metadata_full = {
        "PhotometricInterpretation": "MONOCHROME1",
        "RescaleSlope": 2.0,
        "RescaleIntercept": -100.0,
        "WindowCenter": 2000,
        "WindowWidth": 4000
    }

    decoded_full = decoder.decode(pixel_array.copy(), metadata_full)
    assert decoded_full.shape == pixel_array.shape

    # Without numpy (testing list fallback)
    pixel_list = [0, 1000, 2000, 3000, 4000]
    decoded_list = decoder.decode(pixel_list, metadata_m1)
    assert decoded_list == [4000, 3000, 2000, 1000, 0]
