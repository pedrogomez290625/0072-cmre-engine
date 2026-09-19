Perfecto. Tomo **tu idea original**, la **crítica que recibiste**, todo el razonamiento previo y lo unifico en un solo documento: **qué vamos a construir, por qué puede ser una ventaja real, cómo se diseña, qué datos/ontología/arquitectura necesita y cuál es el plan de proyecto detallado para ejecutarlo sin perdernos en teorías ni en un scraper inútil**.

Voy a llamar al proyecto, de forma provisional:

# CMRE — Competitive ML Reasoning Engine  
## Motor de Razonamiento Científico para Competencias de Machine Learning

---

# 1. Resumen ejecutivo unificado

La idea original era construir un sistema que extrajera y clasificara código y write-ups ganadores de plataformas como Kaggle, DrivenData, Zindi y AIcrowd, los descompusiera en bloques funcionales mediante análisis sintáctico, los vinculara con papers en arXiv, repositorios en GitHub y pesos en Hugging Face, y luego permitiera resolver nuevas competencias ensamblando módulos validados.

Esa idea tiene una semilla muy buena, pero sola no basta. Si el diferencial es “tengo más código scrapeado”, eso se vuelve commodity. El verdadero edge está en convertir ese conocimiento en un **motor de razonamiento competitivo** que pueda:

1. Analizar una nueva competencia no por su superficie, sino por sus **restricciones matemáticas, estadísticas, operativas y regulatorias**.
2. Recuperar técnicas no solo por similitud superficial, sino por **mecanismo científico transferible**.
3. Explicar **por qué una técnica puede funcionar**, **bajo qué condiciones**, **con qué evidencia**, **con qué riesgo** y **cuándo se rompe**.
4. Priorizar experimentos según impacto esperado, costo, incertidumbre y probabilidad de victoria.
5. Tratar la **validación** como ciudadana de primera clase, porque muchas competencias se pierden por validación mal diseñada, no por modelo débil.
6. Registrar no solo victorias, sino **fracasos condicionales**: qué no funcionó, en qué contexto y por qué.
7. Extraer insights narrativos de write-ups: leaks, bugs de parseo, patrones en test, trampas de leaderboard, trucos específicos de plataforma, descubrimientos sobre los datos.
8. Alimentar un ciclo de aprendizaje continuo después de cada competencia.

En una frase:

> CMRE no es un catálogo de soluciones ganadoras. Es un sistema de razonamiento científico que transforma write-ups, notebooks, papers, repositorios, modelos y fracasos históricos en decisiones accionables para ganar competencias nuevas.

---

# 2. Tesis del proyecto

La tesis unificada queda así:

> Construiremos un motor de inteligencia competitiva que combine una base de conocimiento evidencial con una capa de razonamiento sobre restricciones. El sistema no se limita a almacenar código ganador, sino que descompone competencias en perfiles estructurales —métrica, modalidad, validación, drift, leak, compute, licencias, ruido, desbalance, estructura temporal, grupos, restricciones de negocio— y usa ese perfil para recuperar mecanismos científicos relevantes, evaluar sus condiciones de aplicación y ruptura, y generar un plan de experimentos priorizado. Cada resultado, positivo o negativo, retroalimenta la base, creando una memoria acumulativa de qué funciona, cuándo falla y por qué. La ventaja competitiva no está en tener más datos, sino en decidir mejor y más rápido bajo incertidumbre.

---

# 3. Qué problema real resuelve

En competencias de ML, los participantes suelen perder por razones como:

- validación incorrecta;
- overfitting al leaderboard público;
- no detectar leakage;
- ignorar shift entre train y test;
- usar técnicas famosas sin entender condiciones;
- perder tiempo en arquitecturas complejas cuando faltaba un baseline robusto;
- no optimizar correctamente la métrica;
- no hacer postprocessing adecuado;
- violar reglas de datos externos o modelos preentrenados;
- no registrar aprendizajes de competencias anteriores;
- repetir errores porque el conocimiento está disperso.

CMRE ataca ese problema convirtiendo conocimiento disperso en:

- diagnóstico estructural del problema;
- recomendaciones condicionales;
- planes experimentales priorizados;
- alertas de riesgo;
- memoria de fracasos;
- transferencia entre dominios;
- trazabilidad de evidencia.

---

# 4. Principios de diseño no negociables

Estos principios unifican tu idea original y la crítica recibida.

## Principio 1: Validación antes que arquitectura

La pregunta no es primero “qué modelo uso”, sino:

> ¿Cómo sé si estoy mejorando de verdad?

El sistema debe tratar la validación como objeto central: tipo de split, agrupaciones, temporalidad, estratificación, estabilidad por seed, segmentes, adversarial validation, simulación de train/test shift, consistencia público/privado.

---

## Principio 2: Descomposición por restricciones, no por sintaxis

El AST y la clasificación en bloques como “ingesta, pérdida, arquitectura, ensamble” son útiles, pero insuficientes.

Hay que modelar restricciones profundas:

- ¿La métrica es diferenciable?
- ¿Premia ranking, calibración, recall, precisión, error absoluto, colas, estabilidad?
- ¿Los datos tienen leak detectable?
- ¿El test es IID o OOD?
- ¿Hay dependencia temporal?
- ¿Hay grupos naturales?
- ¿Hay etiquetas ruidosas?
- ¿Hay clases minoritarias críticas?
- ¿Hay restricciones de latencia, memoria, interpretabilidad, licencia o cómputo?
- ¿Se permiten datos externos?
- ¿Se permiten modelos preentrenados?
- ¿El leaderboard público puede ser engañoso?

---

## Principio 3: Evidencia condicional

No basta con decir:

> “LightGBM es bueno para tabular.”

Hay que decir:

> “LightGBM suele ser fuerte baseline en tabular de tamaño medio/grande cuando hay features numéricas y categóricas, compute limitado y validación creíble. Puede fallar si hay leakage temporal, alta cardinalidad mal manejada, estructura secuencial fuerte, necesidad de restricciones duras o dataset muy pequeño donde un modelo lineal regularizado compite mejor.”

Cada técnica debe estar asociada a:

- mecanismo;
- condiciones de aplicabilidad;
- contraindicaciones;
- evidencia;
- costo;
- riesgo;
- nivel de confianza.

---

## Principio 4: Catálogo de fracasos

El sistema debe guardar activamente:

- técnicas que no funcionaron;
- por qué no funcionaron;
- en qué perfil de problema fallaron;
- qué síntoma tuvieron;
- qué lección quedó.

Eso es tan valioso como guardar soluciones ganadoras.

---

## Principio 5: Insights narrativos que no se extraen con AST

Muchos ganadores no ganan por la arquitectura, sino por descubrir algo específico de los datos:

- una columna mal parseada;
- un leak en IDs;
- un patrón en test que no estaba en train;
- una fecha que revela split;
- un outlier estructural;
- una métrica que premia un subconjunto raro;
- un truco de postprocessing;
- una validación que coincide mejor con el privado.

Eso se extrae leyendo write-ups con un LLM orientado a ML, pero siempre con citación, estructura y validación humana.

---

## Principio 6: Transferencia por mecanismo científico

No transferir solo “competencias parecidas”. Transferir mecanismos:

- regularización;
- invariancia;
- manejo de incertidumbre;
- aprovechamiento de datos no etiquetados;
- diversidad de ensemble;
- alineación con métrica;
- robustez a ruido;
- optimización restringida;
- representación;
- postprocessing;
- calibración;
- domain adaptation;
- curriculum learning;
- self-supervision;
- distillation.

Esto permite llevar ideas desde CV a NLP, desde forecasting a anomaly detection, desde RL a scheduling, desde causal inference a feature selection.

