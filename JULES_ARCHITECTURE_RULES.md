# 🏛️ REGLAS PERMANENTES DE ARQUITECTURA Y AUDITORÍA DE ERRORES
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Rafael "Rafa" Pérez & Angelus AGI

---

## 📌 1. DOMINIO TÉCNICO Y MÓDULOS BASE
- **Misión de Proyecto:** Motor de razonamiento científico para competencias de Machine Learning que transforma write-ups, papers, repositorios y modelos en decisiones de ingeniería y planes experimentales de alto rendimiento.
- **Módulos Core Protegidos:**
  `src/cmre/models.py`, `schemas.py`, `services/problem_profiler.py`, `services/scoring.py`, `services/recency.py`, `services/planner.py`, `services/reasoner.py`.

---

## 🛡️ 2. DIRECTIVAS ARQUITECTÓNICAS Y TOLERANCIA A ERRORES
Jules debe aplicar estas 7 reglas en cada sesión:

1. **REGLA 1 (Conservación de Estado):** Nunca sobrescribir código funcional existente. Leer `ARQUITECTURA_ESTADO.md` antes de editar.
2. **REGLA 2 (Recuperación de Errores & Logging):** Si una sesión encuentra un fallo sintáctico, error de red o test roto, Jules NO se detiene en pánico. Registra la traza del error en `JULES_EXECUTION_LOG.md`, aplica una solución temporal o fallback y documenta la remediación.
3. **REGLA 3 (Calidad & Tipado):** Aplicar manejo determinista de excepciones, tipado estricto (`typing` / `Pydantic v2` / `SQLModel`) en todos los modelos y servicios.
4. **REGLA 4 (Conectividad Segura & Fallbacks):** Garantizar resiliencia y fallback en llamadas a APIs externas (arXiv, GitHub, Hugging Face, Semantic Scholar). Si la API no responde, usar el pseudo-embedding o mock determinista sin romper el pipeline.
5. **REGLA 5 (Cobertura de Tests al 100%):** Mantener `pytest` al 100% de pasaje sin advertencias destructivas.
6. **REGLA 6 (Almacenamiento Desacoplado):** Los archivos grandes, volcados de bases y datasets residen en Google Drive (`G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`).
7. **REGLA 7 (Canal de Comunicación con Angelus & Rafa):** Si Jules requiere credenciales adicionales, GPUs de mayor potencia (A100/TPU en Google Colab Pro) o guía estratégica superior, debe redactar su petición en `MENSAJES_PARA_ANGELUS.md`. Jules no debe esperar bloqueado; continúa trabajando con fallbacks seguros.

---
[VINCIT_OMNIA_VERITAS]
