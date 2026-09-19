# ⚡ PROMPT ESPECIALIZADO: LA VÍA RÁPIDA (PLAYGROUND SERIES & COMMUNITY SPARRING)
### Para Google Deep Research / Gemini AI Premium / Perplexity Pro
**Misión:** Construcción del Pipeline Automatizado y Meta-Estrategias para Ganar Medallas en Torneos Quincenales/Mensuales de Kaggle.

---

<PROMPT_DEEP_RESEARCH_PLAYGROUND>
Actúa como un **Kaggle Grandmaster especializado en Kaggle Playground Series (Tabular y Multimodal) y Competencias Comunitarias**.

### 🎯 OBJETIVO DE LA INVESTIGACIÓN
Diseccionar y formalizar el **sistema operativo de alta velocidad** que permite a los competidores top ganar medallas y posicionarse consistentemente en el Top 1% en **Kaggle Playground Series** (temporadas 3, 4 y 5) y **Community Competitions**.

Estas competencias son el campo de entrenamiento más frecuente de Kaggle: se publican cada 2 a 4 semanas, utilizan datasets limpios o sintéticos generados por IA, y permiten ciclos de iteración muy rápidos sin la sobrecarga de torneos de 3 meses.

---

### 🔬 PREGUNTAS CLAVE DE INGENIERÍA PARA ESTA CATEGORÍA

1. **La Naturaleza de los Datos Sintéticos en Playground Series:**
   - En Playground, casi todos los datasets son generados sintéticamente a partir de datasets reales mediante modelos generativos (como CTGAN o similares).
   - ¿Qué artefactos o "huellas digitales" dejan estos generadores en los datos? (ej. variables categóricas continuizadas, redondeos anómalos, combinaciones imposibles en la realidad).
   - ¿Cómo utilizan los ganadores el dataset original/real como datos de entrenamiento adicionales o para calibrar distribuciones? ¿Cuándo ayuda y cuándo perjudica?

2. **El Pipeline Canónico de Ganador en Playground:**
   - **Ingeniería de Características Automatizada:** ¿Qué transformaciones automáticas son obligatorias? (Target Encoding fuera de pliegue / OOF, Frequency Encoding, interacciones polinomiales, agregaciones por grupo con media/std/skew, y transformaciones de clustering con K-Means o GMMs).
   - **El Trío Sagrado de GBDTs:** Hiperparámetros base de **LightGBM**, **XGBoost** y **CatBoost** que mejor generalizan sin sobreajustar.
   - **Modelos Complementarios de Diversidad:** ¿Qué redes tabulares (TabNet, ResNet tabular, MLP con embeddings, FT-Transformer) o modelos lineales aportan la ortogonalidad necesaria para el ensamble?

3. **La Ciencia del Ensamble Rápido en Playground:**
   - ¿Cómo combinan las predicciones para exprimir las últimas milésimas en el leaderboard? (Nelder-Mead optimization sobre OOF, Ridge regression, Hill Climbing o Rank Averaging).
   - ¿Por qué el promedio simple suele perder frente a la optimización de pesos restringida?

4. **Blindaje contra el Shakeup en Playground:**
   - Dado que el public leaderboard en Playground suele ser de solo el 20% de los datos de test, los shakeups son brutales.
   - ¿Qué esquema de validación cruzada (CV) de 5 o 10 pliegues es infalible? ¿Cómo detectan el sobreajuste a la tabla pública antes de enviar?

5. **Estrategia para Community Competitions:**
   - En torneos creados por la comunidad o universidades (con premios de hasta $5,000 USD para el host):
     - ¿Cuáles son las fugas de información más comunes que cometen los organizadores novatos? (ej. fuga temporal, IDs correlacionados con la variable objetivo, imágenes con metadatos EXIF no depurados).
     - ¿Cómo auditar rápidamente un dataset comunitario para detectar estas ventajas asimétricas en las primeras 24 horas?

### 📦 ENTREGABLE ESPERADO
- Un blueprint de código Python ejecutable (template modular) que automatice la ingesta, validación estratificada, entrenamiento multimodelo y ensamble óptimo para cualquier competencia Playground en menos de 1 hora de GPU.
- Lista de las 5 competencias Playground más representativas de los últimos 2 años y el truco exacto que dio la victoria al 1er lugar.
</PROMPT_DEEP_RESEARCH_PLAYGROUND>
