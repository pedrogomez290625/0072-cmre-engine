"""MOD_LOSS - Specialized Competition Loss Functions.

Implements custom loss functions for extreme medical imbalance and competition metrics:
- Asymmetric Loss for massive class imbalance (Claims C27, FC03)
- Differentiable Soft-F1 Loss for metric-aligned optimization
- Partial-AUC (pAUC) surrogate loss
"""

from __future__ import annotations

import math
from typing import Any, List, Tuple


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

class MultiMetricEarlyStopping:
    """Multi-Metric Early Stopping Meta-Controller (Claim CMRE-28).

    Monitors multiple metrics simultaneously (e.g. loss and pAUC/F1) and only stops
    training when there is a consensus of no improvement across the metrics.
    Prevents premature stopping when loss plateaus but secondary metrics like precision/recall
    are still improving (resolves RSNA Mammography FAIL_10).
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.0, mode: str = "all"):
        """
        Args:
            patience: Number of epochs with no improvement after which training will be stopped.
            min_delta: Minimum change in the monitored quantity to qualify as an improvement.
            mode: "all" (stop if ALL metrics fail to improve) or "any" (stop if ANY metric fails).
                  Default is "all" to be conservative against premature stopping.
        """
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode

        # metric_name -> {"best": float, "mode": "min"|"max", "wait": int}
        self.metrics_state: dict[str, dict[str, Any]] = {}
        self.stopped_epoch = 0
        self.stop_training = False

    def register_metric(self, name: str, mode: str = "min") -> None:
        """Registers a metric to track. Mode must be 'min' or 'max'."""
        best_val = float("inf") if mode == "min" else float("-inf")
        self.metrics_state[name] = {"best": best_val, "mode": mode, "wait": 0}

    def __call__(self, epoch: int, metrics: dict[str, float]) -> bool:
        """
        Checks if training should stop.
        Returns True if early stopping condition is met.
        """
        if self.stop_training:
            return True

        improvements = []

        for name, current_val in metrics.items():
            if name not in self.metrics_state:
                continue

            state = self.metrics_state[name]
            mode = state["mode"]
            best = state["best"]

            improved = False
            if mode == "min":
                if current_val < best - self.min_delta:
                    improved = True
            else: # max
                if current_val > best + self.min_delta:
                    improved = True

            if improved:
                state["best"] = current_val
                state["wait"] = 0
                improvements.append(True)
            else:
                state["wait"] += 1
                improvements.append(False)

        # Decide based on mode
        if not improvements:
            return False # Nothing to track

        if self.mode == "all":
            # We stop if ALL tracked metrics have waited >= patience
            should_stop = all(self.metrics_state[m]["wait"] >= self.patience for m in self.metrics_state)
        elif self.mode == "any":
             # We stop if ANY tracked metric has waited >= patience
             should_stop = any(self.metrics_state[m]["wait"] >= self.patience for m in self.metrics_state)
        else:
            should_stop = False

        if should_stop:
            self.stopped_epoch = epoch
            self.stop_training = True

        return self.stop_training

class BiTemperedLogisticLoss(nn.Module):
    """Bi-Tempered Logistic Loss for label noise robustness (Claim CMRE-38).

    Uses t1 and t2 parameters to create a heavy-tailed distribution that bounds
    the loss and is robust to mislabeled examples (e.g. 15-20% clinical noise).
    Based on Google Research "Robust Bi-Tempered Logistic Loss Based on Tsallis Divergence".
    """

    def __init__(self, t1: float = 0.8, t2: float = 1.2, label_smoothing: float = 0.0, num_iters: int = 5):
        super().__init__()
        self.t1 = t1
        self.t2 = t2
        self.label_smoothing = label_smoothing
        self.num_iters = num_iters

    def log_t(self, u, t):
        if t == 1.0:
            return torch.log(u)
        else:
            return (u.pow(1.0 - t) - 1.0) / (1.0 - t)

    def exp_t(self, u, t):
        if t == 1.0:
            return torch.exp(u)
        else:
            return torch.relu(1.0 + (1.0 - t) * u).pow(1.0 / (1.0 - t))

    def compute_normalization_fixed_point(self, activations, t, num_iters):
        mu = torch.max(activations, dim=-1, keepdim=True).values
        normalized_activations_step_0 = activations - mu

        normalized_activations = normalized_activations_step_0
        i = 0
        while i < num_iters:
            i += 1
            logt_partition = torch.sum(
                self.exp_t(normalized_activations, t), dim=-1, keepdim=True
            )
            normalized_activations = normalized_activations_step_0 * \
                                     (logt_partition.pow(1.0 - t))

        logt_partition = torch.sum(
            self.exp_t(normalized_activations, t), dim=-1, keepdim=True
        )
        normalization_constants = - self.log_t(1.0 / logt_partition, t) + mu

        return normalization_constants

    def compute_probabilities(self, activations, t, num_iters):
        normalization_constants = self.compute_normalization_fixed_point(activations, t, num_iters)
        return self.exp_t(activations - normalization_constants, t)

    def forward(self, activations, labels):
        """
        Args:
            activations: Raw logits (B, C)
            labels: Integer target labels (B,) or one-hot (B, C)
        """
        if labels.dim() == 1 or (labels.dim() == 2 and labels.shape[1] == 1):
            labels_one_hot = torch.nn.functional.one_hot(labels.long().view(-1), num_classes=activations.shape[-1]).float()
        else:
            labels_one_hot = labels.float()

        if self.label_smoothing > 0:
            num_classes = labels_one_hot.shape[-1]
            labels_one_hot = labels_one_hot * (1 - self.label_smoothing) + self.label_smoothing / num_classes

        probabilities = self.compute_probabilities(activations, self.t2, self.num_iters)

        # Loss formula for bi-tempered logistic loss
        loss_values = labels_one_hot * self.log_t(labels_one_hot + 1e-10, self.t1) \
                      - labels_one_hot * self.log_t(probabilities, self.t1) \
                      - labels_one_hot.pow(2.0 - self.t1) / (2.0 - self.t1) \
                      + probabilities.pow(2.0 - self.t1) / (2.0 - self.t1)

        loss_values = loss_values.sum(dim=-1)

        return loss_values.mean()


class MDLComplexityOptimizer:
    """Optimizador de Complejidad MDL (Minimum Description Length) (Claim CMRE-48).

    En el razonamiento AGI (ARC Prize), penaliza programas inducidos (DSL) que están
    sobre-ajustados (espagueti simbólico). Evalúa candidatos con:
    cost = len(DSL_ast_nodes) * alpha + Error_Rate * beta
    """

    def __init__(self, alpha: float = 1.0, beta: float = 100.0):
        """
        Args:
            alpha: Peso para la complejidad del programa (longitud de nodos).
            beta: Peso para el error de validación empírico (Error_Rate).
        """
        self.alpha = alpha
        self.beta = beta

    def compute_cost(self, num_ast_nodes: int, error_rate: float) -> float:
        """Calcula el costo MDL explícito."""
        return (num_ast_nodes * self.alpha) + (error_rate * self.beta)

    def select_best_program(self, programs_metadata: List[Dict[str, float]]) -> int:
        """
        Selecciona el índice del programa candidato con el menor costo MDL.

        Args:
            programs_metadata: Lista de diccionarios, cada uno con 'nodes' y 'error_rate'.
        """
        if not programs_metadata:
            return -1

        best_idx = 0
        best_cost = float('inf')

        for i, meta in enumerate(programs_metadata):
            cost = self.compute_cost(int(meta.get('nodes', 0)), float(meta.get('error_rate', 1.0)))
            if cost < best_cost:
                best_cost = cost
                best_idx = i

        return best_idx