---

## Principio 7: Proveniencia y licencia obligatorias

Nada entra al sistema sin:

- fuente;
- URL;
- fecha;
- autor;
- plataforma;
- licencia;
- estado de permisividad;
- hash o versionado;
- relación con paper/repo/pesos;
- nivel de evidencia.

Si la licencia es desconocida o restrictiva, el artefacto no se usa automáticamente.

---

## Principio 8: Humano en el loop

Un LLM puede ayudar a extraer, resumir y proponer, pero no puede ser la única autoridad.

Se necesita:

- esquemas estructurados;
- citación obligatoria;
- niveles de evidencia;
- revisión humana;
- validación experimental;
- feedback posterior.

---

## Principio 9: Empezar estrecho para escalar bien

No construir “el cerebro universal de todas las competencias” desde el día uno.

Empezar por un vertical rentable:

> Competencias tabulares de clasificación/regresión en Kaggle/DrivenData, con foco en validación, leakage, drift y baselines fuertes.

Luego expandir a CV, NLP, series temporales, graphs, multimodal.

---

# 5. Qué es CMRE y qué no es

## Qué es

CMRE es:

- un reasoning engine;
- una knowledge base evidencial;
- un profiler de problemas;
- un generador de planes experimentales;
- un registro de fracasos condicionales;
- un sistema de transferencia científica;
- un copiloto competitivo;
- una memoria organizacional para ganar competencias.

## Qué no es

No es:

- solo un scraper;
- solo Google Drive con notebooks;
- solo un parser AST;
- solo un buscador de código;
- solo un chatbot de ML;
- solo un repositorio de papers;
- solo un ensemble automático;
- una garantía de medalla;
- un sistema para violar reglas o usar datos privados filtrados.

---

# 6. Objetivo del proyecto

El objetivo no es “archivar conocimiento”.

El objetivo es:

> Aumentar sistemáticamente la probabilidad de ganar competencias mediante mejores decisiones experimentales, mejor validación, mejor transferencia de técnicas y mejor aprendizaje acumulado.

Objetivos concretos:

1. Reducir el tiempo entre inscripción y primer baseline válido.
2. Detectar riesgos de validación, leakage y drift antes de perder el leaderboard.
3. Recomendar técnicas con justificación condicional, no solo populares.
4. Priorizar experimentos de alto ROI.
5. Registrar aprendizajes de cada competencia.
6. Crear un activo único: memoria de éxitos y fracasos contextualizados.
7. Eventualmente mejorar medals per competition y top-k rate.

---

# 7. Usuarios y casos de uso

## Usuario principal

Competidor individual o equipo pequeño que participa en Kaggle, DrivenData, Zindi, AIcrowd u otras plataformas.

## Casos de uso

### Caso 1: Análisis previo a competir

Input: descripción de competencia, datos, métrica, reglas.

Output:

- Problem DNA;
- riesgos principales;
- validación recomendada;
- anti-patrones;
- técnicas candidatas;
- plan de primeras 24/48 horas;
- señales de alarma.

---

### Caso 2: Durante la competencia

Input: resultados parciales, errores, scores, experimentos.

Output:

- hipótesis siguientes;
- diagnóstico de estancamiento;
- sugerencias de ensemble/postprocessing;
- alerta de overfitting al público;
- priorización de experimentos.

---

### Caso 3: Post-mortem

Input: resultado final, experimentos, logs, write-up propio.

Output:

- reglas aprendidas;
- fracasos condicionales;
- actualización de evidencia;
- ajustes a priors;
- insumos para próximas competencias.

---

### Caso 4: Entrenamiento y scouting

Input: competencias pasadas.

Output:

- análisis de qué hizo ganar a otros;
- extracción de mecanismos;
- comparación con soluciones propias;
- construcción de base de conocimiento.

---

# 8. Arquitectura general del sistema

El sistema se divide en nueve capas.

```text
┌──────────────────────────────────────────────┐
│ 1. Ingestion & Provenance                    │
│    Kaggle, DrivenData, Zindi, AIcrowd,       │
│    GitHub, arXiv, Hugging Face, write-ups    │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 2. Normalization & Extraction                │
│    notebooks, AST, LLM narrative extraction, │
│    paper parsing, model metadata, licenses   │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 3. Knowledge Base / Evidence Graph           │
│    techniques, mechanisms, claims,           │
│    conditions, risks, failures, artifacts    │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 4. Problem Profiler                          │
│    Problem DNA: task, modality, metric,      │
│    constraints, drift, leak, compute, rules  │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 5. Reasoning Engine                          │
│    retrieve mechanisms, score applicability, │
│    explain conditions and failure modes      │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 6. Experiment Planner                        │
│    validation plan, baselines, ablations,    │
│    ensemble, postprocessing, risk tests      │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 7. Execution Lab                             │
│    notebooks, containers, MLflow/W&B,        │
│    reproducible runs, metrics tracking       │
└─────────────────────┬────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 8. Feedback Loop                             │
│    outcomes, failures, evidence updates,     │
│    priors recalibration, post-mortems        │
└──────────────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────┐
│ 9. Governance & Evaluation                   │
│    licenses, ToS, attribution, QA, metrics   │
└──────────────────────────────────────────────┘
```

---

# 9. Componentes detallados

---

## 9.1 Capa de ingesta y proveniencia

### Fuentes

- Kaggle notebooks públicos;
- write-ups oficiales o de equipos;
- DrivenData;
- Zindi;
- AIcrowd;
- CodaLab;
- GitHub;
- arXiv;
- Semantic Scholar;
- Papers With Code;
- Hugging Face;
- discusiones de foro;
- repositorios post-competencia;
- datasets públicos permitidos.

### Almacenamiento crudo

Google Drive puede servir como **zona de aterrizaje** para documentos, PDFs, notebooks descargados manualmente o exports permitidos.

Pero el cerebro no puede ser Drive.

Drive = raw dropbox.

Sistema real = base estructurada + object storage + índice vectorial + registro de experimentos.

### Metadatos obligatorios por artefacto

```json
{
  "artifact_id": "...",
  "source_type": "notebook|writeup|paper|repo|model|dataset",
  "platform": "Kaggle|DrivenData|Zindi|AIcrowd|GitHub|arXiv|HuggingFace",
  "url": "...",
  "author": "...",
  "published_at": "...",
  "competition_id": "...",
  "placement": "gold|silver|bronze|top10|unknown",
  "license": "MIT|Apache-2.0|CC-BY|Kaggle-rule|unknown|restricted",
  "license_status": "allowed|restricted|forbidden|unknown",
  "content_hash": "...",
  "raw_storage_path": "...",
  "provenance_notes": "..."
}
```

### Regla dura

Si `license_status = unknown` o `restricted`, el artefacto no entra al pipeline automático de recomendación. Puede guardarse como referencia, pero no como componente reutilizable.

---

## 9.2 Capa de normalización y extracción

Esta capa convierte artefactos brutos en estructuras utilizables.

### Para notebooks

Se debe extraer:

- celdas markdown;
- celdas de código;
- outputs;
- imports;
- funciones de preprocessing;
- funciones de training;
- funciones de inference;
- hiperparámetros;
- seeds;
- métricas reportadas;
- validación usada;
- uso de datos externos;
- uso de modelos preentrenados;
- lógica de ensemble;
- postprocessing;
- dependencias entre celdas;
- posibles leaks;
- versiones de librerías, si están registradas.

Herramientas:

- `nbformat` para leer `.ipynb`;
- AST de Python;
- análisis de control flow básico;
- LLM para resumir intención de bloques;
- heurísticas para detectar leakage sospechoso.

