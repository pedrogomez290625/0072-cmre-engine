# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Sesión de Desarrollo Agnóstico (5 de Octubre 2026) - Auto-Reescritura
**Autor:** Perez, Ernesto Rafael ("Rafa") & Victoria Perez

Este archivo es reescrito por el motor tras el análisis de `ACTIVE_COMPETITIONS.json` y el `data/knowledge/postmortems_failures_catalog.json`. Su objetivo es proyectar las mitigaciones a las vulnerabilidades encontradas y potenciar los solvers de las competencias activas (RSNA Knee, CASMI, ARC-AGI).

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-46: Integrador de Metadata Tabular + Visión 2.5D
- **Origen:** `ACTIVE_COMPETITIONS.json` (RSNA Knee 2026 - modality: tabular_metadata + image_2.5d_mri).
- **Problema:** El solver actual `RSNAKneeSolver` y `ClassWiseAsymmetricBlender` asumen entradas homogéneas de los canales MRI, ignorando variables clínicas críticas como edad, BMI y marcadores previos de lesión, los cuales son clave para predecir patologías complejas como roturas meniscales (target multilabel de 12 clases).
- **Implementación:** Diseñar un fusionador bimodal en `MOD_ENSEMBLE` que proyecte embeddings de metadatos tabulares mediante redes densas residuales y los concatene o aplique Cross-Attention sobre los embeddings finales del encoder de visión antes de la capa de clasificación.

### [ ] SUPER-TAREA CMRE-47: Detector de Decoys Basado en Grafos Moleculares (GNN Validator)
- **Origen:** `ACTIVE_COMPETITIONS.json` (Enveda CASMI 2026 - modality: molecular_smiles_graph) & `FAIL_14` (Decoy Overload).
- **Problema:** El filtro SIRIUS de ausencia es necesario pero insuficiente. Se requiere evaluar estructuralmente si el "SMILES_graph" propuesto como decoy es energéticamente estable o biofísicamente probable dentro del dominio de metabolómica humana/vegetal.
- **Implementación:** Construir en `MOD_OOD` un estimador heurístico o integrador para GNN ligeras (ej. pre-entrenadas con GraphSAGE) que asigne un "Plausibility Score" al grafo SMILES candidato. Penalizar candidatos Top-K cuyo score estructural caiga en percentiles inferiores de distribución de entrenamiento OOD.

### [ ] SUPER-TAREA CMRE-48: Optimizador de Complejidad MDL (Minimum Description Length)
- **Origen:** `ACTIVE_COMPETITIONS.json` (ARC Prize 2026 - key_challenge: mdl_program_complexity).
- **Problema:** En el razonamiento AGI, la síntesis de programas DSL a menudo genera pipelines sobre-ajustados con demasiadas operaciones ("espagueti simbólico") que resuelven los pares de demostración (few-shot) pero fallan catastróficamente en generalizar el grid de test oculto (Zero-Shot Generalization).
- **Implementación:** Incorporar en `MOD_LOSS` o como un meta-controlador en el `ARCAGIHybridSolver` una penalización explícita MDL. Durante la fase de validación de programas inducidos, priorizar candidatos basándose en `cost = len(DSL_ast_nodes) * alpha + Error_Rate * beta`.

### [ ] SUPER-TAREA CMRE-49: Arquitectura de Poda Dinámica por Límite de Tiempo (Dynamic Pruning)
- **Origen:** `ACTIVE_COMPETITIONS.json` (Kaggle timeout risk, Latency Budgets) y extensión a `CMRE-42`.
- **Problema:** El límite estricto de latencia de inferencia por muestra ($1.5s$ para RSNA, $5.0s$ para CASMI, $30.0s$ para ARC) requiere una adaptación más sofisticada que la poda estática predefinida. Dependiendo de la complejidad de la muestra entrante (ej. imagen muy ruidosa), se debe gastar más o menos cómputo.
- **Implementación:** Extender `LatencyBudgetPruner` en `MOD_ENSEMBLE` a un ruteador dinámico: si un predictor "rápido y barato" estima baja confianza o alta ambigüedad para una muestra, enruta el cálculo a la rama pesada del ensamble consumiendo el presupuesto; de lo contrario, aplica *early exit*.

### [ ] SUPER-TAREA CMRE-50: Generador de Data Augmentation Específica de Dominio Médico
- **Origen:** Análisis retrospectivo del Desbalance Severo (RSNA Knee 2026).
- **Problema:** Las lesiones de clase minoritaria (ej. desgarros de ligamento cruzado grado 3) son extremadamente raras y requieren aumentación que no deforme la anatomía radiológica. MixUp estandar introduce artefactos no realistas.
- **Implementación:** Introducir en `MOD_INGEST` un "Anatomically Safe Augmenter": aplicar transformaciones elásticas suaves confinadas al ROI del tejido (ya extraído previamente por el pipeline DICOM) y mezclas locales (Local MixUp/CutMix) sobre áreas patológicas de interés.

---
[VINCIT_OMNIA_VERITAS]
Autor: Perez, Ernesto Rafael ("Rafa") & Victoria Perez
