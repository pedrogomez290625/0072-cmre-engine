# 🏛️ ARQUITECTURA Y ESTADO VIGENTE DEL REPOSITORIO
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Versión:** 0.3.0
**Estado:** STAGE_4_DOMAIN_ENRICHED 🟢 (100% Tests Pasando: 68/68)
**Última Auditoría:** 19 de Septiembre de 2026

---

## 📊 1. RESUMEN DE COBERTURA Y SALUD
- **Tests Unitarios:** 68/68 pasados (100% de éxito).
- **Herramienta de Construcción:** `pyproject.toml` (PEP 621) + `uv.lock`.
- **Smoke Test:** Verificado (35 claims, 6 reportes de torneo generados).
- **Almacén Google Drive:** Sincronizado en `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`.
- **GitHub:** [https://github.com/perezernestorafael933/0072-cmre-engine](https://github.com/perezernestorafael933/0072-cmre-engine).

---

## 📂 2. INVENTARIO DE MÓDULOS ACTIVOS
- **`src/cmre/models.py`:** Esquemas relacionales SQLModel con soporte para pgvector (`Mechanism`, `Technique`, `Claim`, `Failure`, `ProblemProfile`, `Experiment`).
- **`src/cmre/schemas.py`:** Modelos Pydantic v2 inmutables para tipado de entrada y salida (`CompetitionInput`, `ProblemDNA`, `RankedClaim`, `ExperimentPlan`).
- **`src/cmre/connectors/`:** Conectores a arXiv, GitHub, Hugging Face y Semantic Scholar.
- **`src/cmre/services/problem_profiler.py`:** Extractor de ADN de problemas competitivos.
- **`src/cmre/services/scoring.py` y `recency.py`:** Algoritmos de scoring multidimensional y decaimiento temporal.
- **`src/cmre/services/planner.py`:** Planificador en 6 fases.
- **`src/cmre/services/reporter.py`:** Generador de reportes en Markdown.
- **`src/cmre/cli.py`:** CLI interactivo con Typer y Rich.
