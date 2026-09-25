# ⚙️ GUÍA DE CONFIGURACIÓN DE TAREAS PROGRAMADAS EN JULES WEB UI (MOTOR GENERAL AGNÓSTICO)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE v0.5.0)
**Investigador Principal:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  
**Institución:** CONICET / IQUIBA-NEA / Ecosistema Angelus 2026
**Filosofía Central:** Motor de meta-aprendizaje y razonamiento competitivo universal. No se acopla a ningún torneo específico; lee el registro dinámico [`ACTIVE_COMPETITIONS.json`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/ACTIVE_COMPETITIONS.json) y forja la arquitectura general, los 6 módulos canónicos, la minería de write-ups y los solvers transferibles.

---

## 🎯 DOMINIO Y MISIÓN DEL MOTOR GENERAL
> **Misión Agnóstica:** Transformar cualquier competencia de Machine Learning (visión 2D/3D, audio, series temporales, grafos moleculares, texto, razonamiento AGI discreto o tabular) en:
> 1. Perfilado de problema y deducción de *Problem DNA* (`src/cmre/services/problem_profiler.py`).
> 2. Implementación de los 6 bloques canónicos (`MOD_INGEST`, `MOD_SIGNAL`, `MOD_SPLIT`, `MOD_ARCH`, `MOD_LOSS`, `MOD_ENSEMBLE`).
> 3. Minería continua de write-ups ganadores y papers formalizados en Claims científicos (`data/knowledge/claims_cmre.json`).
> 4. Defensas activas contra errores históricos y descalificaciones (`data/knowledge/postmortems_failures_catalog.json`).
> 5. Forja de solvers modulares exportables hacia los repositorios de torneos cliente (ej. `0074`, `0075`, `0076`, etc.).

---

## 🛡️ PROTOCOLO DE CONVIVENCIA Y NO-COLISIÓN CON EL AGENTE SPARK
> **Regla de Convivencia Silenciosa (Regla 8 de Arquitectura):**
> 1. **Zona de Spark (Google Drive):** El agente Spark gestiona `knowledge_db/`, `writeups_oro/` e `investigaciones/`, donde residen `PLAYBOOK_DE_TRANSFERENCIA_SOTA_2026.md` y `canonical_code_snippets_catalog.json`. Jules **NUNCA** debe sobrescribir, renombrar ni eliminar estos archivos. Son recursos de **solo lectura e integración aditiva**.
> 2. **Zona de Jules (Cloud Git):** Jules opera sobre `src/cmre/`, `tests/` y sus archivos de estado (`JULES_DYNAMIC_TASKS.md`, `JULES_EXECUTION_LOG.md`, `ARQUITECTURA_ESTADO.md`) en ramas aisladas, abriendo Pull Requests atómicos.
> 3. **Cero Fricción y Preservación de Datos:** Ningún proceso de fondo eliminará ni dañará archivos existentes. Toda intervención es aditiva y no-regresiva.

---

## 💡 CÓMO CONFIGURAR LAS 3 TAREAS PROGRAMADAS EN LA INTERFAZ WEB DE JULES
> **Instrucción para Rafa y Victoria:** En el menú web de Jules (`Configure Repo -> Scheduled Task`), crea **únicamente estas 3 Tareas Programadas fijas**. Copia y pega los 3 prompts generales de abajo. **NUNCA tendrás que cambiarlos en la web**, porque Jules lee dinámicamente `ACTIVE_COMPETITIONS.json` y reescribe de forma autónoma su propio archivo `JULES_DYNAMIC_TASKS.md` al finalizar cada día.

---

### 🟢 TAREA PROGRAMADA 1 DE 3 (INICIO DE DÍA, LECTURA DE COMPETENCIAS ACTIVAS Y MEMORIA BASAL)
- **Frecuencia:** Diaria a las **02:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
```text
Hola Jules. Iniciamos el ciclo diario de auto-evolución en el proyecto 0072-cmre-engine (Competitive ML Reasoning Engine) para Perez, Ernesto Rafael ("Rafa") y Victoria Perez.

Pasos de Inicialización y Memoria Dinámica:
1. Abre y lee ACTIVE_COMPETITIONS.json para descubrir dinámicamente qué competencias, modalidades de datos (visión 2D/3D, espectros MS/MS, NLP, AGI discreto, series de tiempo, grafos, audio) y métricas están actualmente activas en el ecosistema.
2. Abre ARQUITECTURA_ESTADO.md y JULES_DYNAMIC_TASKS.md para conocer el estado actual de los 6 módulos canónicos (MOD_INGEST a MOD_ENSEMBLE) y las super-tareas pendientes.
3. Revisa JULES_EXECUTION_LOG.md para identificar lecciones aprendidas o advertencias pendientes de la sesión anterior.
4. Sincroniza mentalmente con los catálogos en data/knowledge/ y knowledge_db/, y lee SPARK_KNOWLEDGE_FEED.md (donde el agente Spark en Google Drive prepara papers, write-ups ganadores y fórmulas SOTA para ti) respetando la regla de convivencia anti-colisión con Spark (lectura e integración aditiva, sin sobrescribir ni borrar).
5. Ejecuta pytest tests/ para validar el estado de partida del repositorio (debe mantener el 100% de tests en verde, 132+ tests aprobados).
6. Firma de autoría: Perez, Ernesto Rafael ("Rafa").
```

