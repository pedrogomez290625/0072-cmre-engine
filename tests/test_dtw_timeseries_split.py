import pytest
import numpy as np
from cmre.modules.split import DTWPurgedTimeSeriesSplit

def test_dtw_purged_time_series_split():
    # Create a non-stationary time series
    timestamps = list(range(100))
    # Variance changes over time
    series_values = [np.sin(t / 10.0) + (np.random.randn() * (0.1 if t < 50 else 1.0)) for t in timestamps]

    splitter = DTWPurgedTimeSeriesSplit(n_splits=3, embargo_pct=0.05, max_warping_window=0.1)
    folds = splitter.split(timestamps, series_values)

    assert len(folds) == 3
    for train_idx, val_idx in folds:
        assert len(train_idx) > 0
        assert len(val_idx) > 0
        # Check embargo
        assert min(val_idx) - max(train_idx) >= int(100 * 0.05)
        # Check no overlap
        assert set(train_idx).isdisjoint(set(val_idx))
