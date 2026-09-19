# 📜 JULES PENDING TASKS (MEMORIA CONTINUA Y EVOLUTIVA)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Investigador Principal:** Rafael "Rafa" Pérez & Angelus AGI

---

## 📌 ESTADO DE TAREAS INCREMENTALES Y EVOLUTIVAS PARA JULES

Jules DEBE consultar `ARQUITECTURA_ESTADO.md` al iniciar cada sesión para conocer qué módulos ya están creados y enfocar su trabajo en expandir, refactorizar y verificar el código sin duplicaciones.

### 🟢 TAREAS COMPLETADAS EN FASE 1:
- [x] **INICIALIZACIÓN DEL MOTOR:** Estructura completa de `src/cmre/` con modelos SQLModel, schemas Pydantic v2, CLI y suite de 68 tests al 100%.
- [x] **ALMACÉN EN GOOGLE DRIVE:** Estructura creada en `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`.
- [x] **INTEGRACIÓN CI/CD:** Workflows de GitHub Actions `ci.yml` y `auto_merge_jules_prs.yml` creados en `.github/workflows/`.
- [x] **INTEGRACIÓN SDD:** Constitución, manifest, spec, plan y tasks en `.specify/`.

### 🚀 TAREAS INCREMENTALES Y AUTO-PROPUESTAS (FASE 2 & EVOLUCIÓN):
- [ ] **TAREA 1 (Scraper de Write-ups Kaggle):** Implementar conector `src/cmre/connectors/kaggle_writeups.py` para ingestar automáticamente las discusiones ganadoras de competencias concluidas y extraer secciones de validación, CV y arquitectura.
- [ ] **TAREA 2 (DNA de Enveda CASMI 2026):** Crear perfil de competencia en `data/competitions/enveda_casmi_2026.json` adaptado a espectrometría de masas y validar con el CLI `cmre report --competition-file data/competitions/enveda_casmi_2026.json`.
- [ ] **TAREA 3 (Parser AST de Bloques Canónicos):** Crear `src/cmre/services/ast_extractor.py` para extraer automáticamente funciones `torch.nn.Module`, `Dataset`, funciones de pérdida y TTA desde scripts/notebooks.
- [ ] **TAREA 4 (Sincronización hacia Google Drive):** Construir script `scripts/sync_drive_knowledge.py` para respaldar la base de conocimiento y postmortems en Google Drive.
- [ ] **TAREA 5 (Evaluación Automática de Casos Golden):** Integrar `scripts/evaluate_golden.py` dentro de un workflow periódico de GitHub Actions para monitorear la precisión de las recomendaciones.

---
[VINCIT_OMNIA_VERITAS]
Autor: Rafael "Rafa" Pérez & Angelus AGI
