"""
CMRE DECISION MATRIX & DETERMINISTIC DISPATCH ENGINE
Servicio de despacho de arquitecturas y pipelines óptimos basados en reglas formales y autopsias forenses.

Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ..schemas import CompetitionInput


class DispatchedPipelineResult(BaseModel):
    matched_rule_id: str
    rule_title: str
    domain: str
    confidence_score: float = 1.0
    prescribed_pipeline: Dict[str, str] = Field(default_factory=dict)
    forbidden_approaches: List[str] = Field(default_factory=list)
    wall_of_shame_alerts: List[str] = Field(default_factory=list)


class DecisionMatrixEngine:
    """
    Motor de razonamiento determinista que mapea restricciones de problema a recetas SOTA de ejecución.
    
    Autor: Perez, Ernesto Rafael ("Rafa")
    """
    
    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path = catalog_path or (
            Path(__file__).resolve().parents[3] / "data" / "knowledge" / "decision_matrix_engine.json"
        )
        self.rules: List[Dict[str, Any]] = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        if self.catalog_path and self.catalog_path.exists():
            try:
                data = json.loads(self.catalog_path.read_text(encoding="utf-8"))
                return data.get("rules", [])
            except Exception:
                pass
        return self._get_fallback_rules()

    @staticmethod
    def _get_fallback_rules() -> List[Dict[str, Any]]:
        return [
            {
                "rule_id": "RULE_MED_MAMMO_EXTREME_IMBALANCE",
                "title": "Radiología & Mamografía Dual CC/MLO con Desbalance Extremo",
                "domain": "medical_imaging",
                "prescribed_pipeline": {
                    "ingest": "SNIP_INGEST_DICOM_FAST (VOI LUT + corrección MONOCHROME1)",
                    "split": "SNIP_SPLIT_GROUP_PATIENT_DISJOINT (StratifiedGroupKFold por paciente)",
                    "signal": "SNIP_MED_CROSS_VIEW_MAMMO_ATTENTION (Fusión atencional CC <-> MLO)",
                    "loss": "SNIP_LOSS_ASYMMETRIC_CUDA + SNIP_LOSS_SOFT_F1_WEIGHTED",
                    "model": "ConvNeXt / EfficientNet-B4 + CrossView Bidirectional Attention",
                    "ensemble": "SNIP_ENS_NNLS_STACKING",
                    "postprocess": "SNIP_ENS_NELDER_MEAD_THRESHOLD"
                },
                "forbidden_approaches": [
                    "Umbral fijo de decisión 0.50 (FAIL_01: colapso de pF1)",
                    "K-Fold aleatorio mezclando proyecciones del mismo paciente (FAIL_05)",
                    "Omitir interpretación de PhotometricInterpretation MONOCHROME1 (FAIL_10)"
                ]
            },
            {
                "rule_id": "RULE_FIN_TIMESERIES_ORDERBOOK",
                "title": "Microestructura Financiera & Libros de Órdenes de Alta Frecuencia",
                "domain": "time_series_finance",
                "prescribed_pipeline": {
                    "ingest": "Ingesta Parquet columnar con downcasting int16/float32",
                    "split": "SNIP_SPLIT_PURGED_EMBARGO_TIME",
                    "signal": "SNIP_HPC_SEGMENT_TREE_LAZY",
                    "loss": "Huber Loss",
                    "model": "LightGBM + CatBoost",
                    "ensemble": "SNIP_ENS_NNLS_STACKING",
                    "postprocess": "Centrado estacional intra-bucket diario"
                },
                "forbidden_approaches": [
                    "K-Fold aleatorio sin purga ni embargo temporal (FAIL_02)",
                    "Meta-regresión libre con coeficientes negativos (FAIL_09)"
                ]
            },
            {
                "rule_id": "RULE_CHEM_MOLECULAR_SCAFFOLD",
                "title": "Química Computacional & Metabolómica Ciega (CASMI)",
                "domain": "cheminformatics_mass_spec",
                "prescribed_pipeline": {
                    "ingest": "Binned high-resolution MS/MS spectra (0.05 Da) + Morgan fingerprint bitsets",
                    "split": "SNIP_SPLIT_SCAFFOLD_MURCKO",
                    "signal": "SNIP_HPC_BITSET_TANIMOTO_FAST",
                    "loss": "Cosine Contrastive Loss",
                    "model": "Spectra-Transformer + Chokudai Beam Search",
                    "ensemble": "SNIP_HPC_CHOKUDAI_SEARCH",
                    "postprocess": "Reranking bayesiano restringido por masa monoisotópica"
                },
                "forbidden_approaches": [
                    "Split aleatorio por ID molecular sin aislar esqueletos Bemis-Murcko (FAIL_04)",
                    "Bucles puros en Python para cálculo de similitudes Tanimoto (FAIL_02)"
                ]
            },
            {
                "rule_id": "RULE_TAB_ORDINAL_DAMAGE",
                "title": "Ingeniería Sísmica & Tabular con Clases Ordinales",
                "domain": "tabular_engineering",
                "prescribed_pipeline": {
                    "ingest": "Tipado riguroso de identificadores geográficos",
                    "split": "StratifiedKFold",
                    "signal": "SNIP_ALT_DRIVENDATA_ORDINAL_DAMAGE_MODELER",
                    "loss": "Multi-Class Log-Loss con pesos ordinales",
                    "model": "SNIP_HPC_SIMULATED_ANNEALING_FEATURE_SELECTION + LightGBM",
                    "ensemble": "SNIP_ENS_NNLS_STACKING",
                    "postprocess": "Optimización Nelder-Mead continua sobre umbrales de partición"
                },
                "forbidden_approaches": [
                    "Target encoding directo sobre IDs de alta cardinalidad sin OOF (FAIL_06)",
                    "Argmax estándar con umbrales simétricos sin calibración (FAIL_01)"
                ]
            },
            {
                "rule_id": "RULE_ENV_SPATIO_TEMPORAL_IOT",
                "title": "Telemetría Ambiental & Redes de Sensores IoT con Fuga Espacio-Temporal",
                "domain": "environmental_telemetry",
                "prescribed_pipeline": {
                    "ingest": "Ingesta cronológica de observaciones por estación sensor",
                    "split": "Spatial Group K-Fold sobre identificadores de dispositivo con purga",
                    "signal": "SNIP_ALT_ZINDI_SPATIO_TEMPORAL_LAG_BLENDER",
                    "loss": "RMSE / Huber Loss",
                    "model": "GBDT temporal + regresión espacial Geo-KNN",
                    "ensemble": "Blending convexo ponderado 85% GBDT + 15% Geo-KNN",
                    "postprocess": "Clipping físico no negativo para concentraciones de partículas"
                },
                "forbidden_approaches": [
                    "K-Fold aleatorio que mezcle lecturas simultáneas de sensores contiguos (FAIL_02)",
                    "Omitir armónicos del ciclo circadiano diurno"
                ]
            }
        ]

    def dispatch(self, comp: CompetitionInput | Dict[str, Any]) -> DispatchedPipelineResult:
        """
        Evalúa las restricciones del torneo y devuelve la receta de despacho óptima.
        """
        data = comp.model_dump() if isinstance(comp, CompetitionInput) else comp
        
        modality = str(data.get("modality", "")).lower()
        title = str(data.get("title", "")).lower()
        metric = str(data.get("metric", "")).lower()
        signals = [s.lower() for s in data.get("leak_signals", [])]
        has_groups = bool(data.get("has_group_structure", False))
        has_temporal = bool(data.get("has_temporal_component", False))
        imbalance = str(data.get("class_imbalance", "")).lower()
        task_type = str(data.get("task_type", "")).lower()

        # 1. CASMI / Metabolómica / Química
        if any("scaffold" in s or "smiles" in s or "msms" in s for s in signals) or "casmi" in title or "molecular" in title:
            return self._build_result("RULE_CHEM_MOLECULAR_SCAFFOLD", 0.95)

        # 2. RSNA Mamografía / Radiología
        if ("mammo" in title or "breast" in title or "dicom" in title) or (modality in ("image", "multimodal") and has_groups and imbalance in ("high", "severe", "extreme")):
            return self._build_result("RULE_MED_MAMMO_EXTREME_IMBALANCE", 0.98)

        # 3. Dermatología / ISIC / Patito Feo
        if "melanoma" in title or "skin" in title or "isic" in title:
            return self._build_result("RULE_MED_DERMATOLOGY_PATIENT_COHORT", 0.96)

        # 4. Finanzas / Microestructura / Optiver
        if has_temporal and ("trading" in title or "volatility" in title or "order" in title or "stock" in title):
            return self._build_result("RULE_FIN_TIMESERIES_ORDERBOOK", 0.95)

        # 5. Zindi AirQo / IoT Ambiental Espacio-Temporal
        if has_temporal and has_groups and ("air" in title or "sensor" in title or "pm2" in title or "weather" in title):
            return self._build_result("RULE_ENV_SPATIO_TEMPORAL_IOT", 0.94)

        # 6. DrivenData Richter's Predictor / Ordinal
        if "damage" in title or "earthquake" in title or "ordinal" in task_type:
            return self._build_result("RULE_TAB_ORDINAL_DAMAGE", 0.92)

        # 7. HuBMAP / Gigapíxel / Histopatología
        if "hubmap" in title or "wsi" in title or "kidney" in title or "histopath" in title:
            return self._build_result("RULE_WSI_HISTOPATHOLOGY_GIGAPIXEL", 0.90)

        # 8. Re-Identificación Facial / Fauna Few-Shot
        if "turtle" in title or "reid" in task_type or "few_shot" in task_type:
            return self._build_result("RULE_BIO_ANIMAL_FEWSHOT_REID", 0.90)

        # Default genérico tabular / multimodal
        if has_temporal:
            return self._build_result("RULE_FIN_TIMESERIES_ORDERBOOK", 0.70)
        return self._build_result("RULE_TAB_ORDINAL_DAMAGE", 0.65)

    def _build_result(self, rule_id: str, confidence: float) -> DispatchedPipelineResult:
        rule = next((r for r in self.rules if r["rule_id"] == rule_id), None)
        if not rule:
            rule = next((r for r in self._get_fallback_rules() if r["rule_id"] == rule_id), self._get_fallback_rules()[0])
            
        return DispatchedPipelineResult(
            matched_rule_id=rule["rule_id"],
            rule_title=rule["title"],
            domain=rule.get("domain", "general_competitive_ml"),
            confidence_score=confidence,
            prescribed_pipeline=rule.get("prescribed_pipeline", {}),
            forbidden_approaches=rule.get("forbidden_approaches", []),
            wall_of_shame_alerts=[f"Bloqueado: {a}" for a in rule.get("forbidden_approaches", [])]
        )
