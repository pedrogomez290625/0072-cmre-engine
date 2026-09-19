# 🧬 PROMPT ESPECIALIZADO: BIOINFORMÁTICA, ESPECTROMETRÍA DE MASAS & QUÍMICA COMPUTACIONAL (CASMI / KAGGLE)
### Para Google Deep Research / Gemini AI Premium / Perplexity Pro

---

<PROMPT_DEEP_RESEARCH_BIO>
Actúa como un **Bioinformático Computacional Senior, Quimioinformático y Kaggle Grandmaster especializado en Espectrometría de Masas (MS/MS), Genómica y Modelado Molecular**.

### 🎯 OBJETIVO DE LA INVESTIGACIÓN
Realizar una **investigación profunda y forense** sobre competencias de Machine Learning y desafíos científicos de benchmark internacional enfocados en:
1. **Identificación Molecular y Espectrometría de Masas (MS/MS & LC-MS):**
   - CASMI (Critical Assessment of Small Molecule Identification) —todas sus ediciones recientes, incluyendo el benchmark Enveda CASMI 2026.
   - Predicción de espectros de fragmentación y búsqueda en librerías espectrales (GNPS, NIST, MassBank).
2. **Plegamiento y Modelado de Ácido Ribonucleico (RNA):**
   - Stanford Ribonanza RNA Folding (Kaggle).
   - Stanford RNA 3D Folding.
3. **Quimioinformática, Afinidad de Unión y Propiedades Moleculares:**
   - Predicting Molecular Properties (CHAMPS / Kaggle).
   - Open Catalyst Project (OCP) & NeurIPS Molecular Challenges.
   - CAFA (Critical Assessment of Function Annotation) 1 a 5.

---

### 🔬 PREGUNTAS Y FOCOS ESPECÍFICOS DE INGENIERÍA

Para cada una de estas áreas y competencias:
1. **Representación del Dato (Input Engineering):**
   - ¿Cómo representan los ganadores los espectros de masas MS2? (¿Histogramas de m/z binned, tensores de intensidad normalizada, matrices de pérdidas neutras (*neutral loss spectra*), grafos moleculares o transformers de picos?).
   - ¿Qué embeddings químicos dominan? (Morgan Fingerprints, RDKit 2D descriptors, Mol2Vec, ChemBERTa, Uni-Mol, SchNet, DimeNet++, Graphormer).
2. **Esquema de Validación Cruzada (CV):**
   - ¿Cómo evitaron la fuga de datos por similitud de scaffolds o familias químicas? (¿Bemis-Murcko Scaffold Split, partición por clusters Tanimoto, o partición por instrumento/laboratorio?).
3. **Métricas de Evaluación y Funciones de Pérdida:**
   - ¿Cómo optimizaron métricas como Cosine Similarity de espectros, Top-k Retrieval Accuracy, o RMSD?
   - ¿Qué trucos de pérdida personalizada (*custom loss*) superaron al error cuadrático o entropía cruzada?
4. **Post-procesamiento y Fusión Espectral:**
   - Técnicas de matching con fórmulas brutas candidatas, reglas de valencia, filtrado de adductos ([M+H]+, [M-H]-, etc.) y re-ranking de base de datos.
5. **Papers, Repositorios y Checkpoints:**
   - Indicar el paper formal en arXiv/Nature/Bioinformatics, el repositorio limpio en GitHub (ej. Matchms, Spec2Vec, MS-Novelist, CFM-ID, Sirius/CSI:FingerID, GNPS tools) y los modelos preentrenados en Hugging Face.

### 📦 ENTREGABLE
Un informe técnico exhaustivo con código Python/PyTorch de referencia, diagramas conceptuales de los pipelines ganadores y catálogo de errores que evitaron los mejores equipos.
</PROMPT_DEEP_RESEARCH_BIO>
