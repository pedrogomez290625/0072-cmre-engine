# 📋 ESPECIFICACIÓN FUNCIONAL SOBERANA (SPEC LATEST)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Versión:** 0.3.0
**Misión:** Transformar la experiencia acumulada de competencias de Data Science en decisiones de ingeniería de alta precisión y planes de experimentación guiados por evidencia.

---

## 🎯 1. REQUERIMIENTOS FUNCIONALES CLAVE

### RF-01: Perfilado de Competencia (*Problem DNA*)
- Recibir una entrada estructurada en JSON (`CompetitionInput`) conteniendo:
  - Métrica oficial (ej. Multi-Class Log Loss, Dice, ROC-AUC, Cosine Similarity).
  - Modalidades presentes (tabular, texto, imágenes, series temporales, espectrometría/grafos).
  - Riesgos de fuga de datos (*leakage risk*) y variabilidad de distribución (*distribution drift*).
  - Estructura de grupos de validación (`group_keys`, dependencia temporal).
  - Restricciones operativas (tiempo máximo de inferencia, sin acceso a internet en kernel de sumisión).
- Generar un objeto inmutable `ProblemDNA` que guíe la búsqueda y el ranqueo de técnicas.

### RF-02: Recuperación Híbrida y Scoring con Decaimiento por Recencia
- Combinar similitud de embeddings semánticos con filtros duros de modalidad y compatibilidad de restricciones.
- Aplicar función de decaimiento por recencia:
  $$\text{peso} = 0.5^{(\text{días\_antigüedad} / \text{vida\_media})}$$
  (Vida media por defecto: 365 días).
- Re-ranquear claims mediante evaluación condicional (por qué funciona, bajo qué condiciones y cuándo se rompe).

### RF-03: Generador de Planes Experimentales en 6 Fases
- Producir un `ExperimentPlan` jerárquico dividido estrictamente en:
  1. **Phase 1 - Validation Scheme:** Partición representativa libre de fugas.
  2. **Phase 2 - Fast Baseline:** Modelo simple, rápido y reproducible.
  3. **Phase 3 - Deep Diagnosis:** Auditoría de errores, residuos y falsos positivos/negativos.
  4. **Phase 4 - Model Improvements:** Feature engineering, adaptadores y funciones de pérdida personalizadas.
  5. **Phase 5 - Robustness & Ensembling:** Test-Time Augmentation (TTA), fusión de probabilidades y post-proceso.
  6. **Phase 6 - Submission Pipeline:** Serialización, verificación de tiempo en CPU/GPU de Kaggle y empaquetado final.

### RF-04: Conectores a Fuentes Externas y Triangulación
- arXiv / bioRxiv: Consulta y parseo de abstracts teóricos y ecuaciones.
- GitHub: Búsqueda de repositorios con código mantenido.
- Hugging Face Hub: Detección de backbones preentrenados y tokenizers.
- Kaggle API: Ingesta de write-ups ganadores e inspección de foros.

---

## 🔒 2. REQUERIMIENTOS NO FUNCIONALES
- Cobertura de tests unitarios: $\ge 95\%$.
- Compatibilidad: CPython $\ge 3.11$, Windows 11 y Linux (Ubuntu 22.04 LTS).
- Cero fugas de tokens o datos confidenciales.