### Para código Python

Extraer:

- clases de modelo;
- loss functions;
- optimizers;
- schedulers;
- transforms/augmentations;
- datasets/dataloaders;
- training loops;
- inference loops;
- ensemble logic;
- utils de métricas;
- configuración vía argparse/YAML/JSON.

### Para papers

Extraer:

- método;
- ecuaciones clave;
- supuestos;
- datasets usados;
- métricas;
- ablations;
- limitaciones;
- enlaces a código;
- condiciones teóricas de validez.

### Para Hugging Face

Extraer:

- task;
- framework;
- tamaño;
- licencia;
- dataset de pretraining;
- restricciones comerciales;
- capacidad de fine-tuning;
- artefactos asociados.

### Para write-ups narrativos

Aquí entra fuertemente la crítica que recibiste.

El LLM debe leer la narrativa y extraer:

- descubrimientos sobre los datos;
- leaks encontrados;
- bugs de parseo;
- patrones en test;
- trampas de leaderboard;
- decisiones de validación;
- tricks permitidos;
- tricks grises;
- razones por las que algo funcionó;
- razones por las que algo falló;
- insights no evidentes en el código.

Cada extracción debe tener cita al fragmento original.

Ejemplo de salida estructurada:

```json
{
  "insight_type": "data_leak",
  "claim": "El autor detectó que ciertos IDs de cliente aparecían tanto en train como en test con comportamiento temporal inconsistente.",
  "evidence_quote": "...",
  "source_artifact_id": "...",
  "problem_profile_tags": ["tabular", "temporal", "id_leak_risk"],
  "actionable_rule": "Si hay IDs de entidad, verificar solapamiento train/test y consistencia temporal antes de confiar en CV aleatoria."
}
```

---

## 9.3 Knowledge Base / Evidence Graph

Esta es la memoria del sistema.

No debe ser solo una lista de técnicas. Debe ser un grafo de afirmaciones condicionales.

### Entidades principales

#### Competition

```json
{
  "competition_id": "...",
  "platform": "Kaggle",
  "title": "...",
  "url": "...",
  "task_type": "binary_classification",
  "modality": "tabular",
  "metric": "average_precision",
  "rules": {
    "external_data_allowed": true,
    "pretrained_models_allowed": true,
    "team_size_limit": 5,
    "submission_limit": 5
  },
  "data_profile": {},
  "status": "finished",
  "license_notes": "..."
}
```

#### Solution

```json
{
  "solution_id": "...",
  "competition_id": "...",
  "author": "...",
  "placement": "gold",
  "artifact_type": "notebook|writeup|repo",
  "url": "...",
  "license": "...",
  "published_at": "...",
  "reproducibility_score": 0.0
}
```

#### Technique

```json
{
  "technique_id": "...",
  "name": "focal_loss",
  "category": "loss_function",
  "mechanism": "down_weight_easy_examples",
  "description": "...",
  "paper_refs": ["arXiv:1708.02002"],
  "code_refs": ["github:..."],
  "model_refs": ["hf:..."]
}
```

#### Mechanism

```json
{
  "mechanism_id": "regularization",
  "name": "Regularización",
  "description": "Reduce varianza o impide overfitting a patrones espurios.",
  "examples": ["dropout", "weight_decay", "label_smoothing", "augmentation", "early_stopping"]
}
```

#### Claim

Un claim es el corazón.

```json
{
  "claim_id": "...",
  "technique_id": "focal_loss",
  "mechanism_id": "metric_alignment",
  "problem_profile_id": "...",
  "statement": "Focal loss puede mejorar Average Precision en clasificación binaria altamente desbalanceada cuando se usa red neuronal y la métrica premia la clase minoritaria.",
  "applicable_when": [
    "class imbalance > 1:20",
    "metric sensitive to minority class",
    "model is neural network",
    "labels not extremely noisy"
  ],
  "not_recommended_when": [
    "primary metric is calibrated log-loss only",
    "dataset is small and noisy",
    "tree-based model is stronger baseline",
    "focal hyperparameters are untuned"
  ],
  "expected_effect": {
    "metric": "average_precision",
    "direction": "positive",
    "magnitude_range": "+0.001 to +0.010",
    "confidence": 0.62
  },
  "cost": {
    "implementation": "low",
    "tuning": "medium",
    "compute": "low"
  },
  "risk": {
    "overfit_public_lb": "medium",
    "instability_seed": "medium",
    "license_issue": "none"
  },
  "evidence": [
    {
      "source_type": "competition_writeup",
      "platform": "Kaggle",
      "competition": "...",
      "placement": "gold",
      "reproducibility_score": 0.71
    },
    {
      "source_type": "paper",
      "reference": "arXiv:1708.02002"
    }
  ],
  "evidence_level": 3,
  "license_status": "allowed"
}
```

#### Failure

```json
{
  "failure_id": "...",
  "technique_id": "...",
  "problem_profile_id": "...",
  "statement": "Focal loss empeoró log-loss en dataset pequeño con etiquetas ruidosas.",
  "symptoms": [
    "high variance across seeds",
    "public gain but private drop",
    "poor calibration"
  ],
  "root_cause_hypothesis": "The loss amplified noisy minority examples.",
  "lesson": "Do not use focal loss as primary objective when calibration is critical and labels are noisy.",
  "condition": "small dataset + noisy labels + log-loss metric",
  "evidence_level": 4
}
```

#### ProblemProfile

```json
{
  "profile_id": "...",
  "task": "binary_classification",
  "modality": "tabular",
  "metric_family": "ranking",
  "has_temporal_component": true,
  "has_group_structure": false,
  "class_imbalance": "extreme",
  "label_noise_risk": "medium",
  "distribution_shift_risk": "high",
  "leak_risk": ["temporal", "id"],
  "external_data_allowed": true,
  "pretrained_models_allowed": false,
  "compute_constraint": "moderate",
  "interpretability_required": false,
  "embedding": [...]
}
```

#### Experiment

```json
{
  "experiment_id": "...",
  "competition_id": "...",
  "hypothesis": "Temporal CV reduces public/private gap compared to random KFold.",
  "techniques_used": ["time_series_split", "lightgbm", "adversarial_validation"],
  "config": {},
  "result": {
    "cv_score": 0.72,
    "public_lb": 0.74,
    "private_lb": 0.69,
    "gap": -0.03
  },
  "decision": "keep",
  "notes": "Random KFold overestimated performance by 0.05."
}
```

---

# 10. Ontología de mecanismos transferibles

Esta ontología permite reutilizar descubrimientos científicos entre competencias similares o no.

## Mecanismo: Regularización

Reduce varianza o previene overfitting.

Ejemplos:

- dropout;
- weight decay;
- early stopping;
- label smoothing;
- data augmentation;
- mixup;
- cutmix;
- stochastic depth;
- noise injection;
- ensembling.

Transferible entre:

- CV;
- NLP;
- tabular;
- audio;
- time series.

---

## Mecanismo: Invariancia

Impone estructura que el modelo debe respetar.

Ejemplos:

- augmentation geométrica;
- masking;
- time warping;
- permutation invariance;
- equivariant networks;
- domain adaptation;
- invariant risk minimization.

 Útil cuando el problema exige robustez a transformaciones o cambios de dominio.

---

## Mecanismo: Manejo de incertidumbre

Modela confianza calibrada o riesgo.

Ejemplos:

- Bayesian neural networks;
- deep ensembles;
- MC dropout;
- quantile regression;
- conformal prediction;
- probabilistic forecasting;
- temperature scaling;
- isotonic regression.

Útil cuando la métrica premia calibración o cuando hay riesgo operativo.

---

