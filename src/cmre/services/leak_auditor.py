"""
CMRE ANTI-SHAKEUP & LEAKAGE FORENSIC AUDITOR
Servicio de auditoría determinista para detección preventiva de fugas de datos y colapso de leaderboard.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
from typing import List, Dict, Any, Set, Optional, Tuple
from pydantic import BaseModel, Field


class LeakAuditResult(BaseModel):
    has_leak: bool = False
    risk_score: float = 0.0  # 0.0 (Cero riesgo) a 1.0 (Fuga catastrófica)
    detected_leaks: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    prescribed_defenses: List[str] = Field(default_factory=list)
    fold_statistics: Dict[str, Any] = Field(default_factory=dict)


class LeakAuditor:
    """
    Auditor forense de estrategias de validación cruzada y partición de datos.
    Previene el gap CV-LB y el shakeup de leaderboard antes de entrenar modelos costosos.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """

    @staticmethod
    def audit_group_leakage(
        train_groups: List[Any],
        val_groups: List[Any]
    ) -> Tuple[bool, int, Set[Any]]:
        """
        Verifica si hay grupos (pacientes, usuarios, dispositivos) compartidos entre train y val.
        """
        set_train = set(train_groups)
        set_val = set(val_groups)
        intersection = set_train.intersection(set_val)
        has_leak = len(intersection) > 0
        return has_leak, len(intersection), intersection

    @staticmethod
    def audit_temporal_lookahead(
        train_times: List[float | int],
        val_times: List[float | int],
        embargo_gap: float | int = 0
    ) -> Tuple[bool, int]:
        """
        Verifica lookahead bias: si algún timestamp de entrenamiento ocurre después
        del inicio de validación (menos el embargo).
        """
        if not train_times or not val_times:
            return False, 0
        min_val = min(val_times)
        leaked_samples = [t for t in train_times if t >= (min_val - embargo_gap)]
        has_leak = len(leaked_samples) > 0
        return has_leak, len(leaked_samples)

    @staticmethod
    def audit_class_imbalance(
        targets: List[int | float]
    ) -> Tuple[bool, float, str]:
        """
        Evalúa el riesgo de saturación de gradientes por desbalance severo.
        """
        if not targets:
            return False, 0.0, "normal"
        positives = sum(1 for t in targets if t > 0.5)
        pos_rate = positives / len(targets)
        
        if pos_rate < 0.01:
            return True, pos_rate, "extreme (<1%)"
        elif pos_rate < 0.05:
            return True, pos_rate, "severe (<5%)"
        return False, pos_rate, "balanced"

    @classmethod
    def audit_split(
        cls,
        train_indices: List[int],
        val_indices: List[int],
        groups: Optional[List[Any]] = None,
        timestamps: Optional[List[float | int]] = None,
        targets: Optional[List[int | float]] = None,
        embargo: float | int = 0
    ) -> LeakAuditResult:
        """
        Audita una partición de entrenamiento y validación de extremo a extremo.
        """
        result = LeakAuditResult()
        leaks = []
        warnings = []
        defenses = []
        risk_acc = 0.0

        # 1. Auditoría de Grupos (Pacientes)
        if groups is not None:
            train_g = [groups[i] for i in train_indices]
            val_g = [groups[i] for i in val_indices]
            has_grp_leak, count_leaked, leaked_items = cls.audit_group_leakage(train_g, val_g)
            if has_grp_leak:
                leaks.append(f"GROUP_LEAKAGE: {count_leaked} grupos/pacientes compartidos entre Train y Val")
                defenses.append("SNIP_SPLIT_GROUP_PATIENT_DISJOINT (StratifiedGroupKFold)")
                risk_acc += 0.5
                result.fold_statistics["leaked_groups_count"] = count_leaked

        # 2. Auditoría Temporal
        if timestamps is not None:
            train_t = [timestamps[i] for i in train_indices]
            val_t = [timestamps[i] for i in val_indices]
            has_time_leak, count_t_leak = cls.audit_temporal_lookahead(train_t, val_t, embargo_gap=embargo)
            if has_time_leak:
                leaks.append(f"TEMPORAL_LOOKAHEAD: {count_t_leak} observaciones de Train solapan con la ventana futura de Val")
                defenses.append("SNIP_SPLIT_PURGED_EMBARGO_TIME (PurgedGroupTimeSeriesSplit)")
                risk_acc += 0.5
                result.fold_statistics["lookahead_samples_count"] = count_t_leak

        # 3. Auditoría de Desbalance
        if targets is not None:
            val_targets = [targets[i] for i in val_indices]
            is_imbalanced, pos_rate, level = cls.audit_class_imbalance(val_targets)
            if is_imbalanced:
                warnings.append(f"CLASS_IMBALANCE_{level.upper()}: Tasa de positivos del {pos_rate*100:.2f}%")
                defenses.append("SNIP_LOSS_ASYMMETRIC_CUDA (AsymmetricLoss)")
                defenses.append("SNIP_LOSS_SOFT_F1_WEIGHTED (SoftF1Loss)")
                risk_acc += 0.2
                result.fold_statistics["positive_rate"] = pos_rate

        result.has_leak = len(leaks) > 0
        result.risk_score = min(risk_acc, 1.0)
        result.detected_leaks = leaks
        result.warnings = warnings
        result.prescribed_defenses = list(dict.fromkeys(defenses))  # deduplicar
        return result