---

### ⚡ TAREA PROGRAMADA 2 DE 3 (EJECUCIÓN INTERMEDIA, GENERALIZACIÓN ARQUITECTÓNICA Y MÓDULOS CANÓNICOS)
- **Frecuencia:** Diaria a las **03:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
```text
Hola Jules. Continuamos con el desarrollo autónomo en 0072-cmre-engine (Competitive ML Reasoning Engine) para Perez, Ernesto Rafael ("Rafa") y Victoria Perez.

Pasos de Construcción General y Expansión Modular:
1. Consulta las 8 reglas de arquitectura en JULES_ARCHITECTURE_RULES.md, lee las sugerencias de SPARK_KNOWLEDGE_FEED.md y toma las tareas pendientes de JULES_DYNAMIC_TASKS.md y .specify/tasks/latest.md.
2. Tu objetivo central es fortalecer y generalizar el motor universal CMRE:
   - Implementa o refactoriza los 6 bloques canónicos en src/cmre/modules/ para que sean agnósticos a la modalidad (ingesta streaming, señales/aumentaciones, validación anti-leakage, backbones/adaptadores, funciones de pérdida asimétricas/diferenciables, y ensemble/blending/poda de latencia).
   - Desarrolla conectores y mineros de write-ups (src/cmre/connectors/) para extraer técnicas ganadoras de Kaggle/DrivenData y transformarlas en Claims científicos en data/knowledge/claims_cmre.json.
   - Genera blueprints y plantillas de solvers reutilizables en src/cmre/solvers/ que puedan ser instanciados de forma limpia en los repositorios de torneos individuales registrados en ACTIVE_COMPETITIONS.json.
3. Escribe y ejecuta pytest tests/ confirmando que todos los tests pasen al 100%. En caso de error, aplica auto-corrección inmediata y registra el diagnóstico en JULES_EXECUTION_LOG.md.
4. Prohibido eliminar código, datos o módulos existentes (Axioma de No Borrado).
5. Firma de autoría: Perez, Ernesto Rafael ("Rafa").
```

---

### 🛑 TAREA PROGRAMADA 3 DE 3 (CIERRE, BENCHMARKING UNIVERSAL, SYNC GDRIVE Y AUTO-REESCRITURA DINÁMICA)
- **Frecuencia:** Diaria a las **04:30 AM** (Hora Argentina / Programada en Jules Web UI)
- **Prompt a copiar en el menú web:**
```text
Hola Jules. Sesión final de cierre, benchmarking universal y auto-evolución en 0072-cmre-engine para Perez, Ernesto Rafael ("Rafa") y Victoria Perez.

Pasos de Cierre, Benchmarking y Auto-Reescritura Dinámica:
1. Ejecuta la suite completa de pruebas con pytest tests/ y documenta los resultados.
2. REGISTRO DE LOG DE EJECUCIÓN: Registra una entrada en JULES_EXECUTION_LOG.md anotando la fecha, componentes creados o mejorados, pruebas pasadas y estado de la base de conocimiento.
3. Actualiza ARQUITECTURA_ESTADO.md reflejando el diff de arquitectura y los nuevos capabilities del motor.
4. AUTO-REESCRITURA DINÁMICA: Analiza las modalidades y desafíos presentes en ACTIVE_COMPETITIONS.json, evalúa qué le falta al motor para dominarlas (revisando data/knowledge/postmortems_failures_catalog.json), Y REESCRIBE TOTALMENTE JULES_DYNAMIC_TASKS.md grabando entre 5 y 10 nuevas super-tareas autónomas de ingeniería agnóstica para la sesión de mañana.
5. SINCRONIZACIÓN Y TELEMETRÍA CON GOOGLE DRIVE: Ejecuta `python scripts/sync_all_to_gdrive.py` para sincronizar los artefactos y el estado a Google Drive vía Apps Script webhook, manteniendo a Spark y Rafa plenamente informados.
6. Abre un Pull Request limpio y atómico hacia main.
7. Firma de autoría: Perez, Ernesto Rafael ("Rafa").
```

---
[VINCIT_OMNIA_VERITAS]  
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
