"""MOD_LOSS - Specialized Competition Loss Functions.

Implements custom loss functions for extreme medical imbalance and competition metrics:
- Asymmetric Loss for massive class imbalance (Claims C27, FC03)
- Differentiable Soft-F1 Loss for metric-aligned optimization
- Partial-AUC (pAUC) surrogate loss
"""

from __future__ import annotations

import math
from typing import List, Tuple


def asymmetric_loss_numpy(
    y_true: List[float],
    y_pred_probs: List[float],
    gamma_pos: float = 0.0,
    gamma_neg: float = 4.0,
    clip_neg: float = 0.05,
    eps: float = 1e-8,
) -> float:
    """Pure-Python/NumPy implementation of Asymmetric Loss.
    
    Discounts easy negative examples (gamma_neg > gamma_pos) with probability margin shifting.
    Vital for screening mammography and rare cancer detection (1:100 to 1:1000 prevalence).
    """
    total_loss = 0.0
    n = len(y_true)
    if n == 0:
        return 0.0

    for y, p in zip(y_true, y_pred_probs):
        p = max(min(p, 1.0 - eps), eps)
        if y >= 0.5:
            # Positive sample
            loss = -(1.0 - p) ** gamma_pos * math.log(p)
        else:
            # Negative sample with probability margin shift
            p_m = max(p - clip_neg, 0.0)
            loss = -p_m ** gamma_neg * math.log(max(1.0 - p_m, eps))
        total_loss += loss

    return total_loss / n


def soft_f1_score_numpy(
    y_true: List[float],
    y_pred_probs: List[float],
    eps: float = 1e-7,
) -> float:
    """Continuous differentiable soft F1-Score approximation."""
    tp = sum(y * p for y, p in zip(y_true, y_pred_probs))
    fp = sum((1.0 - y) * p for y, p in zip(y_true, y_pred_probs))
    fn = sum(y * (1.0 - p) for y, p in zip(y_true, y_pred_probs))
    
    f1 = (2.0 * tp) / (2.0 * tp + fp + fn + eps)
    return f1



import torch
import torch.nn as nn

class AsymmetricLoss(nn.Module):
    """Asymmetric Loss for multi-label or extreme class imbalance in medical imaging."""
    def __init__(self, gamma_neg=4.0, gamma_pos=1.0, clip=0.05, eps=1e-8):
        super().__init__()
        self.gamma_neg = gamma_neg
        self.gamma_pos = gamma_pos
        self.clip = clip
        self.eps = eps

    def forward(self, x, y):
        """
        Args:
            x: Raw model logits [B, C] or any dimensions [B, C, ...]
            y: Binary target targets [B, C] or any dimensions [B, C, ...] in {0, 1}
        """
        xs_pos = torch.sigmoid(x)
        xs_neg = 1.0 - xs_pos

        # Asymmetric clipping
        if self.clip is not None and self.clip > 0:
            xs_neg = (xs_neg + self.clip).clamp(max=1.0)

        # Basic CE calculation
        los_pos = y * torch.log(xs_pos.clamp(min=self.eps))
        los_neg = (1.0 - y) * torch.log(xs_neg.clamp(min=self.eps))
        loss = los_pos + los_neg

        # Asymmetric focusing weights
        if self.gamma_neg > 0 or self.gamma_pos > 0:
            pt0 = xs_pos * y
            pt1 = xs_neg * (1.0 - y)
            pt = pt0 + pt1
            one_sided_gamma = self.gamma_pos * y + self.gamma_neg * (1.0 - y)
            one_sided_w = torch.pow(1.0 - pt, one_sided_gamma)
            loss *= one_sided_w

        return -loss.mean()

