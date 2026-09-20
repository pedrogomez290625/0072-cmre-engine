# 📊 ÍNDICE MAESTRO DE INVESTIGACIONES COMPETITIVAS
### Ecosistema: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Frecuencia de Actualización:** Ciclo Programado cada 15 Días (Días 1 y 15 de cada mes).

---

## 🧭 ESTADO GENERAL DE LA BASE DE CONOCIMIENTO

| Métrica | Valor Actual |
| :--- | :--- |
| **Total de Competencias Indexadas** | 0 (Inicializando ciclo) |
| **Kaggle Playground / Community (Vía Rápida)** | 0 |
| **Kaggle Featured / Research (Grandes Premios)** | 0 |
| **Plataformas Alternativas (DrivenData, Zindi, etc.)** | 0 |
| **Última Ejecución de Tarea Programada** | 19 de Septiembre de 2026 |

---

## 🗂️ REGISTRO HISTÓRICO DE INVESTIGACIONES

> Este índice es leído automáticamente por el script `scripts/cron_research_auditor.py` y por el agente de Deep Research en cada ciclo de 15 días para evitar duplicar análisis ya realizados.

| ID | Plataforma | Categoría | Competencia | Año | Métrica Oficial | Estado CMRE | Archivo de Investigación |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| *#001* | Kaggle | Research | Enveda CASMI 2026 (Mass Spectra) | 2026 | Cosine / Top-k | 🟡 En Preparación | `investigaciones/kaggle/research/enveda_casmi_2026.md` |
| *#002* | Kaggle | Research | Stanford Ribonanza RNA Folding | 2023 | MAE | ⚪ Pendiente | `investigaciones/kaggle/research/stanford_ribonanza_rna.md` |
| *#003* | Kaggle | Featured | RSNA Screening Mammography | 2023 | pAUC | ⚪ Pendiente | `investigaciones/kaggle/featured/rsna_breast_cancer.md` |
| *#004* | Kaggle | Featured | IEEE-CIS Fraud Detection | 2019 | ROC-AUC | ⚪ Pendiente | `investigaciones/kaggle/featured/ieee_cis_fraud.md` |
| *#005* | Kaggle | Playground | Tabular Playground Series (TPS) | 2024-26 | ROC-AUC / LogLoss | ⚪ Pendiente | `investigaciones/kaggle/playground/tps_master_patterns.md` |
| *#006* | DrivenData | Social Impact | Flu Shot Learning / Climate Challenges | 2024 | LogLoss / Multi-output | ⚪ Pendiente | `investigaciones/alternativas/drivendata/drivendata_master.md` |
| *#007* | Zindi | Africa ML | Crop Disease / African Healthcare | 2025 | F1-Score | ⚪ Pendiente | `investigaciones/alternativas/zindi/zindi_top_solutions.md` |
| *#008* | AIcrowd | Advanced AI | NeurIPS ML Challenges / Robotics | 2025 | Custom Benchmark | ⚪ Pendiente | `investigaciones/alternativas/aicrowd/aicrowd_benchmarks.md` |

---

## 🔄 CÓMO ACTUALIZAR ESTE ÍNDICE
1. Cuando se complete una investigación con el prompt de Deep Research, guardar el archivo Markdown en la subcarpeta correspondiente.
2. Ejecutar:
   ```bash
   uv run python scripts/cron_research_auditor.py --sync
   ```
3. El script auditará los nuevos archivos, actualizará la tabla anterior e insertará los claims a la base de datos de CMRE.
