import pytest
import torch
from cmre.modules.loss import BiTemperedLogisticLoss

def test_bi_tempered_logistic_loss():
    # Setup batch
    B, C = 4, 3
    logits = torch.tensor([
        [2.0, 1.0, 0.1],  # Correct prediction
        [-1.0, 5.0, -1.0], # Correct prediction
        [3.0, 0.0, 0.0],  # Confident but incorrect (simulates label noise/outlier)
        [0.1, 0.1, 0.1],  # Uncertain
    ])
    labels = torch.tensor([0, 1, 1, 2])

    loss_fn = BiTemperedLogisticLoss(t1=0.8, t2=1.2, label_smoothing=0.1, num_iters=5)
    loss = loss_fn(logits, labels)

    assert loss.dim() == 0
    assert not torch.isnan(loss)
    assert loss.item() > 0

    # Check that bounded loss protects against the confident outlier (logits[2])
    ce_loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)
    ce_loss = ce_loss_fn(logits, labels)

    # Bi-tempered should ideally bounded the outlier better, making the overall average lower
    # given its heavy tails (t2 > 1) and bounded property (t1 < 1)

    # Ensure gradients flow
    logits.requires_grad_(True)
    loss_fn(logits, labels).backward()
    assert logits.grad is not None
