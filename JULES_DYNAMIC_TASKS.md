# 📝 TABLERO DINÁMICO DE SUPER-TAREAS (AUTO-EVOLUCIÓN CMRE)
### Proyecto: `0072-cmre-engine` - Competitive ML Reasoning Engine
**Iteración:** Auto-Evolución y Proyección Diaria
**Autor:** Perez, Ernesto Rafael ("Rafa")

Este archivo ha sido reescrito totalmente de forma dinámica tras cruzar `ACTIVE_COMPETITIONS.json` con `data/knowledge/postmortems_failures_catalog.json`. El motor proyecta nuevas super-tareas agnósticas para abordar los desafíos pendientes en las modalidades activas para la sesión de mañana.

---

## 🚀 BACKLOG DE SUPER-TAREAS AGNÓSTICAS (PRÓXIMA SESIÓN)

### [ ] SUPER-TAREA CMRE-244: Auto-Evolution against FAIL_03 (SNIP_MED_WSI_HANNING_TILER)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_03)
- **Problema:** Modelos con Dice de 0.88 en parches aislados de 512x512 colapsaron a 0.74 al evaluar la imagen gigapíxel completa (Whole Slide Image de 50,000x50,000 px).
- **Causa Raíz:** Recombinación ingenua de mosaicos (tiling sin solapamiento o con promedio rectangular simple). Las convoluciones estándar pierden contexto espacial en las fronteras de los mosaicos, generando discontinuidades en forma de cuadrícula.
- **Implementación:** Corte con solapamiento del 25% y reconstrucción mediante ponderación separable con ventana 2D de Hanning.

### [ ] SUPER-TAREA CMRE-245: Auto-Evolution against FAIL_08 (SNIP_LOSS_SOFT_F1_WEIGHTED)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_08)
- **Problema:** Modelos complejos (EfficientNet-B5) alcanzaron 99% accuracy en train con Cross-Entropy, pero la validación se estancó en 87.5% por sobreajuste severo a etiquetas erróneas.
- **Causa Raíz:** El dataset contenía entre 15% y 20% de ruido en las etiquetas debido a diagnósticos de campo en hojas de yuca sin confirmación de laboratorio. Cross-Entropy penaliza exponencialmente las discrepancias, forzando a la red a memorizar el ruido.
- **Implementación:** Uso de Label Smoothing, Bi-Tempered Loss o Soft-F1 con gradientes amortiguados para mitigar la penalización de outliers.

### [ ] SUPER-TAREA CMRE-246: Auto-Evolution against FAIL_11 (SNIP_ARC_ANTI_IDENTITY_GUARD)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_11)
- **Problema:** Pipeline híbrido V2 de búsqueda simbólica + heurísticas colapsó a un score oficial de 0.00 en Kaggle tras 17 horas de corrida.
- **Causa Raíz:** Cuando el motor simbólico alcanzó su límite de profundidad y tiempo de CPU, el bloque de escape ejecutó fallback = test_input (copia idéntica de la grilla de entrada). En ARC-AGI, la grilla objetivo jamás es idéntica a la entrada; por tanto 0/240 intentos fueron correctos.
- **Implementación:** Guardián estricto anti-identidad que prohíbe la sumisión de grillas idénticas y conmuta a Test-Time Training (TTT) con aumentaciones D8 y transformaciones cromáticas/topológicas seguras.

### [ ] SUPER-TAREA CMRE-247: Auto-Evolution against FAIL_06 (SNIP_SIGNAL_BAYESIAN_OOF_TE)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_06)
- **Problema:** Target encoding directo sobre pares de tarjetas y direcciones (card1 + addr1) infló el CV a 0.985, colapsando a 0.880 en test temporal.
- **Causa Raíz:** Fuga de la variable objetivo hacia las medias de grupo sin validación cruzada interna (in-fold) ni regularización bayesiana m-estimate. En test, transacciones fraudulentas ocurrieron bajo nuevas identidades no vistas.
- **Implementación:** Codificación bayesiana OOF estricta con regularización m-estimate de Dirichlet y adición de ruido gaussiano.

### [ ] SUPER-TAREA CMRE-248: Auto-Evolution against FAIL_12 (SNIP_ENS_LATENCY_BUDGET_PRUNING)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_12)
- **Problema:** Pipeline multi-modelo con más de 30 sub-redes (DINO slot-attention, 5 folds A5, RadImageNet y 4 ramas CoAtNet) demoró más de 6.5 horas en el test set privado, rozando el timeout de 9 horas y arriesgando la pérdida de la sumisión.
- **Causa Raíz:** Sobre-ingeniería de ensamble sin presupuestación de latencia de inferencia. La concatenación ciega de modelos pesados sin podado greedy degrada la velocidad sin aportar ganancia marginal de AUC.
- **Implementación:** LatencyBudgetPruner podando el ensamble a una tríada quirúrgica (KneeSpecialistMONAI512 + CoAtNet + Raptor) reduciendo el tiempo de inferencia a 1.86s por estudio.

### [ ] SUPER-TAREA CMRE-249: Auto-Evolution against FAIL_02 (SNIP_SPLIT_PURGED_EMBARGO_TIME)
- **Origen:** `data/knowledge/postmortems_failures_catalog.json` (FAIL_02)
- **Problema:** Validación cruzada K-Fold aleatoria infló el score a 5.12 MAE. En la fase de test en vivo (Private LB) el score se degradó a 5.89 MAE, provocando caídas de más de 800 puestos.
- **Causa Raíz:** Autocorrelación intradiaria de alta frecuencia en el libro de órdenes (order book). Muestras contiguas en el tiempo compartían micro-tendencias y volatilidad. Un split aleatorio filtró información del futuro inmediato hacia el pasado.
- **Implementación:** PurgedGroupTimeSeriesSplit con ventana de embargo de al menos 10 minutos entre pliegues de entrenamiento y test.

