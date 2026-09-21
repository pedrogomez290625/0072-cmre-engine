# ⚙️ GUÍA DE CONFIGURACIÓN DE TAREAS PROGRAMADAS EN JULES WEB UI
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  
**Institución:** CONICET / IQUIBA-NEA / Ecosistema Angelus 2026

---

## 🎯 DOMINIO Y MISIÓN DEL PROYECTO
> **Área Objetivo:** Motor de razonamiento científico de élite para Machine Learning competitivo y salud digital. Transforma write-ups, papers y telemetría de competencias (Kaggle/RSNA/DrivenData) en planes de ejecución experimental óptimos, módulos de alto rendimiento a nivel de silicio (HPC, AVX2, Popcount bitsets), pipelines físicos DICOM mamográficos, funciones de pérdida asimétricas diferenciables y ensamblado no-negativo de modelos.  
> **Módulos Principales:** `src/cmre/modules/ingest.py`, `src/cmre/modules/signal.py`, `src/cmre/modules/split.py`, `src/cmre/modules/loss.py`, `src/cmre/modules/ensemble.py`, `src/cmre/modules/hpc.py`, `src/cmre/modules/registry.py`, `src/cmre/services/seeder_claims.py`, `src/cmre/services/planner.py`, `src/cmre/services/reasoner.py`.

---

## 💡 CÓMO CONFIGURAR LAS 3 TAREAS PROGRAMADAS EN LA INTERFAZ WEB DE JULES
> **Instrucción para Rafa y Victoria:** En el menú web de Jules (`Configure Repo -> Scheduled Task`), crea **únicamente 3 Tareas Programadas fijas**. Copia y pega los siguientes 3 prompts adaptados a este repositorio. **NUNCA tendrás que cambiarlos en la web**, porque Jules reescribirá autónomamente su propio archivo `JULES_DYNAMIC_TASKS.md` en GitHub al concluir cada día.

---

### 🟢 TAREA PROGRAMADA 1 DE 3 (INICIO DE DÍA, LECTURA DE MEMORIA Y LOG DE EJECUCIÓN)
- **Frecuencia:** Diaria a las **02:30 AM** (Hora Argentina / Programada en Jules)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Iniciamos el ciclo diario de auto-evolución en el proyecto `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael**.
> 
> Pasos de Inicialización y Memoria:
> 1. Abre y lee `ARQUITECTURA_ESTADO.md` y `JULES_DYNAMIC_TASKS.md` para conocer el estado del código, módulos canónicos e inventario.
> 2. Revisa `JULES_EXECUTION_LOG.md`. Si la sesión anterior terminó con algún error o tarea incompleta, toma nota del fallo para corregirlo prioritariamente.
> 3. Si `JULES_DYNAMIC_TASKS.md` no existe o está vacío, créalo analizando los 6 módulos canónicos en disco (`src/cmre/modules/`).
> 4. Ejecuta `pytest tests/` para validar el estado de partida del repositorio (debe mantener el 100% de tests en verde).
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

### ⚡ TAREA PROGRAMADA 2 DE 3 (EJECUCIÓN INTERMEDIA & REGLAS DE DOMINIO)
- **Frecuencia:** Diaria a las **03:30 AM** (Hora Argentina / Programada en Jules)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Continuamos con el desarrollo autónomo en `0072-cmre-engine` (Competitive ML Reasoning Engine) para **Perez, Ernesto Rafael**.
> 
> Pasos de Ejecución Intermedia:
> 1. Consulta las 7 reglas de arquitectura en `JULES_ARCHITECTURE_RULES.md` y las tareas dinámicas en `JULES_DYNAMIC_TASKS.md`.
> 2. Ejecuta las tareas enfocadas en la misión principal del proyecto: Optimización de razonamiento ML, funciones de pérdida diferenciables, validación cruzada purgada, pipelines DICOM y kernels HPC.
> 3. Refactoriza e incrementa los módulos principales (`src/cmre/modules/` y `src/cmre/services/`) sin romper funcionalidades previas ni alterar firmas públicas, asegurando resiliencia en la base de datos (fallback SQLite/PostgreSQL) y en los Servidores MCP de `AGENTS.md`.
> 4. Corre `pytest tests/` y confirma pasaje al 100%. En caso de error, no te detengas; registra el diagnóstico parcial en `JULES_EXECUTION_LOG.md` y aplica la recuperación quirúrgica.
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---

### 🛑 TAREA PROGRAMADA 3 DE 3 (CIERRE, REGISTRO DE LOGS Y REESCRITURA AUTÓNOMA)
- **Frecuencia:** Diaria a las **04:30 AM** (Hora Argentina / Programada en Jules)
- **Prompt a copiar en el menú web:**
> "Hola Jules. Sesión final de cierre y auto-evolución en `0072-cmre-engine` para **Perez, Ernesto Rafael**.
> 
> Pasos de Cierre, Registro de Log y Reescritura Autónoma:
> 1. Ejecuta la suite completa de pruebas con `pytest tests/` y documenta el resultado de la sesión.
> 2. **REGISTRO DE LOG DE EJECUCIÓN:** Registra una entrada en `JULES_EXECUTION_LOG.md` anotando la fecha, tareas completadas, pruebas pasadas y cualquier fallo o advertencia detectada con su plan de remediación.
> 3. Actualiza `ARQUITECTURA_ESTADO.md` registrando la lista de módulos actualizados y el diff de arquitectura de hoy.
> 4. **AUTO-REESCRITURA DINÁMICA:** Evalúa los requerimientos futuros del motor CMRE (HPC, kernels GPU, validadores de torneos), **Y REESCRIBE TOTALMENTE `JULES_DYNAMIC_TASKS.md` grabando entre 5 y 10 nuevas super-tareas autónomas para la sesión de mañana.**
> 5. Firma de autoría: `Perez, Ernesto Rafael ("Rafa")`."

---
[VINCIT_OMNIA_VERITAS]