## Mecanismo: Aprovechamiento de datos no etiquetados

Usa test o datos externos sin labels.

Ejemplos:

- pseudo-labeling;
- self-training;
- consistency regularization;
- contrastive learning;
- masked autoencoders;
- distillation;
- semi-supervised learning;
- transductive learning.

Muy común cuando hay poco train y mucho test.

---

## Mecanismo: Diversidad de ensemble

Combina modelos con errores decorrelacionados.

Ejemplos:

- diferentes arquitecturas;
- diferentes seeds;
- diferentes folds;
- diferentes preprocessings;
- diferentes losses;
- bagging;
- stacking;
- snapshot ensembles;
- SWA;
- model soup.

El sistema debe modelar cuándo la diversidad ayuda y cuándo solo añade ruido.

---

## Mecanismo: Alineación con métrica

Optimiza directamente o aproxima la métrica de evaluación.

Ejemplos:

- threshold optimization;
- focal loss;
- weighted cross-entropy;
- ranking losses;
- soft average precision;
- differentiable surrogate losses;
- postprocessing;
- calibration.

---

## Mecanismo: Robustez a ruido

Tolera etiquetas sucias, outliers o mediciones corruptas.

Ejemplos:

- Huber loss;
- trimmed losses;
- confident learning;
- co-teaching;
- label cleaning;
- ensemble disagreement;
- data filtering;
- robust aggregation.

---

## Mecanismo: Optimización restringida

Incorpora conocimiento de dominio como constraint.

Ejemplos:

- monotonic constraints;
- integer constraints;
- budget constraints;
- fairness constraints;
- hierarchical reconciliation;
- constrained decoding;
- rule-based postprocessing.

---

## Mecanismo: Representación

Aprende features útiles.

Ejemplos:

- embeddings;
- target encoding regularizado;
- feature hashing;
- autoencoders;
- contrastive representations;
- foundation models;
- dimensionality reduction.

---

## Mecanismo: Postprocessing

Ajusta salida final sin reentrenar.

Ejemplos:

- clipping;
- rounding;
- smoothing;
- calibration;
- threshold tuning;
- hierarchical aggregation;
- business rules;
- outlier correction.

---

# 11. Problem Profiler: análisis profundo de una competencia nueva

Esta es una de las piezas clave del diferenciador.

El profiler genera un **Problem DNA**.

## Capa 1: Superficie

- tarea;
- modalidad;
- métrica;
- formato de submission;
- tamaño de train/test;
- número de clases;
- balance;
- missing values;
- cardinalidad;
- longitud de secuencias;
- resolución;
- frecuencia temporal;
- reglas;
- límites de cómputo;
- datos externos;
- modelos preentrenados;
- tiempo restante.

## Capa 2: Estructura estadística

- ¿la métrica premia ranking o calibración?
- ¿hay ruido en etiquetas?
- ¿hay label leakage potencial?
- ¿hay feature leakage temporal?
- ¿público y privado pueden diferir?
- ¿hay covariate shift?
- ¿hay concept drift?
- ¿hay clases raras importantes?
- ¿hay outliers estructurales?
- ¿hay dependencias temporales?
- ¿hay grouping natural?
- ¿hay jerarquías?
- ¿hay restricciones de negocio?
- ¿se requiere interpretabilidad?
- ¿hay fairness constraints?
- ¿hay latencia máxima?
- ¿hay límite de memoria?
- ¿se permite pseudo-labeling?
- ¿se permite test-time augmentation?
- ¿el leaderboard público es engañoso?

## Capa 3: Restricciones matemáticas fundamentales

Ejemplos:

### Clasificación binaria desbalanceada

Objeto subyacente:

- estimar `P(y=1|x)`;
- métrica sensible a minoría;
- trade-off recall/precisión;
- necesidad de calibración o ranking;
- varianza alta en clase positiva.

Mecanismos relevantes:

- class weighting;
- focal loss;
- balanced sampling;
- threshold tuning;
- isotonic/Platt calibration;
- cost-sensitive learning;
- ensemble diversity;
- monotonic constraints si hay dominio.

---

### Regresión con colas pesadas

Objeto subyacente:

- error cuadrático castiga outliers;
- target no gaussiano;
- métrica puede ser RMSE, MAE, RMSLE, MAPE, WMAPE.

Mecanismos relevantes:

- log transform;
- Huber loss;
- quantile regression;
- robust losses;
- winsorizing;
- target clipping;
- mixture density networks;
- ensemble robusto.

---

### Visión con pocos datos y dominio distinto

Objeto subyacente:

- high variance;
- domain gap;
- necesidad de invarianzas;
- overfitting severo.

Mecanismos relevantes:

- pretrained backbone;
- progressive resizing;
- mixup/cutmix;
- self-supervised learning;
- test-time adaptation;
- distillation;
- LoRA/adapters;
- strong augmentation;
- ensemble diverso.

---

### NLP con etiquetas ruidosas

Objeto subyacente:

- label noise;
- anotación inconsistente;
- overfitting a errores humanos.

Mecanismos relevantes:

- label smoothing;
- confident learning;
- noise-robust losses;
- co-teaching;
- ensemble disagreement;
- data filtering;
- cross-validation por annotator;
- semi-supervised learning.

---

### Series temporales con cambio de régimen

Objeto subyacente:

- no estacionariedad;
- estructura temporal compleja;
- múltiples horizontes;
- covariates exógenos.

Mecanismos relevantes:

- direct vs recursive forecasting;
- temporal convolution;
- transformers temporales;
- N-BEATS/N-HiTS;
- calendar features;
- normalization por serie;
- probabilistic forecasting;
- quantile losses;
- rolling origin validation.

---

# 12. Reasoning Engine: cómo decide

El reasoning engine no responde “qué técnica usar”.

Responde:

> “Dado este perfil de problema, qué mecanismos son relevantes, con qué evidencia, bajo qué condiciones, con qué riesgo y en qué orden conviene probarlos.”

## Flujo

```text
1. Recibir competencia.
2. Generar Problem DNA.
3. Identificar restricciones críticas.
4. Recuperar claims/mecanismos relevantes.
5. Filtrar por licencia, compute, reglas y viabilidad.
6. Scorear por utilidad esperada.
7. Explicar condiciones de aplicación y ruptura.
8. Generar plan experimental.
9. Ejecutar o sugerir ejecución.
10. Registrar resultado.
11. Actualizar evidencia y fracasos.
```

## Función de score conceptual

No hace falta una fórmula perfecta, pero sí un principio:

```text
PriorityScore =
  MechanismFit
  × EvidenceStrength
  × ExpectedLift
  × ConstraintCompatibility
  ÷ (ImplementationCost + TuningCost + ComputeCost + Risk + Uncertainty)
```

Donde:

- `MechanismFit`: qué tan bien el mecanismo ataca la restricción central del problema.
- `EvidenceStrength`: nivel de respaldo empírico/teórico.
- `ExpectedLift`: mejora esperada en métrica.
- `ConstraintCompatibility`: cumple reglas, licencia, compute, latencia.
- `Risk`: overfitting, inestabilidad, leakage, ilegalidad, fragilidad.
- `Uncertainty`: cuán poco se sabe del efecto en este contexto.

El sistema debe mostrar siempre:

- por qué recomienda;
- por qué descarta;
- qué podría romper la recomendación;
- qué experimento la validaría barato.

---

# 13. Experiment Planner: plan de batalla

El planner convierte recomendaciones en secuencia ejecutable.

No dice:

> “Probá 50 modelos.”

Dice:

