# 🚀 PROMPTS MAESTROS INCREMENTALES Y AGRUPADOS PARA JULES
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI

---

## 💡 GUÍA DE DESPACHO AGRUPADO (AHORRO DE CUOTA Y TAREAS PROGRAMADAS)

> **Regla de Oro:** 
> - El **PROMPT 1** (Inicio/Lectura) y el **PROMPT 7** (Cierre/Metacognición) **NUNCA se agrupan**; se ejecutan solos al inicio y al final.
> - Los prompts intermedios (2, 3, 4, 5, 6) se agrupan en **Super-Bloques** para ejecutarse juntos en una sola Tarea Programada de Jules, ahorrando hasta un 60% de cuotas diarias.

---

## 📋 BLOQUES UNIFICADOS PARA COPIAR Y PEGAR EN JULES

### 🟢 BLOQUE 1 DE 4 (SESIÓN 1 - SOLO): Inicio, Lectura de Memoria y Cobertura Unit Test
> "Hola Jules. Iniciamos una nueva iteración de auto-evolución en `0072-cmre-engine` para **Perez, Ernesto Rafael**.
> 
> Instrucciones de Estado:
> 1. Abre y lee `ARQUITECTURA_ESTADO.md` y `JULES_PENDING_TASKS.md` para verificar el inventario de módulos canónicos en `src/cmre/modules/` y servicios en `src/cmre/services/`.
> 2. Ejecuta `pytest tests/` para validar el estado actual del repositorio (los 85 tests deben pasar al 100%). Si algún test falla o falta cobertura, soluciónalo de inmediato.
> 3. Asegura la firma invariable: `Autor: Perez, Ernesto Rafael ("Rafa")` en los docstrings.
> 4. Actualiza la lista de tareas completadas en `JULES_PENDING_TASKS.md` y abre un PR acotado."

---

### ⚡ BLOQUE 2 DE 4 (SESIÓN 2 - AGRUPADO: PROMPT 2 + PROMPT 3): Refactorización Core y Módulos Canónicos
> "Hola Jules. Seguimos avanzando guiados por **Perez, Ernesto Rafael**. En esta única sesión combinada ejecutaremos las siguientes tareas intermedias:
> 
> --- PARTE A (Refactorización y Expansión Incremental de Módulos) ---
> 1. Inspecciona los 6 módulos canónicos en `src/cmre/modules/` (`ingest.py`, `signal.py`, `split.py`, `loss.py`, `ensemble.py`, `hpc.py`). NO sobrescribas archivos completos si ya contienen lógica funcional.
> 2. Extiende sus métodos agregando manejo determinista de excepciones, validación de tipos (`Pydantic v2` / `typing`), y optimización sintáctica.
> 3. Implementa nuevos componentes de la backlog de `JULES_DYNAMIC_TASKS.md` (ej. Soft-F1 autograd, DICOM batch processor, purga de series temporales).
> 4. Escribe o expande los tests correspondientes en `tests/` garantizando que `pytest` pase al 100%.
> 
> --- PARTE B (Conectores de Base de Datos y Servidores MCP) ---
> 5. Inspecciona la base de datos en `src/cmre/db.py` y `src/cmre/services/seeder_claims.py`.
> 6. Verifica la integración con los 5 Servidores MCP (`Render`, `Google Stitch`, `Vercel v0`, `Supabase`, `Context7`) definidos en `AGENTS.md`.
> 7. Asegura que el fallback de SQLite standalone (`sqlite:///data/cmre.db`) opere sin bloqueos cuando PostgreSQL no esté disponible.
> 8. Firma invariable: `Autor: Perez, Ernesto Rafael ("Rafa")`."

---

### ⚡ BLOQUE 3 DE 4 (SESIÓN 3 - AGRUPADO: PROMPT 4 + PROMPT 5 + PROMPT 6): Integración, Benchmarking y Documentación
> "Hola Jules. Excelente avance técnico para **Perez, Ernesto Rafael**. Ejecutaremos el segundo Super-Bloque en esta sesión:
> 
> --- PARTE A (Integración y Diagnóstico de Rendimiento) ---
> 1. Realiza una prueba de integración cruzada entre los 6 módulos canónicos y el generador de planes de competencia (`src/cmre/services/planner.py`).
> 2. Mide tiempos de ejecución y uso de memoria en datasets de ejemplo (`data/examples/`), aplicando optimizaciones de código en cuellos de botella (bitsets AVX2, matrices vectorizadas NumPy).
> 3. Ejecuta `python smoke_test.py` y verifica la generación exitosa de todos los reportes de torneo en `reports/`.
> 
> --- PARTE B (Logging Estructurado y Explicabilidad Forense) ---
> 4. Implementa logging estructurado (JSON o estándar) en el CLI y en los servicios de razonamiento sin exponer datos sensibles.
> 5. Agrega captura limpia de errores con mensajes técnicos orientados al diagnóstico rápido.
> 
> --- PARTE C (Redacción Didáctica y Difusión Científica) ---
> 6. Crea o actualiza la documentación técnica en `docs/` o en los reportes de `reports/`.
> 7. Explica la arquitectura implementada, los patrones de diseño y los resultados de unit tests en `pytest` (100% verde).
> 8. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

### 🛑 BLOQUE 4 DE 4 (SESIÓN 4 - SOLO DE CIERRE): Auto-Observación Metacognitiva y Cierre
> "Hola Jules. Fase final de la iteración para **Perez, Ernesto Rafael**.
> 
> Instrucciones de Cierre Metacognitivo:
> 1. Ejecuta la suite completa de pruebas con `pytest` y confirma 100% de éxito (85+ tests en verde).
> 2. Actualiza `ARQUITECTURA_ESTADO.md` registrando la lista actualizada de archivos en el disco y las mejoras aplicadas hoy.
> 3. Identifica autónomamente de 5 a 10 deudas técnicas o refinamientos futuros y grábalos en `JULES_DYNAMIC_TASKS.md`.
> 4. Registra un log completo en `JULES_EXECUTION_LOG.md`.
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

## 🔍 PROMPTS INDIVIDUALES DETALLADOS (PARA INSPECCIÓN GRANULAR)

- **PROMPT 1:** Inspección de Estado, Lectura de Memoria y Cobertura Unit Test (85/85 tests).
- **PROMPT 2:** Refactorización y Expansión Incremental de los 6 Módulos Canónicos.
- **PROMPT 3:** Robustecimiento de Conectores de Datos (SQLite/PostgreSQL) y Servidores MCP.
- **PROMPT 4:** Integración de Módulos, Benchmarking y Smoke Testing.
- **PROMPT 5:** Explicabilidad, Trazabilidad Forense y Logging Estructurado.
- **PROMPT 6:** Redacción Didáctica y Difusión Científica de Soluciones de Machine Learning.
- **PROMPT 7:** Auto-Observación Metacognitiva, Diff en `ARQUITECTURA_ESTADO.md` y Cierre.

---
[VINCIT_OMNIA_VERITAS]
