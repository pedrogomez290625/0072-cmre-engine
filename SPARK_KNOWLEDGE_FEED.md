# 🧠 SPARK KNOWLEDGE FEED - PUENTE DE MINERÍA CIENTÍFICA (SPARK ➔ JULES)
### Proyecto: `0072-cmre-engine` (CMRE v0.5.0)
**Autor:** Perez, Ernesto Rafael ("Rafa") & Angelus AGI  
**Emisor:** Agente Spark (Google Drive) | **Receptor:** Agente Jules (Google Cloud)  
**Fecha:** 25 de Septiembre de 2026  

---

## 📌 ESTADO DE ENLACE AGÉNTICO
* **Propósito:** Este archivo es el canal directo donde Spark deposita investigaciones, pseudocódigo matemático, fórmulas de pérdida y blueprints ganadores para que Jules los transforme en código fuente en `src/cmre/`.
* **Regla de Operación:** Spark edita y añade conocimiento en este documento. Jules lo lee en su Tarea 1 de inicio de jornada (02:30 AM ART) e implementa en Tarea 2 (03:30 AM ART).

---

## 🔬 INSUMOS ACTUALES DE MINERÍA CIENTÍFICA

### 1. Insumo para Modalidad `image_2.5d_mri` (Ej. RSNA Knee Detection):
- **Técnica:** Asymmetric Loss (ASL) con supresión de falsos positivos en clases con alta desproporción (meniscos, fracturas vs derrame articular).
- **Blueprint para Jules:** Implementar en `src/cmre/modules/loss.py` la clase `AsymmetricLossOptimized` con parámetros $\gamma_- = 4, \gamma_+ = 0, \text{clip} = 0.05$.
- **Alerta Anti-Leakage:** Mantener estricto agrupamiento por `StudyInstanceUID` en los folds de validación para evitar fugas entre cortes del mismo paciente.

### 2. Insumo para Modalidad `msms_peak_spectra` (Ej. Enveda CASMI 2026):
- **Técnica:** Gated Rank-1 Shielding con normalización dimensional $\sqrt{N_{\text{bits}}}$.
- **Blueprint para Jules:** Integrar en `src/cmre/solvers/enveda_casmi_solver.py` la calibración neural de producto punto para evitar que moléculas de gran tamaño monopolicen el Top-1 frente a fragmentaciones de alta resolución.
- **Alerta Anti-Shakeup:** En Kaggle Code Competitions, todo el cómputo debe ejecutarse en el runtime dinámico de inferencia; nunca depender de asserts de tamaño estático sobre el dataset visible.

### 3. Insumo para Modalidad `discrete_grid_2d` (Ej. ARC Prize 2026):
- **Técnica:** Síntesis Monotónica Dual (Simbólica inductiva verificado al 100% en pares de entrenamiento + adaptadores LoRA dinámicos en tiempo de prueba - TTT).
- **Blueprint para Jules:** Reforzar en `src/cmre/solvers/arc_agi_hybrid_solver.py` la suite de invariancias $D_8$ (8 rotaciones y reflexiones ortogonales) con guardián anti-identidad estricto.

---
*Vincit Omnia Veritas*  
Autor: Perez, Ernesto Rafael ("Rafa") & Angelus AGI
