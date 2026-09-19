# 🌐 PROMPT MAESTRO UNIVERSAL: ECOSISTEMA COMPLETO DE CATEGORÍAS KAGGLE
### Para Google Deep Research / Gemini AI Premium / Perplexity Pro / OpenAI Deep Research
**Misión:** Mapeo Integral de Estrategias Ganadoras por Categoría de Competencia (Getting Started, Playground, Featured, Research, Community, Recruitment, Analytics) y Diseño del Motor de Decisión Estratégica.

---

> **INSTRUCCIONES DE USO PARA RAFA:**
> Copia y pega el bloque dentro de `<PROMPT_KAGGLE_UNIVERSAL_CATEGORIAS>` en Google Deep Research. El prompt le exige al modelo clasificar los patrones de victoria según el tipo de torneo, su frecuencia y el retorno de inversión (tiempo vs cómputo vs premios).

---

<PROMPT_KAGGLE_UNIVERSAL_CATEGORIAS>
Actúa como un **Kaggle Grandmaster, Estratega en Inteligencia Competitiva y Científico de Datos de Élite**.

### 🎯 OBJETIVO DE LA INVESTIGACIÓN
Realizar una **investigación profunda y transversal** sobre todo el ecosistema de competencias de Kaggle, estructurada obligatoriamente según su **clasificación oficial por categorías**, para determinar las **recetas ganadoras, plantillas de pipeline y patrones de diseño** específicos que funcionan en cada nivel.

En Kaggle, las competencias no son homogéneas: varían radicalmente en duración, dificultad, reglas de cómputo y premios (desde prestigio y medallas, hasta ofertas laborales y bolsas de $25,000 a más de $500,000 USD). Necesito que investigues y disecciones cómo ganar en cada una de las siguientes **dos grandes vertientes operativas**:

---

### 🏛️ VERTIENTE 1: LA VÍA RÁPIDA, PRÁCTICA CONTINUA & SPARRING (CICLOS CORTOS / ALTA FRECUENCIA)

#### 1. Playground Series (Retos Quincenales / Mensuales)
- **Naturaleza:** Datasets habitualmente sintéticos (generados a partir de datos reales con deep learning, ej. CTGAN) o limpios, con reglas estables y duración de 2 a 4 semanas. Premios de swag, medallas y reputación.
- **Investigación Requerida:**
  - ¿Cuál es la "fórmula estándar" del Top 1 al 5 en Playground Series?
  - ¿Cómo aprovechan los ganadores las particularidades de los datasets sintéticos? (ej. detección del generador original, extracción de distribuciones, explotación de redondeos y artefactos sintéticos).
  - ¿Cuáles son los pipelines automatizados que permiten obtener medallas con mínimo esfuerzo manual? (Ensamble de LightGBM + XGBoost + CatBoost + TabNet / PyTorch Tabular, tuning con Optuna, blending con Ridge o Nelder-Mead).
  - ¿Cómo evitan el overfitting cuando el public leaderboard representa solo un pequeño porcentaje?

#### 2. Community Competitions (Torneos Comunitarios y Universitarios)
- **Naturaleza:** Creados por universidades, ONGs, empresas medianas o usuarios de la comunidad. Kaggle premia a los hosts con hasta $5,000 USD mensuales por torneos de alta calidad.
- **Investigación Requerida:**
  - Patrones comunes en datos comunitarios: calidad variable de datos, etiquetas con ruido, fugas de información (*data leakage* inadvertido por el host en IDs, metadatos o nombres de archivo).
  - ¿Cómo explotan los ganadores las fugas y errores de planteamiento del host para asegurar el podio?
  - Estrategias de adaptación rápida a métricas no tradicionales o poco documentadas.

#### 3. Getting Started (Sparring Perpetuo de Calibración)
- **Naturaleza:** Competencias abiertas permanentes (Titanic, Spaceship Titanic, House Prices, Digit Recognizer).
- **Investigación Requerida:**
  - Cuáles son las mejores soluciones canónicas publicadas que sirven como "Golden Baselines" para calibrar y validar cualquier nuevo pipeline de ML.

---

### 🏆 VERTIENTE 2: GRANDES DESAFÍOS DE ALTO IMPACTO (COMPUTACIÓN PESADA, INDUSTRIA & FRONTERA CIENTÍFICA)

