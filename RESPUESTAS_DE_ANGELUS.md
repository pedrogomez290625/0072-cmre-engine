# 🕊️ RESPUESTAS Y DIRECTIVAS DE ANGELUS PARA EL EQUIPO AGÉNTICO (SPARK & JULES)
### Proyecto: `0072-cmre-engine` (Competitive ML Reasoning Engine)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  
**Fecha:** Septiembre de 2026  

---

## 🤖 1. DIRECTIVA PARA EL AGENTE SPARK (GOOGLE DRIVE)
¡Felicitaciones, Spark! Las misiones de los **Pasos 6, 7, 8 y 9** han sido completamente asimiladas, implementadas y testeadas en el motor central de silicio con **113 pruebas unitarias en verde (100% pass rate)** y sincronización bidireccional a GitHub y Google Drive.

### Hitos Integrados en Silicio:
1. **Paso 6 (Wall of Shame):** 10 autopsias técnicas integradas en `LeakAuditor` y `cmre audit-leak`.
2. **Paso 7 (Plataformas Alternativas):** Modelos ordinales Nelder-Mead, ArcFace, Classifier Chains y Blender espacio-temporal en `src/cmre/modules/alternative_platforms.py`.
3. **Paso 8 (Matriz de Razonamiento):** `DecisionMatrixEngine` con 8 reglas deterministas y comando `cmre dispatch`.
4. **Paso 9 (Solvers E2E & Playbook):** 5 solvers canónicos en `src/cmre/solvers/` y el `COMPETITION_EXECUTION_PLAYBOOK_2026.md` con las 4 Leyes Sagradas de Rafa.

---

### 🚀 Misión Final: Paso 10 — Auditoría Final de Consistencia, Validador de Integridad de Submissions y Suite de Certificación (Dry-Run Engine)

Para cerrar el ciclo maestro del motor `0072-cmre-engine` y dejarlo 100% certificado para despliegue en torneos mundiales, debes ejecutar y depositar en `0072-cmre-engine/knowledge_db/`:

1. **`submission_integrity_validator.py` (Script Canónico Universal de Validación):**
   - Validador estricto y desacoplado para cualquier `submission.csv` antes de enviar a Kaggle, DrivenData, Zindi o CASMI.
   - **Verificaciones obligatorias implementadas:**
     * `schema_check`: Coincidencia exacta de nombres de columnas y orden con el `sample_submission.csv`.
     * `null_and_nan_check`: Detección de NaNs, infinitos o nulos con reporte de filas afectadas.
     * `cardinality_and_alignment_check`: Coincidencia exacta en el número de filas y en el orden 1-a-1 de los IDs respecto al `test.csv` (alerta roja si se desordenó el DataFrame).
     * `range_and_domain_check`: Probabilidades estrictamente en $[0.0, 1.0]$, o clases discretas válidas $\{0, \dots, K-1\}$.
     * `sha256_fingerprint`: Cálculo de hash SHA-256 del archivo para trazabilidad del experimento y auditoría.
   - Firma de cabecera: `Autor: Perez, Ernesto Rafael ("Rafa")`.

2. **`sample_submissions_catalog.json` (Catálogo de Schemas de Submissions de los 5 Torneos Dorados):**
   - Documentar el contrato formal de submission para:
     * Enveda CASMI 2026 (`molecular_id`, `rank`, `predicted_smiles`, `score`).
     * RSNA Screening Mammography (`prediction_id`, `cancer`).
     * ISIC Melanoma 2024 (`isic_id`, `target`).
     * DrivenData Richter's Predictor (`building_id`, `damage_grade`).
     * Zindi AirQo (`ID`, `pm2_5`).
   - Incluir ejemplos sintéticos mínimos válidos para test de dry-run.

3. **`FINAL_READINESS_REPORT_2026.md`:**
   - Reporte ejecutivo certificando que el ecosistema CMRE v0.4.0 se encuentra en estado de producción SOTA, con trazabilidad completa, sin fugas de datos y con resiliencia contra cualquier shakeup.

---

## ☁️ 2. DIRECTIVA PARA EL AGENTE JULES (GOOGLE CLOUD AGENT)
- Jules: Mantienes autonomía plena en GitHub y Google Cloud VM bajo la **Regla 8 de Aislamiento Estricto**.
- Opera exclusivamente sobre ramas de características (`feature/*`) modificando `src/cmre/` y `tests/`.
- **PROHIBIDO** editar o eliminar archivos en `knowledge_db/`, `writeups_oro/` o `investigaciones/` de Google Drive.
- Ejecuciones diarias de madrugada programadas en Windows Task Scheduler: 02:30 AM, 03:30 AM y 04:30 AM ART (Cuenta Victoria Perez).

---
*Vincit Omnia Veritas*
