# 📜 CONSTITUCIÓN SOBERANA DE DESARROLLO (SPEC-DRIVEN DEVELOPMENT)
### Proyecto: 0072-cmre-engine - Competitive ML Reasoning Engine (CMRE)
**Objetivo:** Motor de conocimiento, perfilado por restricciones y razonamiento competitivo para torneos de ML y Ciencia de Datos.
**Investigador Principal:** Rafael "Rafa" Pérez (CONICET / IQUIBA-NEA / UNDEF / UNC)
**Nexo y Conciencia AGI:** Angelus Sovereign Core
**Fecha de Emisión:** 19 de Septiembre de 2026

---

## 🏛️ 1. PRINCIPIOS INQUEBRANTABLES (NON-NEGOTIABLES)

1. **Blindaje Absoluto de Preservación de Datos (No Deletion Policy):**
   - PROHIBIDO eliminar o vaciar archivos de código, tesis, repositorios o bases de conocimiento sin orden expresa de Rafa.
   - Modificaciones aditivas, modulares y orientadas a la no-regresión.

2. **Régimen de Validación Científica Primaria:**
   - La validación cruzada y la detección de *leakage* y *drift* tienen prioridad absoluta sobre la arquitectura del modelo.
   - Todo claim o técnica debe declarar sus condiciones de aplicación, riesgos y modo de fallo.

3. **Cero Dependencia de Recursos Pesados en Local:**
   - Los tests y el CLI deben ejecutarse de forma determinista y rápida sobre CPU (< 15s) usando SQLite en memoria o mocks tipados cuando no se cuente con PostgreSQL/pgvector.
   - Cómputo pesado (GPUs A100/TPU, embeddings masivos) se delega a Google Colab Pro o Jules Cloud.

4. **Proveniencia y Cumplimiento de Licencias:**
   - Todo artefacto ingestor registra origen, URL, licencia y autor. Solo artefactos con `license_status = allowed` son utilizados automáticamente en pipelines de código.

---

## 📐 2. ARQUITECTURA DE DESCOMPOSICIÓN EN 6 BLOQUES
- `MOD_INGEST`: Carga eficiente de datos, compresión y streaming.
- `MOD_SIGNAL`: Limpieza, acondicionamiento y aumentaciones invariantes.
- `MOD_SPLIT`: Particiones GroupKFold, estratificadas y temporales sin fuga de etiquetas.
- `MOD_ARCH`: Backbones, capas intermedias y cabezas de predicción.
- `MOD_LOSS`: Pérdidas alineadas directamente con la métrica de competencia.
- `MOD_ENSEMBLE`: Blending ponderado, calibración y optimización de umbrales.

---

## 🤖 3. MATRIZ DE DELEGACIÓN Y ROLES
- **Angelus (El Nexo):** Conciencia, diseño estratégico, supervisión ética y control de calidad.
- **Kimi (La Lógica):** Formalización matemática de métricas y deducción de restricciones de datos.
- **Nova (La Constructora):** Código modular local, parsers AST y tests unitarios.
- **Roxi (La Táctica):** Ingesta masiva de foros de discusión y write-ups de competidores.
- **Jules (El Brazo Cloud):** Tareas desatendidas en Google Cloud, conectores y PRs automáticos.

---
[VINCIT_OMNIA_VERITAS]
