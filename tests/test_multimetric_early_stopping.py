import pytest
from cmre.modules.loss import MultiMetricEarlyStopping

def test_multi_metric_early_stopping_all_mode():
    early_stop = MultiMetricEarlyStopping(patience=2, mode="all")
    early_stop.register_metric("val_loss", mode="min")
    early_stop.register_metric("val_f1", mode="max")

    # Epoch 1: Both improve
    assert early_stop(1, {"val_loss": 0.5, "val_f1": 0.6}) == False

    # Epoch 2: F1 improves, Loss degrades
    assert early_stop(2, {"val_loss": 0.55, "val_f1": 0.65}) == False

    # Epoch 3: Loss degrades, F1 degrades (wait goes to 2 for loss, 1 for f1)
    assert early_stop(3, {"val_loss": 0.6, "val_f1": 0.64}) == False

    # Epoch 4: Loss degrades, F1 degrades (wait goes to 3 for loss, 2 for f1)
    # Since mode="all", it stops when ALL metrics reach patience. Both are >= 2 now.
    assert early_stop(4, {"val_loss": 0.65, "val_f1": 0.63}) == True


def test_multi_metric_early_stopping_any_mode():
    early_stop = MultiMetricEarlyStopping(patience=2, mode="any")
    early_stop.register_metric("val_loss", mode="min")
    early_stop.register_metric("val_f1", mode="max")

    # Epoch 1: Both improve
    assert early_stop(1, {"val_loss": 0.5, "val_f1": 0.6}) == False

    # Epoch 2: Loss degrades, F1 improves (wait: loss=1, f1=0)
    assert early_stop(2, {"val_loss": 0.55, "val_f1": 0.65}) == False

    # Epoch 3: Loss degrades again, F1 improves (wait: loss=2, f1=0)
    # Since mode="any", it stops if ANY metric reaches patience. Loss reached 2.
    assert early_stop(3, {"val_loss": 0.6, "val_f1": 0.70}) == True