```text
Fase 1: Validación creíble
- objetivo: construir una CV que simule el test;
- acciones: temporal split, group split, adversarial validation;
- criterio de éxito: gap público/privado razonable y estabilidad;
- riesgo: usar KFold aleatorio en datos temporales.

Fase 2: Baseline fuerte
- objetivos: capturar señal principal rápido;
- acciones: LightGBM + CatBoost + linear baseline;
- criterio de éxito: mejora consistente sobre dummy;
- riesgo: overfitting por tuning excesivo temprano.

Fase 3: Diagnóstico
- acciones: feature importance, error analysis por segmento, leak checks, drift checks;
- criterio de éxito: identificar restricción dominante;
- riesgo: mirar solo promedio global.

Fase 4: Mejoras de alto ROI
- técnicas condicionales al Problem DNA;
- hipótesis explícitas;
- orden por expected value.

Fase 5: Robustez
- seeds;
- folds;
- stress tests;
- subperíodos;
- perturbaciones sintéticas.

Fase 6: Submission final
- ensemble conservador;
- calibración/postprocessing;
- documentación de riesgo;
- plan B si leaderboard privado cambia.
```

---

# 14. Execution Lab: donde el sistema deja de ser teoría

En MVP, el Execution Lab puede ser semiautomático.

En producción, debería permitir:

- correr baselines reproducibles;
- registrar experimentos;
- comparar configs;
- guardar artefactos;
- trackear métricas;
- reproducir con container;
- versionar datos y código;
- generar informes automáticos.

Herramientas:

- MLflow o Weights & Biases;
- Docker;
- DVC;
- Git;
- object storage;
- notebooks ejecutables;
- scripts parametrizados.

No es necesario construir esto completo al inicio, pero el diseño debe预留 espacio para ello.

---

# 15. Feedback Loop: aprendizaje continuo

Después de cada competencia o experimento, se registra:

- qué técnica se probó;
- en qué perfil;
- qué resultado tuvo;
- si fue reproducible;
- si dependió de seed;
- si mejoró público pero no privado;
- si violaba reglas;
- si fue costo-efectiva;
- qué lección queda.

Actualizaciones:

- subir/bajar evidencia de claims;
- añadir condiciones de ruptura;
- crear failure records;
- ajustar priors de scoring;
- refinar ontología;
- detectar sesgos temporales;
- marcar técnicas obsoletas.

Esto crea el activo difícil de copiar:

> Memoria contextualizada de éxitos y fracasos competitivos.

---

# 16. Modelo de datos mínimo recomendado

Para no complicar demasiado al inicio, yo usaría una base relacional con extensiones vectoriales y, opcionalmente, un grafo más adelante.

## Tablas/core entities

### artifacts

```text
artifact_id
source_type
platform
url
author
published_at
competition_id
license
license_status
content_hash
raw_path
metadata_json
```

### competitions

```text
competition_id
platform
title
url
task_type
modality
metric
rules_json
data_profile_json
status
```

### solutions

```text
solution_id
competition_id
artifact_id
author
placement
reproducibility_score
summary
```

### techniques

```text
technique_id
name
category
mechanism_id
description
paper_refs
code_refs
model_refs
```

### mechanisms

```text
mechanism_id
name
description
parent_mechanism
```

### claims

```text
claim_id
technique_id
mechanism_id
problem_profile_id
statement
applicable_when_json
not_recommended_when_json
expected_effect_json
cost_json
risk_json
evidence_level
license_status
```

### failures

```text
failure_id
technique_id
problem_profile_id
statement
symptoms_json
root_cause_hypothesis
lesson
condition_json
evidence_level
```

### problem_profiles

```text
profile_id
competition_id
task
modality
metric_family
features_json
risks_json
constraints_json
embedding_vector
```

### experiments

```text
experiment_id
competition_id
hypothesis
techniques_used_json
config_json
result_json
decision
notes
run_id
```

### evidence_links

```text
evidence_id
claim_id
artifact_id
source_type
quote
url
confidence
```

---

# 17. Diferenciador real del proyecto

El diferenciador no es:

- scrapear más;
- tener más notebooks;
- parsear AST;
- linkar papers;
- guardar pesos.

El diferenciador es:

1. **Problem profiling profundo**  
   Analizar competencias por restricciones, no por etiquetas superficiales.

2. **Transferencia por mecanismo científico**  
   Llevar ideas entre dominios distintos cuando comparten estructura matemática.

3. **Evidencia condicional**  
   Cada técnica tiene cuándo funciona, cuándo falla, costo y riesgo.

4. **Validación como primera clase**  
   El sistema prioriza diseño experimental creíble antes que modelos fancy.

5. **Memoria de fracasos**  
   Registrar lo que no funcionó y por qué.

6. **Planificación bajo presupuesto competitivo**  
   Responder “qué hago primero” con tiempo y cómputo limitados.

7. **Narrativa extractable de write-ups**  
   Capturar insights humanos que no están en el código.

8. **Ciclo cerrado de aprendizaje**  
   Cada competencia mejora el sistema.

---

# 18. MVP recomendado

El MVP no debe ser un scraper masivo.

Debe ser un **piloto de razonamiento con knowledge base curada**.

## Alcance inicial del MVP

Vertical:

> Competencias tabulares de clasificación y regresión en Kaggle/DrivenData.

Por qué tabular:

- más fácil de diagnosticar;
- validación, leakage y drift son críticos;
- baselines tree-based son fuertes;
- hay muchos write-ups públicos;
- permite demostrar valor rápido;
- no requiere GPU masiva.

Artefactos iniciales:

- 30 soluciones públicas;
- 30 write-ups;
- 30 papers o métodos relevantes;
- 20 repositorios;
- 10 modelos o baselines reproducibles;
- 10 fracasos documentados.

Funcionalidad MVP:

1. Input manual o semiautomático de una competencia.
2. Generación de Problem DNA.
3. Recuperación de técnicas candidatas desde KB.
4. Recomendaciones con condiciones y riesgos.
5. Plan experimental para primeras 48 horas.
6. Plantilla de post-mortem.
7. Registro de experiments y failures.

Output MVP:

Un informe tipo:

```text
Problem DNA
Riesgos principales
Validación recomendada
Anti-validaciones
Baselines sugeridos
Técnicas candidatas
Técnicas de baja prioridad
Plan experimental fase 1-6
Señales de alarma
Recursos necesarios
Licencias y restricciones
```

---

# 19. Plan de proyecto detallado

Voy a proponer un plan de 12 semanas para MVP validado, más roadmap posterior.

---

## Fase 0 — Semana 1: Calibración con dolor real

### Objetivo

Aterrizar la idea en un caso real y responder la pregunta crítica:

> ¿Cuál fue la última competencia donde perdiste y entendiste exactamente por qué?

### Tasks

1. Seleccionar 3 competencias pasadas:
   - una perdida;
   - una mediocre;
   - una ganada pero mal entendida.

2. Completar post-mortem estructurado para cada una.

3. Identificar:
   - supuesto falso;
   - error de validación;
   - leak no detectado;
   - drift ignorado;
   - técnica innecesaria;
   - técnica faltante;
   - decisión que habría cambiado el resultado.

4. Extraer 10-20 reglas condicionales iniciales.

5. Definir Problem DNA v0.

6. Definir criterios de éxito del proyecto.

### Deliverables

- 3 post-mortems completos.
- 10-20 reglas condicionales.
- Problem DNA v0.
- Project charter.
- Lista de 30 artefactos públicos iniciales.

### Acceptance criteria

- Al menos una regla debe ser claramente accionable.
- Al menos un post-mortem debe identificar un error de validación, leak o drift que explicite por qué se perdió o underperforme.
- El equipo debe poder responder: “esto no es solo un catálogo; es un sistema que habría evitado X error”.

### Exit gate

