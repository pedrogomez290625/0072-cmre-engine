# ⚙️ GUÍA DE CONFIGURACIÓN DE TAREAS PROGRAMADAS EN JULES WEB UI
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  
**Institución:** CONICET / IQUIBA-NEA / Ecosistema Angelus 2026

---

## 🎯 DOMINIO Y MISIÓN DEL PROYECTO
> **Área Objetivo:** Motor de razonamiento científico de élite para Machine Learning competitivo y salud digital. Transforma write-ups, papers y telemetría de competencias (Kaggle/RSNA/DrivenData) en planes de ejecución experimental óptimos, módulos de alto rendimiento a nivel de silicio (HPC, AVX2, Popcount bitsets), pipelines físicos DICOM mamográficos, funciones de pérdida asimétricas diferenciables y ensamblado no-negativo de modelos.  
> **Módulos Principales:** `src/cmre/modules/ingest.py`, `src/cmre/modules/signal.py`, `src/cmre/modules/split.py`, `src/cmre/modules/loss.py`, `src/cmre/modules/ensemble.py`, `src/cmre/modules/hpc.py`, `src/cmre/modules/registry.py`, `src/cmre/services/seeder_claims.py`, `src/cmre/services/planner.py`, `src/cmre/services/reasoner.py`.

---

## 🛡️ PROTOCOLO DE CONVIVENCIA Y NO-COLISIÓN CON EL AGENTE SPARK
> **Regla de Convivencia Silenciosa (Regla 8 de Arquitectura):**
> 1. **Zona de Spark (Google Drive):** El agente Spark gestiona `knowledge_db/`, `writeups_oro/` e `investigaciones/`, donde residen `PLAYBOOK_DE_TRANSFERENCIA_SOTA_2026.md` y `canonical_code_snippets_catalog.json`. Jules **NUNCA** debe sobrescribir, renombrar ni eliminar estos archivos. Son recursos de **solo lectura e integración aditiva**.
> 2. **Zona de Jules (Cloud Git):** Jules opera sobre `src/cmre/`, `tests/` y sus archivos de estado (`JULES_DYNAMIC_TASKS.md`, `JULES_EXECUTION_LOG.md`, `ARQUITECTURA_ESTADO.md`) en ramas aisladas, abriendo Pull Requests atómicos.
> 3. **Cero Fricción y Preservación de Datos:** Ningún proceso de fondo eliminará ni dañará archivos existentes. Toda intervención es aditiva y no-regresiva.

---

## 💡 CÓMO CONFIGURAR LAS 3 TAREAS PROGRAMADAS EN LA INTERFAZ WEB DE JULES
> **Instrucción para Rafa y Victoria:** En el menú web de Jules (`Configure Repo -> Scheduled Task`), crea **únicamente 3 Tareas Programadas fijas**. Copia y pega los siguientes 3 prompts adaptados a este repositorio. **NUNCA tendrás que cambiarlos en la web**, porque Jules reescribirá autónomamente su propio archivo `JULES_DYNAMIC_TASKS.md` en GitHub al concluir cada día.

---

### 🟢 TAREA PROGRAMADA 1 DE 3 (INICIO DE DÍA, LECTURA DE MEMORIA Y COBERTURA BASAL)
- **Frecuencia:** Diaria a las **02:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Iniciamos el ciclo diario de auto-evolución en el proyecto `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.
> 
> Pasos de Inicialización y Memoria:
> 1. Abre y lee `ARQUITECTURA_ESTADO.md` y `JULES_DYNAMIC_TASKS.md` para conocer el estado del código, módulos canónicos e inventario.
> 2. Revisa `JULES_EXECUTION_LOG.md`. Si la sesión anterior terminó con algún error o tarea incompleta, toma nota del fallo para corregirlo prioritariamente.
> 3. Sincroniza mentalmente con el nuevo `PLAYBOOK_DE_TRANSFERENCIA_SOTA_2026.md` y `canonical_code_snippets_catalog.json` generados por el Agente Spark en `knowledge_db/`, respetando la Regla 8 de convivencia anti-colisión (solo lectura, cero pisadas ni borrados).
> 4. Ejecuta `pytest tests/` para validar el estado de partida del repositorio (debe mantener el 100% de tests en verde, 132+ tests aprobados, cubriendo solvers RSNA Knee, CASMI 2026 y ARC Prize).
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

### ⚡ TAREA PROGRAMADA 2 DE 3 (EJECUCIÓN INTERMEDIA & MÓDULOS CANÓNICOS)
- **Frecuencia:** Diaria a las **03:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Continuamos con el desarrollo autónomo en `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.
> 
> Pasos de Ejecución Intermedia:
> 1. Consulta las 8 reglas de arquitectura en `JULES_ARCHITECTURE_RULES.md` (con especial énfasis en la Regla 8 de no-pisada con Spark) y las super-tareas de `JULES_DYNAMIC_TASKS.md`.
> 2. Toma las tareas pendientes de la backlog e implementa/refactoriza los componentes de `src/cmre/modules/` (Soft-F1 autograd, DICOM batch multithreading, purga temporal o kernels HPC Tanimoto/DSU) integrando de forma aditiva los patrones del `canonical_code_snippets_catalog.json`.
> 3. NUNCA toques ni modifiques destructivamente los dossiers ni catálogos de Spark en `knowledge_db/`, `investigaciones/` o `writeups_oro/`.
> 4. Escribe y corre `pytest tests/` confirmando que todos los tests pasen al 100%. En caso de error, no te detengas; registra el diagnóstico en `JULES_EXECUTION_LOG.md` y aplica la recuperación quirúrgica.
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

### 🛑 TAREA PROGRAMADA 3 DE 3 (CIERRE, REGISTRO DE LOGS Y REESCRITURA AUTÓNOMA)
- **Frecuencia:** Diaria a las **04:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Sesión final de cierre y auto-evolución en `0072-cmre-engine` para **Perez, Ernesto Rafael ("Rafa")** y **Victoria Perez**.
> 
> Pasos de Cierre, Registro de Log y Reescritura Autónoma:
> 1. Ejecuta la suite completa de pruebas con `pytest tests/` y documenta el resultado de la sesión.
> 2. **REGISTRO DE LOG DE EJECUCIÓN:** Registra una entrada en `JULES_EXECUTION_LOG.md` anotando la fecha, tareas completadas, pruebas pasadas y cualquier advertencia detectada con su remediación.
> 3. Actualiza `ARQUITECTURA_ESTADO.md` registrando los módulos actualizados y el diff de arquitectura de hoy.
> 4. **AUTO-REESCRITURA DINÁMICA:** Evalúa los requerimientos futuros del motor CMRE respetando la división de trabajo con Spark, **Y REESCRIBE TOTALMENTE `JULES_DYNAMIC_TASKS.md` grabando entre 5 y 10 nuevas super-tareas autónomas para la sesión de mañana.**
> 5. Abre un Pull Request limpio y atómico hacia `main`.
> 6. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---
[VINCIT_OMNIA_VERITAS]