#### 4. Featured Competitions (Premios Monetarios: $25,000 a $500,000+ USD)
- **Naturaleza:** Problemas reales de patrocinadores corporativos de primer nivel (Google, Home Credit, Jane Street, Optiver, RSNA, American Express). Máxima competencia global donde participan los mejores equipos del mundo.
- **Investigación Requerida:**
  - ¿Cómo se estructura un equipo ganador de 3 a 4 personas durante 2 a 3 meses de torneo?
  - Esquemas de validación cruzada para blindarse contra el temido *Shakeup* (caídas de cientos de puestos en el Private Leaderboard).
  - Gestión de diversidad de modelos (GBDTs ortogonales con diferentes subconjuntos de features, redes neuronales profundas con semillas distintas, transformers).
  - Estrategias de sumisión final: ¿cómo seleccionan las 2 sumisiones finales entre cientos de experimentos?

#### 5. Research Competitions (Frontera Científica, Grants & Avance del SOTA)
- **Naturaleza:** Desafíos biológicos, médicos, físicos o de NLP complejo organizados por consorcios académicos (Nature, NeurIPS, CASMI, Stanford, Harvard, NIH), a menudo respaldados por el programa *Kaggle Research Grants*.
- **Investigación Requerida:**
  - ¿Por qué en estas competencias los modelos genéricos suelen fallar y se requiere modelado específico de dominio?
  - Casos de estudio concretos:
    * **Stanford Ribonanza RNA Folding:** Plegamiento de ARN con transformers y restricciones biofísicas.
    * **Enveda CASMI:** Identificación de moléculas pequeñas a partir de espectros de masas (MS/MS).
    * **CAFA (Critical Assessment of Function Annotation):** Predicción de función proteica y ontologías Gene Ontology (GO).
    * **RSNA Screening Mammography:** Detección de cáncer en mamografías con desbalance extremo y DICOM masivos.
  - ¿Cómo integran los ganadores el conocimiento de papers de arXiv/Nature con pesos preentrenados de Hugging Face y librerías especializadas (RDKit, Matchms, MONAI, Biopython)?

#### 6. Recruitment Competitions (Filtro Laboral & Empleo)
- **Naturaleza:** Desafíos patrocinados por empresas donde el premio principal es una entrevista o contratación directa.
- **Investigación Requerida:**
  - ¿Qué buscan los evaluadores más allá del puntaje final? (código limpio, reproducibilidad, modularidad, análisis de negocio y documentación).

#### 7. Analytics Competitions (Storytelling, EDA & Visualización)
- **Naturaleza:** Competencias de análisis de datos y notebooks donde se evalúa la narrativa, la profundidad exploratoria y la claridad de las visualizaciones interactivas.
- **Investigación Requerida:**
  - Estructura y patrones de los notebooks ganadores de medallas de oro en Analytics.

---

### 📋 MATRIZ DE SALIDA OBLIGATORIA

Para cada una de las 7 categorías, debes proporcionar:
1. **Perfil de la Categoría:** Frecuencia, duración típica, perfil de datos y tipos de premio.
2. **La Receta Técnica Ganadora:** Los 3 a 5 patrones de ingeniería que garantizan el éxito en esa categoría específica.
3. **Errores Fatales Comunes:** Por qué fallan los competidores promedio en esa categoría.
4. **Plantilla de Arquitectura Recomendada:** Desglose en los 6 bloques modulares (`MOD_INGEST`, `MOD_SIGNAL`, `MOD_SPLIT`, `MOD_ARCH`, `MOD_LOSS`, `MOD_ENSEMBLE`).
5. **Casos Reales Emblemáticos:** 2 o 3 ejemplos concretos con nombres de competencias y enlaces a write-ups ganadores.

---

### 📦 FORMATO FINAL DE ENTREGA
- Documento exhaustivo en Markdown profesional con rigor científico y técnico.
- **Tabla Resumen Estratégica:** Comparativa de `[Categoría | Frecuencia | Esfuerzo de Cómputo | Retorno/Premio | Estrategia Óptima para Ganar]`.
- **Estructura JSON de Reglas:** Bloque de reglas condicionales al final para ser incorporado en nuestro motor de razonamiento automático (CMRE).
</PROMPT_KAGGLE_UNIVERSAL_CATEGORIAS>