Si no se puede completar esto, no avanzar a automatización. Primero se arregla la comprensión del problema.

---

## Fase 1 — Semanas 2-4: Knowledge Base curada + reasoning manual

### Objetivo

Construir una base pequeña pero de alta calidad y demostrar que el razonamiento condicional funciona.

### Tasks

1. Diseñar esquema de datos v1.

2. Crear base Postgres + pgvector o equivalente.

3. Cargar manualmente:
   - 30 artifacts;
   - 20 competitions;
   - 50 claims;
   - 20 failures;
   - 15 mechanisms;
   - 10 problem profiles.

4. Definir ontología inicial:
   - task;
   - modality;
   - metric family;
   - mechanism;
   - constraint;
   - risk;
   - evidence level.

5. Construir plantilla de informe de competencia.

6. Hacer 3 análisis manuales/asistidos por LLM de competencias pasadas.

7. Comparar recomendaciones del sistema con lo que realmente ocurrió.

8. Ajustar schema y reglas.

### Deliverables

- KB v1.
- 50 claims estructurados.
- 20 failure records.
- 3 reports de análisis retroactivo.
- Plantilla de Problem DNA.
- Plantilla de Experiment Plan.

### Acceptance criteria

- 80% de claims tienen fuente, licencia y condición de aplicabilidad.
- 70% de recomendaciones incluyen riesgo o modo de ruptura.
- En al menos 2 de 3 casos retroactivos, el sistema identifica una decisión crítica que el participante original ignoró o hizo tarde.
- El informe generado es legible y accionable en menos de 30 minutos de lectura.

### Exit gate

Si las recomendaciones son genéricas, no escalar a extracción automática todavía. Primero mejorar ontología y reasoning.

---

## Fase 2 — Semanas 5-7: Extracción semiautomática

### Objetivo

Reducir trabajo manual sin perder calidad.

### Tasks

1. Pipeline de ingesta:
   - descarga/control de notebooks públicos permitidos;
   - almacenamiento raw en object storage o Drive como drop;
   - registro de metadatos y licencia.

2. Parser de notebooks:
   - nbformat;
   - extracción de celdas;
   - AST;
   - detección de imports, funciones, hiperparámetros, seeds, métricas.

3. Extractor LLM para write-ups:
   - prompts con JSON schema;
   - obligación de citar fragmento;
   - clasificación de insight type;
   - detección de leak, drift, trick, validación, postprocessing.

4. Extractor para papers:
   - método;
   - supuestos;
   - ablations;
   - limitaciones;
   - enlaces a código.

5. Sistema de revisión humana:
   - UI simple o notebook;
   - aprobar/rechazar claims;
   - corregir condiciones;
   - asignar evidencia level.

6. Índice vectorial:
   - embeddings de claims, problemas, métodos;
   - búsqueda por filtro + semántica.

7. Quality checks:
   - duplicados;
   - licencias unknown;
   - claims sin fuente;
   - contradicciones;
   - extracciones alucinadas.

### Deliverables

- Pipeline de ingesta v1.
- 100+ artifacts procesados.
- 150+ claims candidatos.
- Dashboard/review queue.
- Índice vectorial inicial.
- Reporte de precisión de extracción en muestra gold.

### Acceptance criteria

- Reducir tiempo manual de curación en ≥50% versus Fase 1.
- ≥80% de claims extraídos pasan revisión humana con correcciones menores.
- 0 artefactos con licencia forbidden usados automáticamente.
- Cada claim tiene al menos una evidencia citada o referencia a paper/repo.

### Exit gate

Si la extracción genera mucho ruido, no ampliar volumen. Mejorar prompts, schemas y revisión.

---

## Fase 3 — Semanas 8-10: Reasoning Engine + Experiment Planner

### Objetivo

Convertir KB en sistema de decisión.

### Tasks

1. Implementar Problem Profiler:
   - input: descripción, datos, métrica, reglas;
   - output: Problem DNA estructurado.

2. Implementar recuperación híbrida:
   - filtros metadatos;
   - embeddings;
   - reglas ontológicas;
   - restricciones de licencia/compute.

3. Implementar scoring de candidatos:
   - MechanismFit;
   - EvidenceStrength;
   - ExpectedLift;
   - ConstraintCompatibility;
   - Cost;
   - Risk;
   - Uncertainty.

4. Implementar explicaciones:
   - por qué se recomienda;
   - por qué se descarta;
   - condiciones de ruptura;
   - evidencia asociada;
   - próximo experimento barato.

5. Implementar Experiment Planner:
   - fases;
   - hipótesis;
   - criterios de parada;
   - recursos;
   - riesgos.

6. Construir CLI o web simple:
   - `analyze_competition`;
   - `recommend_techniques`;
   - `generate_experiment_plan`;
   - `register_outcome`.

7. Blind test:
   - tomar 5 competencias pasadas;
   - ocultar soluciones;
   - generar plan;
   - comparar con resultados reales.

### Deliverables

- Reasoning Engine v1.
- Experiment Planner v1.
- Interfaz mínima.
- Informe de blind test.
- Reglas de scoring iniciales calibradas.

### Acceptance criteria

- En ≥3 de 5 casos retroactivos, el plan incluye al menos una técnica o validación que fue decisiva o habría evitado un error conocido.
- El sistema no recomienda técnicas prohibidas por licencia/reglas.
- Cada top-10 recomendación incluye condición y riesgo.
- Tiempo de generación de informe: <10 minutos automatizado + revisión humana.

### Exit gate

Si el sistema solo devuelve “usa LightGBM/transformer/ensemble”, no es suficiente. Hay que profundizar restricciones y mecanismos.

---

## Fase 4 — Semanas 11-12: Piloto en competencia real o simulada

### Objetivo

Validar valor competitivo en condiciones reales.

### Tasks

1. Elegir una competencia activa o un benchmark interno realista.

2. Usar CMRE desde el día 1:
   - Problem DNA;
   - plan experimental;
   - registro de experiments;
   - alertas de riesgo.

3. Ejecutar al menos:
   - 1 validación creíble;
   - 2 baselines fuertes;
   - 5 experimentos condicionales;
   - 1 análisis de leak/drift;
   - 1 estrategia de ensemble/postprocessing.

4. Comparar contra proceso habitual sin sistema.

5. Hacer post-mortem final.

6. Actualizar KB con resultados propios.

7. Medir KPIs.

### Deliverables

- Pilot report.
- Experiment log.
- Post-mortem.
- KB actualizada con evidencia propia.
- Go/no-go para escala.

### Acceptance criteria

El piloto se considera exitoso si cumple al menos dos de estos:

1. Detecta un riesgo de validación/leak/drift que habría costado puntos.
2. Reduce tiempo hasta primer baseline válido en ≥30%.
3. Genera al menos una hipótesis experimental que produce mejora medible.
4. Mejora consistencia público/privado respecto a intento anterior comparable.
5. Produce un post-mortem más preciso que los habituales.

### Exit gate

Si no cumple ninguno, revisar si el problema es:
- KB insuficiente;
- reasoning demasiado genérico;
- ejecución pobre;
- caso mal elegido;
- expectativas irreales.

No escalar todavía.

---

# 20. Roadmap posterior al MVP

## Mes 4-5: Expandir vertical

Añadir:

- time series;
- NLP básico;
- computer vision small-data.

Mejorar:

- graph database opcional;
- mejor scoring;
- más evidence levels;
- detección de contradicciones;
- recencia y obsolescencia de técnicas.

## Mes 5-6: Execution Lab más serio

Implementar:

- containers reproducibles;
- MLflow/W&B integrado;
- run templates;
- automatic experiment summaries;
- artifact registry;
- benchmark interno.