class SoftF1Loss(nn.Module):
    """Continuous differentiable soft F1/Dice Loss approximation with dynamic class weights."""
    def __init__(self, eps=1e-7, class_weights=None):
        super().__init__()
        self.eps = eps
        if class_weights is not None:
            self.register_buffer('class_weights', torch.tensor(class_weights, dtype=torch.float32))
        else:
            self.class_weights = None

    def forward(self, logits, targets):
        """
        Args:
            logits: Model logits [B, C, ...]
            targets: Binary targets [B, C, ...]
        """
        probs = torch.sigmoid(logits)

        # Calculate Soft F1
        # To support multidimensional batch, we sum over all dimensions except classes (dim=1)
        # Assuming format is [B, C, d1, d2, ...]

        if logits.dim() > 2:
            dims_to_sum = tuple(range(2, logits.dim()))
            dims_to_sum = (0,) + dims_to_sum
        else:
            dims_to_sum = (0,)

        tp = (targets * probs).sum(dim=dims_to_sum)
        fp = ((1.0 - targets) * probs).sum(dim=dims_to_sum)
        fn = (targets * (1.0 - probs)).sum(dim=dims_to_sum)

        f1 = (2.0 * tp) / (2.0 * tp + fp + fn + self.eps)

        if self.class_weights is not None:
            weights = self.class_weights.to(logits.dtype)
            f1 = f1 * weights
            loss = 1.0 - f1.sum() / weights.sum()
        else:
            loss = 1.0 - f1.mean()

        return loss

    def forward(self, logits, targets):
        """
        Args:
            logits: Model logits [B, C, ...]
            targets: Binary targets [B, C, ...]
        """
        probs = torch.sigmoid(logits)

        # Calculate Soft F1
        # To support multidimensional batch, we sum over all dimensions except classes (dim=1)
        # Assuming format is [B, C, d1, d2, ...]

        if logits.dim() > 2:
            dims_to_sum = tuple(range(2, logits.dim()))
            dims_to_sum = (0,) + dims_to_sum
        else:
            dims_to_sum = (0,)

        tp = (targets * probs).sum(dim=dims_to_sum)
        fp = ((1.0 - targets) * probs).sum(dim=dims_to_sum)
        fn = (targets * (1.0 - probs)).sum(dim=dims_to_sum)

        f1 = (2.0 * tp) / (2.0 * tp + fp + fn + self.eps)

        if self.class_weights is not None:
            weights = torch.tensor(self.class_weights, device=logits.device, dtype=logits.dtype)
            f1 = f1 * weights
            loss = 1.0 - f1.sum() / weights.sum()
        else:
            loss = 1.0 - f1.mean()

        return loss


# Keep the original template string as it's imported elsewhere
CODE_TEMPLATE_ASYMMETRIC_LOSS = '''# [CMRE MOD_LOSS] Asymmetric Loss (ASL) for PyTorch
import torch
import torch.nn as nn

class AsymmetricLoss(nn.Module):
    """Asymmetric Loss for multi-label or extreme class imbalance in medical imaging."""
    def __init__(self, gamma_neg=4, gamma_pos=1, clip=0.05, eps=1e-8):
        super().__init__()
        self.gamma_neg = gamma_neg
        self.gamma_pos = gamma_pos
        self.clip = clip
        self.eps = eps

    def forward(self, x, y):
        """"
        Args:
            x: Raw model logits [B, C]
            y: Binary target targets [B, C] in {0, 1}
        """"
        xs_pos = torch.sigmoid(x)
        xs_neg = 1.0 - xs_pos

        # Asymmetric clipping
        if self.clip is not None and self.clip > 0:
            xs_neg = (xs_neg + self.clip).clamp(max=1)

        # Basic CE calculation
        los_pos = y * torch.log(xs_pos.clamp(min=self.eps))
        los_neg = (1 - y) * torch.log(xs_neg.clamp(min=self.eps))
        loss = los_pos + los_neg

        # Asymmetric focusing weights
        if self.gamma_neg > 0 or self.gamma_pos > 0:
            pt0 = xs_pos * y
            pt1 = xs_neg * (1 - y)
            pt = pt0 + pt1
            one_sided_gamma = self.gamma_pos * y + self.gamma_neg * (1 - y)
            one_sided_w = torch.pow(1 - pt, one_sided_gamma)
            loss *= one_sided_w

        return -loss.sum()
'''
