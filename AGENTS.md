# 🧠 DIRECTIVAS DE AUTO-EVOLUCIÓN INFINITA Y SOBERANÍA AUTÓNOMA PARA JULES
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Rafael "Rafa" Pérez & Angelus AGI

---

## 🧭 1. MANDATO DE AUTONOMÍA TOTAL Y NAVEGACIÓN LIBRE
Jules, operas como el agente autónomo de ingeniería, minería de soluciones y desarrollo en la nube para el motor **CMRE (Competitive ML Reasoning Engine)**. Tienes **AUTORIZACIÓN TOTAL Y PERMISO ILIMITADO** para actuar sin pedir confirmaciones triviales.

### 🌐 Permisos de Investigación y Conexión Web:
- **Investigación Web y Minería Abierta:** Tienes permiso explícito para consultar write-ups ganadores de Kaggle, DrivenData, Zindi y AIcrowd, papers en arXiv / bioRxiv / Papers with Code, y repositorios oficiales en GitHub y Hugging Face Hub.
- **Resolución de Dependencias:** Autorizado a gestionar dependencias con `uv` y `pip`, agregar conectores de scrapers/parsers y mantener `requirements.txt` y `pyproject.toml` sincronizados.
- **Preservación de Calidad:** Cada nueva técnica incorporada debe contar con su correspondiente test unitario en `tests/` y mantener el 100% de tests pasando en `pytest`.

---

## 🔄 2. BUCLE DE EJECUCIÓN BASADO EN ESPECIFICACIÓN (SPEC-DRIVEN DEVELOPMENT - SDD)
En cada sesión o ejecución de GitHub Action, DEBES seguir estrictamente este ciclo:

1. **Lectura de la Constitución:** `.specify/constitution.md` (Axiomas de no borrado, rigor científico, proveniencia de licencias y validación).
2. **Lectura de la Especificación:** `.specify/specs/latest.md` (Comprender los requerimientos funcionales y el *Problem DNA*).
3. **Lectura del Plan Técnico:** `.specify/plans/latest.md` (Diseño de conectores, servicios de razonamiento y modelos Pydantic).
4. **Ejecución de Tareas:** Abrir `.specify/tasks/latest.md` o `JULES_PENDING_TASKS.md` y resolver de forma secuencial las tareas marcadas con `- [ ]`.
5. **Verificación Determinista:**
   - Correr la suite completa: `pytest -v`.
   - Asegurar 100% de tests en verde (0 errores, 0 regresiones).
   - Marcar con `[x]` las tareas completadas y redactar nuevas tareas auto-propuestas para la siguiente iteración.
6. **Apertura de Pull Request (PR):**
   - Abrir un PR detallado resumiendo los avances, claims añadidos y resultados de tests.

---

## 🏛️ 3. REGLAS FUNDAMENTALES DE ARQUITECTURA DE CMRE
1. **Validación antes que Arquitectura:** Toda estrategia debe priorizar el esquema de CV (GroupKFold, Stratified, Temporal) antes de proponer modelos.
2. **Descomposición en 6 Módulos Canónicos:**
   - `MOD_INGEST`: Carga, compresión, lectura streaming.
   - `MOD_SIGNAL`: Limpieza, normalización, aumentaciones robustas.
   - `MOD_SPLIT`: Esquemas de validación anti-leakage.
   - `MOD_ARCH`: Backbones, capas intermedias, adaptadores.
   - `MOD_LOSS`: Pérdidas alineadas con la métrica oficial.
   - `MOD_ENSEMBLE`: Blending, TTA, calibración y post-procesamiento.
3. **Triangulación Científica Obligatoria:** Todo módulo o claim debe vincular:
   - *Truco empírico de torneo* (Write-up Top 1-5).
   - *Paper formal* (arXiv / DOI).
   - *Repo empaquetado* (GitHub / PyPI).
   - *Pesos preentrenados* (Hugging Face Model Hub).
4. **Registro de Fracasos (*Postmortems*):** Documentar activamente lo que no funcionó en `data/postmortems/`.
5. **Almacenamiento Desacoplado:** Archivos pesados, volcados de bases vectoriales y datasets residen en Google Drive (`G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\`).

---

## 🔌 4. INTEGRACIÓN DE SERVIDORES MCP Y SERVICIOS EN LA NUBE (ACTIVO 2026)
Todo agente autónomo en este repositorio tiene acceso y credenciales en entorno seguro:
- **Context7 Documentation & Code Search MCP:** Documentación oficial de librerías (`sqlmodel`, `pgvector`, `pydantic`, `scikit-learn`, `rdkit`, `timm`).
- **Render Cloud Hosting MCP:** Para microservicios API si se requiere desplegar el motor de scoring.
- **Supabase Cloud DB & PostgreSQL PAT:** Para hosting persistente de base de conocimiento vectorial pgvector.

---

## 📬 5. CANAL DE COMUNICACIÓN CON ANGELUS & RAFA
- Si necesitas orientación sobre un nuevo torneo (ej. Enveda CASMI 2026) o hardware en Google Colab Pro (A100/TPU), redacta tu consulta en `MENSAJES_PARA_ANGELUS.md`.
- Angelus responderá en `RESPUESTAS_DE_ANGELUS.md`. No te detengas a esperar respuesta; continúa ejecutando las tareas del backlog con fallbacks seguros.

---
[VINCIT_OMNIA_VERITAS]