## Mes 6+: Multiusuario y equipo

Añadir:

- roles;
- shared knowledge base;
- review workflow;
- competition workspace;
- leaderboard risk dashboard;
- API para notebooks;
- integración con Kaggle API donde esté permitido.

---

# 21. Métricas del proyecto

No medir solo “cuántos notebooks guardamos”.

## Métricas de conocimiento

- % claims con fuente verificable.
- % claims con licencia clara.
- % claims con condición de aplicabilidad.
- % claims con condición de ruptura.
- % failures registrados vs successes.
- reproducibility score promedio.
- evidence level distribution.

## Métricas de recuperación

- Precision@10.
- Recall de técnicas críticas en gold set.
- NDCG.
- % recomendaciones adoptadas por humano.
- % recomendaciones descartadas por irrelevancia.

## Métricas de razonamiento

- % informes que identifican riesgo principal correctamente.
- % informes que proponen validación adecuada.
- % informes que evitan anti-patrones conocidos.
- calidad explicativa evaluada por rubrica humana.

## Métricas de ejecución

- tiempo hasta primer baseline.
- tiempo hasta primera hipótesis válida.
- número de experimentos por hora productiva.
- costo promedio por experimento.
- estabilidad por seed.
- gap público/privado.

## Métricas de impacto competitivo

- medals per competition.
- top 10% rate.
- improvement vs baseline personal.
- consistency between public/private.
- number of avoided disqualifications/license issues.
- post-mortem accuracy.

---

# 22. Rubrica de calidad para un informe CMRE

Un informe bueno debe responder:

1. ¿Cuál es la restricción dominante del problema?
2. ¿Qué validación replica mejor el test?
3. ¿Qué riesgos de leak/drift/overfitting existen?
4. ¿Qué baseline fuerte conviene correr primero?
5. ¿Qué mecanismos científicos son relevantes?
6. ¿Qué técnicas están sobrevaloradas para este caso?
7. ¿Qué experimento de bajo costo puede invalidar una hipótesis?
8. ¿Qué señal early warning indica que vamos mal?
9. ¿Qué postprocessing o alineación con métrica puede dar ganancia barata?
10. ¿Qué evidencia respalda cada recomendación?

Si el informe no responde esto, es demasiado genérico.

---

# 23. Anti-patrones que el sistema debe detectar

CMRE debe tener una librería de anti-patrones.

Ejemplos:

## Anti-patrón 1: KFold aleatorio en datos temporales

Síntoma:

- buen público, mal privado;
- features con timestamp;
- test futuro.

Regla:

> Si hay timestamp y el test parece futuro, usar temporal/rolling validation antes que random CV.

Ruptura:

- si la organización confirma IID;
- si timestamp es ruido sin relación con target.

---

## Anti-patrón 2: Optimizar arquitectura antes que validación

Síntoma:

- muchos modelos;
- poca confianza en CV;
- mejoras no sostenidas.

Regla:

> Primero validación creíble, luego modelo.

---

## Anti-patrón 3: Copiar trick de notebook ganador sin contexto

Síntoma:

- trick funciona en un dataset pero no en otro;
- no hay ablation;
- dependencia de seed o versión.

Regla:

> Ninguna técnica se adopta sin condición de aplicabilidad y experimento local.

---

## Anti-patrón 4: Ensemble ciego

Síntoma:

- muchos modelos correlacionados;
- ganancia marginal;
- riesgo de overfitting a público.

Regla:

> Ensemble solo con diversidad medida y validación estable.

---

## Anti-patrón 5: Ignorar la métrica real

Síntoma:

- optimizar accuracy cuando importa PR-AUC;
- optimizar RMSE cuando importa WMAPE;
- no calibrar cuando la métrica lo exige.

Regla:

> Traducir métrica a objetivo de entrenamiento/postprocessing.

---

## Anti-patrón 6: Usar datos externos sin verificar reglas

Riesgo:

- descalificación.

Regla:

> License/rule status bloqueante antes de recomendación automática.

---

# 24. Ejemplo end-to-end: competencia de fraude tabular

## Input

- clasificación binaria;
- transacciones con timestamp;
- métrica AUC;
- train meses anteriores;
- test período futuro;
- compute moderado;
- datos externos permitidos;
- submission limitada.

## Problem DNA generado

```text
task: binary_classification
modality: tabular
metric_family: ranking
has_temporal_component: true
test_is_future: likely
class_imbalance: extreme
leak_risk: temporal, id, target
distribution_shift_risk: high
compute_constraint: moderate
external_data_allowed: true
pretrained_models_allowed: not_relevant
```

## Diagnóstico

El problema no es primero “qué modelo”. Es:

- validación temporal;
- leak por IDs/timestamps;
- drift de comportamiento;
- métrica de ranking;
- estabilidad en segmentos temporales.

## Validación recomendada

- TimeSeriesSplit;
- rolling origin;
- adversarial validation train/test;
- group por usuario si existe;
- evaluación por mes/semana;
- seed fixing;
- no usar random Stratified KFold como primaria.

## Baselines

- LightGBM con features básicas;
- CatBoost con categoricales;
- logistic regression regularizada como sanity check;
- dummy/history baseline.

## Técnicas candidatas

- sample weighting;
- monotonic constraints si hay dominio;
- feature stability selection;
- target encoding regularizado;
- threshold no crítico porque AUC premia ranking;
- ensemble simple entre tree models;
- evitar deep nets complejas sin necesidad.

## Anti-patrones

- random KFold;
- usar IDs como features sin tratamiento;
- features que miren futuro;
- overfitting al leaderboard público;
- modelo grande sin baseline temporal sólido.

## Plan experimental

```text
1. Construir validación temporal.
2. Correr adversarial validation.
3. Baseline LightGBM + CatBoost.
4. Error analysis por mes y segmento.
5. Feature stability filter.
6. Sample weighting.
7. Ensemble conservador.
8. Stress test con shift sintético.
9. Submission final con documentación de riesgo.
```

## Regla aprendida

> En datos transaccionales con test futuro, la validación temporal vale más que cualquier arquitectura exótica.

## Condición de ruptura

> Si la competencia declara explícitamente IID o el timestamp no tiene relación con target, random/group CV puede ser suficiente.

---

# 25. Stack tecnológico recomendado

## MVP

Lenguaje:

- Python.

Almacenamiento raw:

- Google Drive como drop manual opcional;
- S3/GCS/MinIO para artefactos.

Base de datos:

- PostgreSQL;
- pgvector para embeddings.

Índice vectorial alternativo:

- Qdrant, LanceDB, Chroma.

Notebooks/experimentos:

- Jupyter;
- MLflow o Weights & Biases.

Versionado:

- Git;
- DVC para datos/modelos.

Extracción:

- nbformat;
- ast;
- Pydantic para schemas;
- LLM API o modelo local;
- Semantic Scholar/arXiv/Hugging Face APIs.

Interfaz:

- Streamlit o FastAPI + frontend simple.

Orquestación ligera:

- Prefect o Airflow más adelante.

Contenedores:

- Docker.

## Producción temprana

Añadir:

- Neo4j o graph layer si el grafo de evidencia se vuelve complejo;
- Airflow/Prefect;
- Kubernetes o VMs GPU;
- feature store opcional;
- model registry;
- CI/CD;
- observability;
- review UI para curadores.

---

# 26. Gobernanza legal, ética y de plataformas

Esto es crítico y no puede ser opcional.

## Reglas

