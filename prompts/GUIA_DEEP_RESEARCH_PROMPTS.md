# 🗺️ GUÍA Y CATÁLOGO MAESTRO DE PROMPTS DE DEEP RESEARCH
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine (CMRE)
**Investigador Principal:** Rafael "Rafa" Pérez & Angelus AGI

---

Esta suite de prompts está diseñada para ser utilizada directamente en herramientas de **investigación profunda y navegación autónoma** (Google Deep Research en Gemini AI Premium, Perplexity Pro, OpenAI Deep Research o Claude Sonnet 3.5).

Su propósito es extraer la inteligencia acumulada de la comunidad de Kaggle y transferirla directamente al motor **CMRE** y a nuestro almacenamiento en Google Drive (`G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\writeups_oro\`).

---

## 🗂️ CATÁLOGO DE PROMPTS DISPONIBLES

| Archivo | Tipo de Investigación | Cuándo Usarlo |
| :--- | :--- | :--- |
| **[`PROMPT_DEEP_RESEARCH_KAGGLE_UNIVERSAL_CATEGORIAS.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_KAGGLE_UNIVERSAL_CATEGORIAS.md)** | **Ecosistema Completo de 8 Categorías** | Para mapear todas las categorías de Kaggle (Getting Started, Playground, Featured, Research, Community, Recruitment, Analytics) y entender qué receta funciona en cada una. |
| **[`PROMPT_DEEP_RESEARCH_PLAYGROUND_FAST_TRACK.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_PLAYGROUND_FAST_TRACK.md)** | **La Vía Rápida / Sparring Continuo** | Para competencias de Playground Series y Community (torneos quincenales/mensuales rápidos, datos sintéticos, ensamble de GBDTs y medallas ágiles). |
| **[`PROMPT_DEEP_RESEARCH_FEATURED_AND_RESEARCH.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_FEATURED_AND_RESEARCH.md)** | **Grandes Premios ($25k a $500k+) e Impacto** | Para competencias oficiales de 3 meses, gestión de equipo, prevención profunda de shakeup y modelado de frontera. |
| **[`PROMPT_DEEP_RESEARCH_BIOINFORMATICS_CHEMISTRY.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_BIOINFORMATICS_CHEMISTRY.md)** | **Bioinformática, Espectrometría & CASMI** | Diseñado a medida para la competencia activa **Enveda CASMI 2026** (espectrometría de masas, química molecular, fragmentación MS/MS y ARN). |
| **[`PROMPT_DEEP_RESEARCH_MEDICAL_VISION.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_MEDICAL_VISION.md)** | **Imágenes Médicas & Mamografía (RSNA)** | Para mamografía digital (MammoInsight), DICOMs masivos, pérdidas para desbalance severo y particiones por paciente. |
| **[`PROMPT_DEEP_RESEARCH_KAGGLE_MASTER.md`](file:///C:/Users/rafae/.gemini/01_PROYECTOS/0072-cmre-engine/prompts/PROMPT_DEEP_RESEARCH_KAGGLE_MASTER.md)** | **Atlas General Transversal** | Para un relevamiento amplio de las 5 modalidades técnicas principales (Tabular, Visión, Bio, NLP, Series Temporales). |

---

## 🚀 CÓMO OPERAR EN EL FLUJO DE TRABAJO

1. **Elegir el prompt:** Selecciona el prompt adecuado según el objetivo inmediato (ej. el de *Categorías Universal* para visión amplia, o el de *Bioinformática* para encarar CASMI 2026).
2. **Copiar y pegar en Deep Research:** Pega el texto en la caja de Deep Research de Gemini o Perplexity Pro y déjalo investigar durante 10-25 minutos.
3. **Guardar el informe generado:** 
   - Copia la respuesta completa y guárdala como archivo Markdown (`.md`) en:  
     `G:\Mi unidad\🏛️ Ecosistema_Angelus_2026\0072-cmre-engine\writeups_oro\`
4. **Ingesta en CMRE:** 
   - Nuestro motor CMRE procesará el archivo con el CLI (`cmre`) para indexar los claims y postmortems en la base de conocimiento vectorial, dejando todas esas ventajas listas para ser utilizadas automáticamente.
