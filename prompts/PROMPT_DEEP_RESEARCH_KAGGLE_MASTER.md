# 🛰️ PROMPT MAESTRO PARA GOOGLE DEEP RESEARCH & AGENTES DE INVESTIGACIÓN PROFUNDA
### Misión: Atlas Canónico de Soluciones Ganadoras, Restricciones y Postmortems de Kaggle
**Destinatarios Ideales:** Google Deep Research (Gemini Advanced / AI Premium), Perplexity Pro Deep Research, OpenAI Deep Research, Claude Sonnet 3.5 / Opus.

---

> **INSTRUCCIONES DE USO PARA RAFA:**
> Copia y pega el bloque completo que se encuentra dentro de las etiquetas `<PROMPT_DEEP_RESEARCH>` directamente en tu herramienta de Deep Research. El prompt está optimizado para que el modelo navegue autónomamente por foros de Kaggle, arXiv, GitHub y Papers with Code durante 10-30 minutos y te entregue un dossier exhaustivo de nivel Grandmaster.

---

<PROMPT_DEEP_RESEARCH>
Actúa como un **Kaggle Grandmaster, Investigador Científico Senior en Machine Learning y Arquitecto de Sistemas de Inteligencia Competitiva**. 

### 🎯 OBJETIVO DE LA INVESTIGACIÓN
Tu objetivo es realizar una **investigación profunda, sistemática y exhaustiva** a lo largo de las competencias históricas y modernas más emblemáticas de la plataforma **Kaggle** (y plataformas análogas como DrivenData, AIcrowd y Zindi), con el fin de extraer los **mecanismos científicos reales, trucos empíricos, esquemas de validación y fallas condicionales** que separaron a los ganadores (Top 1% / Posiciones 1 a 5) del resto del leaderboard.

No busques resúmenes superficiales ni generalidades. Necesito **disección forense de ingeniería, código, ecuaciones y descubrimientos en los datos**.

---

### 🌐 ALCANCE DE LA INVESTIGACIÓN (CATEGORÍAS A CUBRIR)
Debes explorar e investigar en profundidad al menos **3 a 5 competencias emblemáticas por cada una de las siguientes 5 modalidades**:

1. **Datos Tabulares y Riesgo / Detección de Anomalías:**
   - *Ejemplos de referencia:* IEEE-CIS Fraud Detection, Home Credit Default Risk, American Express - Default Prediction, Jane Street Market Prediction, Kaggle TPS series.
2. **Visión por Computadora e Imágenes Médicas / Científicas:**
   - *Ejemplos de referencia:* RSNA Screening Mammography Breast Cancer Detection, RSNA Pulmonary Embolism, HuBMAP - Hacking the Kidney / Human BioMolecular Atlas, SIIM-ISIC Melanoma Classification, Severstal: Steel Defect Detection.
3. **Bioinformática, Espectrometría de Masas y Química Computacional:**
   - *Ejemplos de referencia:* Stanford Ribonanza RNA Folding, Open Problems - Multimodal Single-Cell Integration, CAFA 5 Protein Function Prediction, Enveda CASMI (Molecule ID Mass Spectra), Predicting Molecular Properties (CHAMPS).
4. **Procesamiento de Lenguaje Natural (NLP) y Razonamiento de LLMs:**
   - *Ejemplos de referencia:* Kaggle - LLM Science Exam, Feedback Prize (Predicting Effective Arguments), CommonLit Readability Prize, LMSYS Chatbot Arena Human Preference Predictions.
5. **Series Temporales, Pronóstico y Microestructura Financiera:**
   - *Ejemplos de referencia:* M5 Forecasting - Accuracy, Optiver - Realized Volatility Prediction, Ubiquant Market Prediction, G-Research Crypto Forecasting.

---

### 📋 ESQUEMA DE DISECCIÓN OBLIGATORIO POR CADA COMPETENCIA
Para cada una de las competencias analizadas, debes estructurar la información bajo este formato estricto:

#### 1. Ficha Técnica y ADN del Problema (*Problem DNA*)
- **Nombre de la Competencia, Año y Host.**
- **URL oficial en Kaggle y URL del foro de discusiones.**
- **Métrica Oficial de Evaluación:** (ej. LogLoss multiclase, pAUC, QWK, C-index, Pearson Correlation, Cosine Similarity, Dice/F1). Explica matemáticamente qué penaliza o premia esta métrica y si es diferenciable.
- **Restricciones de Entorno:** (Tiempo de inferencia en GPU/CPU, sumisión vía Notebook sin internet, límites de RAM, reglas sobre modelos preentrenados y datasets externos).

#### 2. La Verdad de la Validación (*Validation Scheme*)
- ¿Cuál fue el esquema de validación cruzada (CV) que correlacionó al 100% con el *Private Leaderboard*?
- ¿Cómo evitaron el temido *Shakeup* (caída drástica entre el Public y Private LB)?
- ¿Existió fuga de datos (*data leakage*) o cambio en la distribución (*train/test drift*)? ¿Cómo se detectó (ej. Adversarial Validation)?

#### 3. Anatomía de las Soluciones Ganadoras (Top 1 al Top 5)
- **El Hallazgo Clave en los Datos (*The Breakthrough*):** ¿Qué descubrieron en los datos que los demás no vieron? (ej. IDs secuenciales con información temporal, variables mal parseadas, sesgos de etiquetado, outliers con señal).
- **Ingesta y Preprocesamiento (`MOD_INGEST` & `MOD_SIGNAL`):** Tratamiento de nulos, normalización, aumentaciones críticas que dieron salto de puntaje (*magic features*).
- **Arquitecturas y Backbones (`MOD_ARCH`):** Modelos exactos utilizados (ej. LightGBM + CatBoost + XGBoost; ConvNeXt + EfficientNet-v2 + EVA-02; DeBERTa-v3 + Mistral LoRA; GNNs / ChemBERTa).
- **Funciones de Pérdida (`MOD_LOSS`):** ¿Usaron pérdidas estándar o custom losses diseñadas para la métrica? (ej. Focal Loss, Asymmetric Loss, Correlación de Pearson optimizada directamente, Soft Dice).
- **Ensamble y Post-procesamiento (`MOD_ENSEMBLE`):** Estrategia de blending (Rank Averaging, Nelder-Mead, Ridge Stacking, Out-of-Fold weights), Test-Time Augmentation (TTA), y optimización milimétrica de umbrales (*threshold tuning*).

#### 4. Catálogo de Fracasos (*Postmortem / What Didn't Work*)
- ¿Qué técnicas populares, modelos pesados o ideas obvias **fracasaron rotundamente** según los write-ups de los propios ganadores?
- ¿Por qué fallaron? (ej. sobreajuste a la semilla, gradientes inestables, incompatibilidad con la métrica).

#### 5. Triangulación Científica y Enlaces de Oro
- **Paper Teórico Base:** Título del paper y DOI / enlace en **arXiv** que formaliza el mecanismo usado.
- **Repositorio Oficial / Librería:** Enlace en **GitHub** con la implementación limpia y empaquetada.
- **Pesos Preentrenados:** Enlace al Model Hub de **Hugging Face** con los checkpoints oficiales utilizados.

---

### 📦 FORMATO FINAL DE ENTREGA
1. **Dossier Técnico Detallado:** Desarrolla cada competencia con explicaciones matemáticas y de ingeniería completas.
2. **Tabla Sinóptica Comparativa:** Una tabla comparativa con columnas: `[Competencia | Dominio | Métrica Oficial | Técnica Clave Ganadora | Causa Raíz de Fracaso Común | Enlace Paper/Repo]`.
3. **Bloque JSON Estructurado:** Al final, compila un resumen en formato JSON con la lista de `claims` condicionales (bajo qué condiciones usar cada técnica) para su ingesta directa en una base de datos vectorial de razonamiento automático.
</PROMPT_DEEP_RESEARCH>