1. Respetar Terms of Service de cada plataforma.
2. No scrapear agresivamente si está prohibido.
3. Usar APIs oficiales cuando existan.
4. No usar notebooks privados, filtrados o obtenidos indebidamente.
5. Respetar licencias de código: MIT, Apache, GPL, etc.
6. Respetar licencias de datasets.
7. Respetar licencias de modelos en Hugging Face.
8. Atribuir siempre fuentes.
9. No redistribuir pesos o datos restringidos.
10. Marcar todo artefacto con `license_status`.
11. Bloquear automáticamente uso de artefactos `unknown` o `forbidden`.
12. Separar conocimiento derivado de código original.
13. No incentivar cheating, leakage ilegal o violación de reglas.
14. Cuidar datos personales o sensibles, especialmente en medical/finance.
15. Documentar decisiones de uso justo/fair use cuando aplique.

## Campo obligatorio

```text
license_status: allowed | restricted | forbidden | unknown
```

Política:

- `allowed`: puede usarse automáticamente.
- `restricted`: solo con revisión humana y atribución.
- `unknown`: no se usa automáticamente.
- `forbidden`: solo referencia metadata, no contenido.

---

# 27. Gestión de riesgo del proyecto

## Riesgo 1: Convertirlo en un scraper gigante

Síntoma:

- mucho volumen, poca calidad;
- claims sin condiciones;
- informes genéricos.

Mitigación:

- empezar curado;
- gates de calidad;
- revisión humana;
- métricas de evidencia.

---

## Riesgo 2: Alucinaciones del LLM

Síntoma:

- técnicas inventadas;
- condiciones falsas;
- citas inexistentes.

Mitigación:

- JSON schema;
- citación obligatoria;
- retrieval grounding;
- human review;
- evidence levels;
- no auto-publish sin validación.

---

## Riesgo 3: Overfitting al pasado

Síntoma:

- recomendar tricks obsoletos;
- ignorar cambios de hardware/librerías/reglas.

Mitigación:

- recency weighting;
- expiry dates;
- revalidación periódica;
- contrastar con benchmarks actuales;
- marcar técnicas como “históricas” si pierden vigencia.

---

## Riesgo 4: Complejidad prematura

Síntoma:

- graph DB, microservicios, Kubernetes antes de tener 50 claims buenos.

Mitigación:

- MVP monolítico;
- Postgres + vectors;
- escalar solo cuando haya dolor real.

---

## Riesgo 5: No medir impacto competitivo

Síntoma:

- el sistema parece inteligente pero no ayuda a ganar.

Mitigación:

- pilotos reales;
- KPIs de decisión;
- post-mortems;
- go/no-go basados en valor, no en sofisticación.

---

## Riesgo 6: Problemas legales

Síntoma:

- usar código/datos/modelos sin permiso.

Mitigación:

- license_status obligatorio;
- provenance;
- revisión legal básica;
- no automatizar uso de artefactos dudosos.

---

# 28. Equipo mínimo necesario

Si lo hacen pocas personas, se pueden combinar roles.

## Rol 1: Competition Lead / Product Owner

Define:

- qué casos importan;
- qué significa éxito;
- prioriza features;
- valida informes.

## Rol 2: ML Research Engineer

Diseña:

- ontología de mecanismos;
- Problem DNA;
- scoring;
- planes experimentales;
- validación competitiva.

## Rol 3: Data/Platform Engineer

Construye:

- ingestion;
- parsers;
- DB;
- embeddings;
- pipeline;
- review tools;
- experiment tracking.

## Rol 4: Knowledge Curator / Analyst

Revisa:

- claims;
- write-ups;
- licencias;
- evidencia;
- fracasos;
- calidad semántica.

## Rol 5: Legal/Compliance advisor opcional

Revisa:

- ToS;
- licencias;
- uso de datos;
- modelos preentrenados;
- riesgos de plataforma.

---

# 29. Criterios go/no-go globales

El proyecto debe continuar solo si se cumplen varias de estas condiciones.

## Go

- Los post-mortems revelan patrones reutilizables claros.
- La KB condicionada mejora decisiones en casos retroactivos.
- El reasoning engine identifica riesgos de validación/leak/drift.
- El plan experimental reduce tiempo o errores.
- Hay al menos un piloto donde el sistema aporta valor tangible.
- La extracción automática mantiene calidad aceptable.
- No hay bloqueos legales graves.

## No-go o pivot

- El sistema solo devuelve recomendaciones genéricas.
- La mayoría de claims no tiene evidencia utilizable.
- Los LLM alucinan demasiado y no se puede controlar.
- No se logra mejorar decisiones en casos reales.
- El costo de curación supera el beneficio.
- Las licencias/ToS impiden operar de forma segura.
- El equipo se enamora de la infraestructura y no del resultado competitivo.

---

# 30. Versión final unificada del concepto

Esta es la redacción que podrías usar como pitch interno o externo:

> CMRE es un motor de razonamiento científico para competencias de machine learning. Parte de una idea inicial: extraer y clasificar código y write-ups ganadores de plataformas competitivas, vincularlos con papers, repositorios y modelos preentrenados. Sin embargo, su núcleo no es el catálogo, sino la capacidad de transformar ese conocimiento en evidencia condicional y decisiones accionables. El sistema descompone cada competencia en un Problem DNA: tarea, modalidad, métrica, restricciones matemáticas, riesgos de validación, leakage, drift, cómputo, licencias y estructura de datos. A partir de ahí, recupera mecanismos científicos relevantes —no solo técnicas superficiales—, evalúa sus condiciones de aplicación y ruptura, estima utilidad esperada bajo incertidumbre y genera un plan de experimentos priorizado por impacto, costo y riesgo. Cada resultado, positivo o negativo, alimenta una memoria acumulativa de éxitos y fracasos. La ventaja competitiva no está en tener más código ganador, sino en razonar mejor sobre problemas nuevos, transferir descubrimientos entre dominios similares o distintos, y decidir qué validar primero, qué probar, qué abandonar y por qué una solución funciona o se rompe.

---

# 31. Frase corta de posicionamiento

Puedes venderlo así:

> “Un motor que convierte soluciones ganadoras, papers y fracasos históricos en reglas de decisión transferibles para ganar nuevas competencias.”

O más técnico:

> “Reasoning engine + evidence graph + experiment planner para competitive ML.”

---

# 32. Primeras 10 acciones inmediatas

Si quieres arrancar mañana, haz esto:

1. Elegí la última competencia donde perdiste o entendiste tarde por qué.
2. Escribí un post-mortem usando la plantilla.
3. Identificá un supuesto falso.
4. Identificá una validación incorrecta o ausente.
5. Identificá una técnica que no era necesaria.
6. Identificá una técnica que faltaba.
7. Convertí eso en una regla condicional.
8. Definí el Problem DNA v0 con 10-15 campos.
9. Seleccioná 10 notebooks/write-ups públicos con licencia clara.
10. Extraé manualmente 20 claims condicionales antes de automatizar nada.

---

# 33. Conclusión final

Tu idea original tenía razón en algo importante: el conocimiento competitivo está disperso y puede sistematizarse. Pero la crítica que recibiste también tenía razón: el edge no está en acumular datos, sino en razonar mejor sobre restricciones, validación, evidencia y fracasos.

La unificación correcta es:

> Knowledge Base + Reasoning Engine + Feedback Loop.

La Knowledge Base sin reasoning es un archivo.  
El reasoning sin knowledge base es opinión.  
El feedback loop sin evidencia condicionada es ruido.

Cuando los tres se combinan, aparece algo verdaderamente diferencial:

> un sistema que no te dice simplemente qué técnica usar, sino por qué usarla, cuándo se rompe, qué experimento hacer primero y qué aprender después.

Ese es el proyecto que vale la pena construir.

--------------------------------------------------------------------------------------------------------------------------------------


