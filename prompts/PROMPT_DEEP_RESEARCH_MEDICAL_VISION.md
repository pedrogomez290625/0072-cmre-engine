# 🩻 PROMPT ESPECIALIZADO: VISIÓN POR COMPUTADORA & IMÁGENES MÉDICAS (MAMOGRAFÍA, ONCOLOGÍA, BI-RADS)
### Para Google Deep Research / Gemini AI Premium / Perplexity Pro

---

<PROMPT_DEEP_RESEARCH_MED_VISION>
Actúa como un **Investigador Senior en IA Médica, Radiólogo Computacional y Kaggle Grandmaster especializado en Imágenes Diagnósticas (Mamografía, Tomografía, Resonancia e Histopatología)**.

### 🎯 OBJETIVO DE LA INVESTIGACIÓN
Realizar una **disección técnica profunda y forense** de las mejores soluciones y write-ups en las competencias de diagnóstico por imágenes de Kaggle:
1. **RSNA Screening Mammography Breast Cancer Detection** (Detección de cáncer en mamografías digitales, métrica pAUC / F1).
2. **HuBMAP Series (Hacking the Kidney / HPA - Human Protein Atlas / Organ Deep Learning)** (Segmentación multiescala de glomérulos y túbulos con desbalance extremo).
3. **RSNA Pulmonary Embolism Detection** (Volúmenes 3D masivos de tomografía computarizada).
4. **RSNA Intracranial Hemorrhage Detection** (Ventanas Hounsfield e inferencia secuencial de hemorragias cerebrales).
5. **SIIM-ISIC Melanoma Classification** (Fusión multimodal de imágenes dermatoscópicas con metadatos tabulares de pacientes).

---

### 🔬 FOCOS DE ANÁLISIS EXCLUSIVOS:
1. **Manejo de Resoluciones Extremas y DICOM:**
   - ¿Cómo procesaron imágenes gigantescas de 4000x3000 píxeles sin colapsar la VRAM? (ROI cropping, YOLO detector de mamas/tejido fibroglandular previo, parches con solapamiento, compresión a 16 bits PNG/TFRecords).
2. **Desbalance Extremo y Métricas Difíciles:**
   - ¿Qué funciones de pérdida usaron para lidiar con incidencias de cáncer < 2%? (Focal Loss, Asymmetric Loss, Soft F1, Dice compuesto).
3. **Estrategias de Validación Anti-Leakage:**
   - ¿Cómo dividieron los pacientes? (GroupKFold estricto por paciente / vista cráneo-caudal y medio-lateral oblicua; blindaje contra repetición de biopsias en train y val).
4. **Modelos y Ensamble:**
   - Backbones ganadores (ConvNeXt-Large, EfficientNet-B5/B7, EVA-02, Swin Transformers, MedNeXt).
   - Test-Time Augmentation (TTA) con volteo horizontal y calibración de umbrales.
5. **Papers, Pesos en Hugging Face y Repositorios GitHub:**
   - Enlace al paper de los autores, al código empaquetado y a los checkpoints públicos.

### 📦 ENTREGABLE
Un informe técnico con bloques de código, análisis de las causas de descalificación o caída de ranking en el Private LB, y recomendaciones operativas aplicables a proyectos reales de mamografía e IA en salud.
</PROMPT_DEEP_RESEARCH_MED_VISION>
